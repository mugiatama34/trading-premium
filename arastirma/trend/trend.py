"""Trend takibi modeli: günlük mumlarda N günlük kırılımla giriş, ATR'ye dayalı iz süren stopla çıkış.

Neden: PO3/AMD çalışmasından iki ders çıktı (../po3-backtest/sonuclar/ozet.md): gün içi dar stoplarda
maliyet avantajı siliyor ve coinler birlikte hareket ediyor. Trend takibi seyrek işlem yapar ve geniş
stop kullanır; maliyetin R içindeki payı küçüktür. Öneri: ../yeni-model-onerileri.md

Kurallar (tamamen mekanik):
  - Günlük mumlar 5 dk verisinden üretilir, gün 00:00 UTC'de açılır. 17 coinin tamamı, haftanın her günü.
  - Giriş: günlük kapanış son N günün en yükseğinin üstündeyse ertesi günün açılışında uzun;
    son N günün en düşüğünün altındaysa (kısaya izin varsa) kısa. Giriş piyasa emri (taker + kayma).
  - İlk stop: giriş − k × ATR(20, günlük). R = k × ATR (işlem başına risk mesafesi).
  - İz süren stop: her gün kapanıştan sonra stop, kapanış − k × ATR'ye çekilir (yalnızca lehte yönde).
    Gün içinde fiyat stopa değerse stop fiyatından çıkılır; açılış stopun ötesindeyse açılıştan (boşluk).
    Hedef yoktur. Çıkış piyasa emri (taker + kayma).
  - Coin başına aynı anda en fazla 1 pozisyon. Fonlama: pozisyon açıkken geçen her fonlama anı, gerçek oranla.
  - Portföy: işlem başına sermayenin %1'i risk, aynı yönde toplam açık risk en fazla %3 (proje kuralı).
    Aynı gün sınırı aşan sinyaller arasında kırılımı ATR'ye göre en güçlü olanlar önce alınır.

Önceden sabitlenen seçim kuralı (PO3 v2 ile aynı yöntem):
  Aday ızgarası: N {20, 50, 100} × k {2, 3, 4} × yön {iki yön, yalnızca uzun} = 18 aday.
  Yalnızca örneklem içi (2024-06-01 öncesi girişler) işlemlerle, en az 100 işlemi olan adaylar arasından
  net R ortalaması en yüksek olan seçilir ve örneklem dışında tek seferde sınanır.

Kullanım:  python trend.py      Çıktı: sonuclar/rapor.md, sonuclar/islemler.csv
"""

import csv
import math
import random
import sys
import zlib
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

KLASOR = Path(__file__).parent
sys.path.insert(0, str(KLASOR.parent / "po3-backtest"))

import backtest as B  # noqa: E402  (veri okuma, fonlama, ölçüler ve portföy hesabı ortak)
import kurallar as K  # noqa: E402

CIKTI = KLASOR / "sonuclar"
GUN_MS = 86_400_000
ATR_GUN = 20
EN_AZ_ICINDE = 100


def gunluk_mumlar(veri: dict) -> dict:
    """5 dk mumları 00:00 UTC'de açılan günlük mumlara çevirir. Günün %90'ından azı varsa gün atlanır."""
    gunler = {}
    for t, o, h, l, c in zip(veri["ts"], veri["open"], veri["high"], veri["low"], veri["close"]):
        g = t // GUN_MS * GUN_MS
        if g not in gunler:
            gunler[g] = [o, h, l, c, 1]
        else:
            m = gunler[g]
            m[1], m[2], m[3], m[4] = max(m[1], h), min(m[2], l), c, m[4] + 1
    ts = [g for g in sorted(gunler) if gunler[g][4] >= 0.9 * 288]
    return {"ts": ts, **{a: [gunler[g][i] for g in ts] for i, a in enumerate(("open", "high", "low", "close"))}}


def atr(d: dict, n: int = ATR_GUN) -> list[float]:
    h, l, c = d["high"], d["low"], d["close"]
    tr = [h[0] - l[0]] + [max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1])) for i in range(1, len(h))]
    out, toplam = [], 0.0
    for i, x in enumerate(tr):
        toplam += x - (tr[i - n] if i >= n else 0)
        out.append(toplam / min(i + 1, n))
    return out


def surdur(d, a, bas, yon, giris, risk, k):
    """bas günü açılışta girilen pozisyonu iz süren stopla izler.

    Dönüş: (çıkış günü, çıkış fiyatı, sonuç, son stop seviyesi).
    """
    o, h, l, c = d["open"], d["high"], d["low"], d["close"]
    stop = giris - yon * risk
    for j in range(bas, len(c)):
        if j > bas and (o[j] - stop) * yon <= 0:
            return j, o[j], "stop", stop  # açılış stopun ötesinde (boşluk)
        if (l[j] if yon == 1 else h[j]) * yon <= stop * yon:
            return j, stop, "stop", stop
        yeni = c[j] - yon * k * a[j]
        if (yeni - stop) * yon > 0:
            stop = yeni
    return len(c) - 1, c[-1], "acik", stop  # veri sonunda hâlâ açık: son kapanıştan değerlenir


def maliyet_r(coin, yon, giris, cikis, risk, t_giris, t_cikis, fon):
    oran = (K.TAKER + K.kayma(coin)) / 100
    zaman, fonlama = fon
    i, j = B.bisect_right(zaman, t_giris), B.bisect_left(zaman, t_cikis)
    return oran * (giris + cikis) / risk, sum(fonlama[i:j]) * giris * yon / risk


def coin_trend(coin, d, a, fon, n, k, kisa, rastgele=False):
    islemler = []
    o, h, l, c, ts = d["open"], d["high"], d["low"], d["close"], d["ts"]
    i = max(n, ATR_GUN)
    while i < len(c) - 1:
        tepe, dip = max(h[i - n:i]), min(l[i - n:i])
        yon = 1 if c[i] > tepe else (-1 if kisa and c[i] < dip else 0)
        if yon == 0:
            i += 1
            continue
        giris, risk = o[i + 1], k * a[i]
        cik, fiyat, sonuc, son_stop = surdur(d, a, i + 1, yon, giris, risk, k)
        t_g, t_c = ts[i + 1], ts[cik] + GUN_MS
        kom, fonl = maliyet_r(coin, yon, giris, fiyat, risk, t_g, t_c, fon)
        brut = (fiyat - giris) * yon / risk
        islem = {
            "coin": coin, "gun": datetime.fromtimestamp(t_g / 1000, timezone.utc).date(),
            "yon": "uzun" if yon == 1 else "kisa", "giris_zamani": t_g, "cikis_zamani": t_c,
            "giris": giris, "cikis": fiyat, "sonuc": sonuc, "gun_sayisi": cik - i,
            "guc": (c[i] - (tepe if yon == 1 else dip)) * yon / a[i],
            "stop_yuzde": 100 * risk / giris, "brut_r": brut, "komisyon_kayma_r": kom,
            "fonlama_r": fonl, "net_r": brut - kom - fonl,
            # Açık pozisyon iz süren stopundan kapansaydı (temkinli değer; kapalı işlemlerde net_r ile aynı)
            "net_r_stopta": (brut if sonuc != "acik" else (son_stop - giris) * yon / risk) - kom - fonl,
        }
        if rastgele:
            sonuclar = []
            for s in range(B.RASTGELE_TOHUM):
                y = 1 if random.Random(zlib.crc32(f"{coin}{i}{n}{k}{s}".encode())).random() < 0.5 else -1
                c2, f2, _, _ = surdur(d, a, i + 1, y, giris, risk, k)
                kom2, fon2 = maliyet_r(coin, y, giris, f2, risk, t_g, ts[c2] + GUN_MS, fon)
                sonuclar.append((f2 - giris) * y / risk - kom2 - fon2)
            islem["rastgele_net_r"] = sonuclar
        islemler.append(islem)
        i = cik + 1 if cik > i else i + 1  # pozisyon kapandıktan sonraki günden itibaren yeni sinyal
    return islemler


def portfoy(islemler, risk_yuzde, bas, bit):
    """B.portfoy ile aynı, ama aynı anda gelen sinyallerde kırılımı güçlü olan önce alınır."""
    sirali = sorted(islemler, key=lambda x: (x["giris_zamani"], -x["guc"]))
    for sira, x in enumerate(sirali):
        x["_sira"] = sira
    return B.portfoy([dict(x, giris_zamani=x["giris_zamani"] + x["_sira"] * 1e-6) for x in sirali],
                     risk_yuzde, bas, bit)


def etiket(n, k, kisa):
    return f"N={n}, stop {k}×ATR, {'iki yön' if kisa else 'yalnızca uzun'}"


def main():
    veriler = {}
    for coin in K.COINLER:
        v = B.coin_oku(coin)
        if v["ts"]:
            d = gunluk_mumlar(v)
            veriler[coin] = (d, atr(d), B.fonlama_oku(coin))
    bas_ts = min(d["ts"][0] for d, _, _ in veriler.values())
    bit_ts = max(d["ts"][-1] for d, _, _ in veriler.values()) + GUN_MS
    oos = B.ms(datetime.fromisoformat(K.ORNEKLEM_DISI_BASLANGIC).replace(tzinfo=timezone.utc))

    def calistir(n, k, kisa, rastgele=False):
        tum = []
        for coin, (d, a, fon) in veriler.items():
            tum += coin_trend(coin, d, a, fon, n, k, kisa, rastgele)
        return [x for x in tum if x["giris_zamani"] < oos], [x for x in tum if x["giris_zamani"] >= oos]

    adaylar = []
    for n, k, kisa in product((20, 50, 100), (2, 3, 4), (True, False)):
        ic, dis = calistir(n, k, kisa)
        adaylar.append(((n, k, kisa), B.ozet(ic), B.ozet(dis), portfoy(ic, 1.0, bas_ts, oos), portfoy(dis, 1.0, oos, bit_ts)))
        print(etiket(n, k, kisa), len(ic), len(dis), flush=True)

    uygun = [x for x in adaylar if x[1] and x[1]["n"] >= EN_AZ_ICINDE]
    secilen = max(uygun, key=lambda x: x[1]["net_r"])[0]
    ic, dis = calistir(*secilen, rastgele=True)
    o_ic, o_dis = B.ozet(ic), B.ozet(dis)

    s = ["# Trend Takibi Modeli: Sonuçlar\n",
         "Kod ve kurallar: `trend.py` (dosyanın başında). Veri: Binance USDT-M vadeli, 5 dk mumlardan üretilen "
         "günlük mumlar (00:00 UTC) ve gerçek fonlama oranları, 17 coin, 2021-01 → 2026-09.\n",
         "Maliyetler: giriş ve çıkış piyasa emri (taker %0,05 + coin bazında kayma %0,01–0,05), gerçek fonlama. "
         "Komisyon oranı doğrulanmadı.\n",
         f"Örneklem içi: 2021-01 → {K.ORNEKLEM_DISI_BASLANGIC}. Örneklem dışı: sonrası → 2026-09. "
         "Bu dönem trend modeli için ilk kez kullanıldı.\n",
         f"\n## Seçilen aday: {etiket(*secilen)}\n",
         f"Seçim yalnızca örneklem içi sonuçlara göre yapıldı ({len(uygun)} uygun aday arasında en yüksek net R).\n",
         B.BASLIK, "| Örneklem içi " + B.bicim(o_ic), "| Örneklem dışı " + B.bicim(o_dis)]
    for etk, grup in (("Örneklem dışı, uzun", [x for x in dis if x["yon"] == "uzun"]),
                      ("Örneklem dışı, kısa", [x for x in dis if x["yon"] == "kisa"])):
        if grup:
            s.append(f"| {etk} " + B.bicim(B.ozet(grup)))
    if o_dis:
        p1 = portfoy(dis, 1.0, oos, bit_ts)
        r_ort, r_min, r_max, r_p = B.rastgele_ozet(dis)
        s.append("\n**Örneklem dışı, devam eşikleri:**\n")
        s.append(B.esik_tablosu(o_dis, p1, r_p))
        s.append(f"\nRastgele yönlü kıyas (aynı giriş günü, aynı stop kuralı, {B.RASTGELE_TOHUM} tohum): "
                 f"ortalama net R {r_ort:+.3f} (tohumlar {r_min:+.3f} … {r_max:+.3f}); model {o_dis['net_r']:+.3f}.\n")
        sure = sorted(x["gun_sayisi"] for x in dis)
        s.append(f"\nÖrneklem dışında ortalama kazanç {o_dis['ort_kazanc']:+.2f}R, ortalama kayıp {o_dis['ort_kayip']:+.2f}R. "
                 f"Pozisyon süresi medyan {sure[len(sure) // 2]} gün. İşlem başına maliyet "
                 f"{o_dis['brut_r'] - o_dis['net_r']:.3f}R (fonlama {o_dis['fonlama_r']:+.3f}R). "
                 f"Veri sonunda açık kalan: {sum(1 for x in dis if x['sonuc'] == 'acik')}.\n")
        stopta = [x["net_r_stopta"] for x in dis]
        kapali = [x["net_r"] for x in dis if x["sonuc"] != "acik"]
        kaz, kay = sum(r for r in stopta if r > 0), -sum(r for r in stopta if r < 0)
        s.append(f"\n**Açık pozisyonlara dikkat:** Örneklem dışındaki net R'nin önemli bir kısmı veri sonunda hâlâ açık "
                 f"pozisyonlardan geliyor (son kapanıştan değerlendi). Açık pozisyonlar iz süren stoplarından kapansaydı "
                 f"ortalama net R {sum(stopta) / len(stopta):+.3f}, PF {kaz / kay:.2f} olurdu. Yalnızca kapanmış "
                 f"{len(kapali)} işlemin ortalaması {sum(kapali) / len(kapali):+.3f}R.\n")
        s.append("\n**Portföy (10.000 $ başlangıç, aynı yönde en fazla %3 açık risk):**\n")
        s.append("| Dönem | Risk/işlem | Alınan işlem | Atlanan | Son sermaye | Yıllık getiri | Maks. düşüş |\n"
                 "|---|---|---|---|---|---|---|")
        for etk, grup, b1, b2 in (("Örneklem içi", ic, bas_ts, oos), ("Örneklem dışı", dis, oos, bit_ts)):
            for r in (1.0, 2.0):
                p = portfoy(grup, r, b1, b2)
                s.append(f"| {etk} | %{r:.0f} | {p['alinan']} | {p['atlanan']} | {p['son']:,.0f} $ | "
                         f"%{p['yillik']:.1f} | %{p['dd']:.1f} |")
        mc50, mc95 = B.monte_carlo(dis)
        s.append(f"\nMonte Carlo (örneklem dışı, %1 risk, sınırsız sıralı): medyan maks. düşüş %{mc50:.1f}, "
                 f"%95 kötü durumda %{mc95:.1f}.\n")
        s.append(f"\nPozisyon büyüklüğü / sermaye: %1 riskte {B.kaldirac_satiri(ic + dis, 1)}; "
                 f"%2 riskte {B.kaldirac_satiri(ic + dis, 2)}.\n")
        s.append("\n**Yıllara göre (tüm dönem, giriş yılına göre):**\n")
        s.append(B.yil_tablosu(ic + dis))
        s.append("\n**Coinlere göre (örneklem dışı):**\n")
        s.append(B.BASLIK)
        for c in sorted({x["coin"] for x in dis}):
            s.append(f"| {c} " + B.bicim(B.ozet([x for x in dis if x["coin"] == c])))

    s.append("\n## Tüm adaylar (örneklem içi sıralı)\n")
    s.append("Örneklem dışı sütunları seçimde kullanılmadı. Portföy sütunları %1 risk ve %3 toplam risk sınırıyla.\n")
    s.append("| Aday | İçi işlem | İçi net R | İçi PF | İçi maks. düşüş | Dışı işlem | Dışı net R | Dışı PF | Dışı yıllık | Dışı maks. düşüş |\n"
             "|---|---|---|---|---|---|---|---|---|---|")
    for aday, a, b, pa, pb in sorted(adaylar, key=lambda x: -(x[1]["net_r"] if x[1] else -9)):
        isaret = " **(seçilen)**" if aday == secilen else ""
        f = lambda o: f"{o['n']} | {o['net_r']:+.3f} | {o['pf']:.2f}" if o else "0 | – | –"
        s.append(f"| {etiket(*aday)}{isaret} | {f(a)} | %{pa['dd']:.1f} | {f(b)} | %{pb['yillik']:.1f} | %{pb['dd']:.1f} |")
    pozitif = sum(1 for x in adaylar if x[2] and x[2]["net_r"] > 0)
    s.append(f"\n18 adaydan örneklem dışında net R'si pozitif olan: {pozitif}.\n")

    CIKTI.mkdir(parents=True, exist_ok=True)
    (CIKTI / "rapor.md").write_text("\n".join(s) + "\n", encoding="utf-8")
    with open(CIKTI / "islemler.csv", "w", newline="", encoding="utf-8") as fh:
        alanlar = [a for a in (ic + dis)[0] if a not in ("rastgele_net_r", "_sira")]
        w = csv.DictWriter(fh, fieldnames=alanlar, extrasaction="ignore")
        w.writeheader()
        for x in ic + dis:
            satir = dict(x)
            for a in ("giris_zamani", "cikis_zamani"):
                satir[a] = datetime.fromtimestamp(x[a] / 1000, timezone.utc).isoformat()
            w.writerow(satir)
    print("Seçilen:", etiket(*secilen))


if __name__ == "__main__":
    main()
