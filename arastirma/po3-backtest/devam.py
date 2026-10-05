"""Devam (kırılım) modeli: Asya aralığı Londra'da kırılınca kırılım yönünde işlem.

Neden: Aşama 3'te Asya süpürmesinden sonra fiyatın geri dönmek yerine hafifçe aynı yönde devam ettiği
görüldü (dönüş oranı %47–49). Bu model o eğilimi doğrudan işlemeye çalışır. PO3'ün tersidir.

Kurallar (yükseliş senaryosu; düşüş aynası):
  - Asya aralığı ve manipülasyon penceresi v1 ile aynı (UTC: 00–06 / 06–10, NY: 20–24 / 02–05 NY saati).
  - Pencerede Asya aralığının ilk kırılan tarafı yönü belirler (yukarı kırılım → uzun). İki taraf aynı
    mumda kırılırsa işlem yok. Coin başına günde en fazla 1 işlem, yalnızca hafta içi.
  - Giriş "piyasa": kırılım mumu seviyenin ötesinde kapanırsa kapanışta piyasa emri (taker + kayma).
    Giriş "retest": kırılan seviyeye limit alış (maker); fiyat seviyenin altına inerse dolmuş sayılır;
    24 mum (2 saat) içinde dolmazsa ya da dolmadan hedefe giderse iptal.
  - Stop "karsi": Asya aralığının karşı tarafı. Stop "orta": Asya aralığının ortası.
  - Hedef: 1R, 2R ya da "gun" (hedef yok, yalnızca zaman çıkışı).
  - Bias "var": yalnızca v1 bias'ı ile aynı yöndeki kırılımlar. "yok": tüm kırılımlar.
  - Zaman çıkışı ve maliyetler v1 ile aynı (UTC 20:00 / NY 16:00; gerçek fonlama).

Önceden sabitlenen seçim kuralı (v2 ile aynı yöntem):
  Aday ızgarası: açılış {UTC, NY} × giriş {piyasa, retest} × stop {karsi, orta} × hedef {1R, 2R, gun}
  × bias {var, yok} = 48 aday. Yalnızca örneklem içi (2024-06-01 öncesi) işlemlerle, en az 150 işlemi
  olan adaylar arasından net R'si en yüksek olan seçilir ve örneklem dışında tek seferde sınanır.

Kullanım:  python devam.py      Çıktı: sonuclar/devam_rapor.md, sonuclar/devam_islemler.csv
"""

import csv
import math
import random
import zlib
from dataclasses import dataclass
from datetime import datetime, timezone
from itertools import product

import backtest as B
import kurallar as K

RETEST_BEKLEME = 24
EN_AZ_ICINDE = 150


@dataclass(frozen=True)
class Devam:
    temel: K.Kurallar
    giris: str  # "piyasa" | "retest"
    stop: str  # "karsi" | "orta"
    hedef: str  # "1R" | "2R" | "gun"
    bias: bool


def etiket(d: Devam) -> str:
    acilis = "UTC" if d.temel.ad == "utc" else "NY"
    return (f"{acilis}, giriş {d.giris}, stop {d.stop}, hedef {d.hedef}, "
            f"bias {'var' if d.bias else 'yok'}")


def maliyet(coin, yon, giris, risk, cikis_fiyat, sonuc, giris_turu, t_giris, t_cikis, fon):
    """R cinsinden (komisyon + kayma, fonlama). Fiyatlar gerçek (pozitif) değerlerdir."""
    kayma = K.kayma(coin)
    kom = (K.MAKER if giris_turu == "retest" else K.TAKER + kayma) / 100 * giris
    kom += (K.MAKER if sonuc == "hedef" else K.TAKER + kayma) / 100 * cikis_fiyat
    zaman, oran = fon
    a, b = B.bisect_right(zaman, t_giris), B.bisect_left(zaman, t_cikis)
    return kom / risk, sum(oran[a:b]) * giris * yon / risk


def ilk_kirilim(veri, i0, rel, k, ah, al):
    h, l = veri["high"], veri["low"]
    for i, r in enumerate(rel):
        if k.manipulasyon[0] <= r < k.manipulasyon[1]:
            u, a = h[i0 + i] > ah, l[i0 + i] < al
            if u and a:
                return None, None
            if u or a:
                return i, (1 if u else -1)
    return None, None


def gun_plani(veri, i0, i1, rel, onceki, d: Devam):
    """Kırılım gününün giriş planı: (yön, dolum mumu, giriş, stop, hedef, yönlü fiyatlar) ya da None."""
    k = d.temel
    asya = [i for i, r in enumerate(rel) if k.asya[0] <= r < k.asya[1]]
    ah = max(veri["high"][i0 + i] for i in asya)
    al = min(veri["low"][i0 + i] for i in asya)
    t, yon = ilk_kirilim(veri, i0, rel, k, ah, al)
    if t is None:
        return None
    if d.bias:
        if onceki is None:
            return None
        bias = 1 if onceki["kapanis"] > (onceki["yuksek"] + onceki["dusuk"]) / 2 else -1
        if bias != yon:
            return None
    H, L, C = B.yonlu(veri, i0, i1, yon)
    seviye, karsi = (ah, al) if yon == 1 else (-al, -ah)
    stop = karsi if d.stop == "karsi" else (seviye + karsi) / 2
    if d.giris == "piyasa":
        if C[t] <= seviye:
            return None  # kırılım mumu seviyenin ötesinde kapanmadı
        giris = C[t]
        risk = giris - stop
        hedef = math.inf if d.hedef == "gun" else giris + float(d.hedef.rstrip("R")) * risk
        # Kapanışta girildiği için kırılım mumunun kendisi sayılmaz; sonraki mum temkinli dolum mumu gibi işlenir
        return yon, t + 1, giris, stop, hedef, (H, L, C) if t + 1 < len(H) else None
    giris = seviye
    risk = giris - stop
    hedef = math.inf if d.hedef == "gun" else giris + float(d.hedef.rstrip("R")) * risk
    for q in range(t + 1, min(t + 1 + RETEST_BEKLEME, len(H))):
        if rel[q] >= k.cikis:
            return None
        if L[q] < giris:
            return yon, q, giris, stop, hedef, (H, L, C)
        if H[q] >= hedef:
            return None
    return None


def coin_devam(coin, veri, fon, d: Devam, rastgele=False):
    k = d.temel
    islemler = []
    for gun, i0, i1, rel, onceki in B.gunler(veri, k):
        if gun.weekday() >= 5 or i1 - i0 == 0:
            continue
        if (sum(1 for r in rel if k.asya[0] <= r < k.asya[1]) < 0.9 * (k.asya[1] - k.asya[0]) * 12
                or sum(1 for r in rel if 0 <= r < k.cikis) < 0.9 * k.cikis * 12):
            continue
        plan = gun_plani(veri, i0, i1, rel, onceki, d)
        if plan is None or plan[5] is None:
            continue
        yon, q, giris, stop, hedef, (H, L, C) = plan
        if not stop < giris:
            continue
        risk = giris - stop
        cik, fiyat, sonuc = B.surdur(H, L, C, rel, q, giris, stop, hedef, k.cikis)
        t_g, t_c = veri["ts"][i0 + q], veri["ts"][i0 + cik] + B.MUM_MS
        kom, fonl = maliyet(coin, yon, giris * yon, risk, fiyat * yon, sonuc, d.giris, t_g, t_c, fon)
        brut = (fiyat - giris) / risk
        islem = {
            "coin": coin, "varyant": k.ad, "gun": gun, "yon": "uzun" if yon == 1 else "kisa",
            "giris_zamani": t_g, "cikis_zamani": t_c, "giris": giris * yon, "stop": stop * yon,
            "sonuc": sonuc, "stop_yuzde": 100 * risk / abs(giris), "brut_r": brut,
            "komisyon_kayma_r": kom, "fonlama_r": fonl, "net_r": brut - kom - fonl,
        }
        if rastgele:
            hedef_r = (hedef - giris) / risk
            sonuclar = []
            for s in range(B.RASTGELE_TOHUM):
                y = 1 if random.Random(zlib.crc32(f"{coin}{i0}{k.ad}{s}".encode())).random() < 0.5 else -1
                Hy, Ly, Cy = B.yonlu(veri, i0, i1, y)
                g = giris * yon * y
                c2, f2, s2 = B.surdur(Hy, Ly, Cy, rel, q, g, g - risk, g + hedef_r * risk, k.cikis)
                kom2, fon2 = maliyet(coin, y, abs(g), risk, f2 * y, s2, d.giris, t_g,
                                     veri["ts"][i0 + c2] + B.MUM_MS, fon)
                sonuclar.append((f2 - g) / risk - kom2 - fon2)
            islem["rastgele_net_r"] = sonuclar
        islemler.append(islem)
    return islemler


def main():
    veriler = B.veri_yukle()
    bit_ts = max(v["ts"][-1] for v, _, _ in veriler.values())
    oos = B.ms(datetime.fromisoformat(K.ORNEKLEM_DISI_BASLANGIC).replace(tzinfo=timezone.utc))

    def calistir(d, rastgele=False):
        tum = []
        for coin, (v, _, fon) in veriler.items():
            tum += coin_devam(coin, v, fon, d, rastgele)
        return [x for x in tum if x["giris_zamani"] < oos], [x for x in tum if x["giris_zamani"] >= oos]

    adaylar = []
    for ad, giris, stop, hedef, bias in product(K.TEMEL, ("piyasa", "retest"), ("karsi", "orta"),
                                                 ("1R", "2R", "gun"), (True, False)):
        d = Devam(K.TEMEL[ad], giris, stop, hedef, bias)
        ic, dis = calistir(d)
        adaylar.append((d, B.ozet(ic), B.ozet(dis)))
        print(etiket(d), len(ic), len(dis), flush=True)

    uygun = [a for a in adaylar if a[1] and a[1]["n"] >= EN_AZ_ICINDE]
    secilen = max(uygun, key=lambda a: a[1]["net_r"])[0]
    ic, dis = calistir(secilen, rastgele=True)
    o_ic, o_dis = B.ozet(ic), B.ozet(dis)

    s = ["# Devam (Kırılım) Modeli: Sonuçlar\n",
         "Kod ve kurallar: `devam.py` (dosyanın başında). Maliyetler: retest girişi ve hedef maker %0,02; "
         "piyasa girişi, stop ve zaman çıkışı taker %0,05 + coin bazında kayma; gerçek fonlama.\n",
         f"Örneklem içi: 2021-01 → {K.ORNEKLEM_DISI_BASLANGIC}. Örneklem dışı: sonrası → 2026-09.\n",
         f"\n## Seçilen aday: {etiket(secilen)}\n",
         f"Seçim yalnızca örneklem içi sonuçlara göre yapıldı ({len(uygun)} uygun aday arasında en yüksek net R).\n",
         B.BASLIK, "| Örneklem içi " + B.bicim(o_ic), "| Örneklem dışı " + B.bicim(o_dis)]
    if o_dis:
        p1 = B.portfoy(dis, 1.0, oos, bit_ts)
        r_ort, r_min, r_max, r_p = B.rastgele_ozet(dis)
        s.append("\n**Örneklem dışı, devam eşikleri:**\n")
        s.append(B.esik_tablosu(o_dis, p1, r_p))
        s.append(f"\nRastgele yönlü kıyas ({B.RASTGELE_TOHUM} tohum): ortalama net R {r_ort:+.3f} "
                 f"(tohumlar {r_min:+.3f} … {r_max:+.3f}); model {o_dis['net_r']:+.3f}.\n")
        dagilim = ", ".join(f"{a} %{100 * sum(1 for x in dis if x['sonuc'] == a) / len(dis):.1f}"
                            for a in ("hedef", "stop", "zaman"))
        s.append(f"\nÖrneklem dışı sonuç dağılımı: {dagilim}. İşlem başına maliyet "
                 f"{o_dis['brut_r'] - o_dis['net_r']:.3f}R.\n")
        s.append("\n**Örneklem dışı portföy (10.000 $, aynı yönde en fazla %3 açık risk):**\n")
        s.append("| Risk/işlem | Alınan işlem | Atlanan | Son sermaye | Yıllık getiri | Maks. düşüş |\n|---|---|---|---|---|---|")
        for r in (1.0, 2.0):
            p = B.portfoy(dis, r, oos, bit_ts)
            s.append(f"| %{r:.0f} | {p['alinan']} | {p['atlanan']} | {p['son']:,.0f} $ | %{p['yillik']:.1f} | %{p['dd']:.1f} |")
        mc50, mc95 = B.monte_carlo(dis)
        s.append(f"\nMonte Carlo (örneklem dışı, %1 risk): medyan maks. düşüş %{mc50:.1f}, %95 kötü durumda %{mc95:.1f}.\n")
        s.append(f"\nGereken kaldıraç: %1 riskte {B.kaldirac_satiri(ic + dis, 1)}; %2 riskte {B.kaldirac_satiri(ic + dis, 2)}.\n")
        s.append("\n**Yıllara göre (tüm dönem):**\n")
        s.append(B.yil_tablosu(ic + dis))
        s.append("\n**Coinlere göre (örneklem dışı):**\n")
        s.append(B.BASLIK)
        for c in sorted({x["coin"] for x in dis}):
            s.append(f"| {c} " + B.bicim(B.ozet([x for x in dis if x["coin"] == c])))

    s.append("\n## Tüm adaylar (örneklem içi sıralı)\n")
    s.append("Örneklem dışı sütunları seçimde kullanılmadı.\n")
    s.append("| Aday | İçi işlem | İçi brüt R | İçi net R | İçi PF | Dışı işlem | Dışı brüt R | Dışı net R | Dışı PF |\n"
             "|---|---|---|---|---|---|---|---|---|")
    f = lambda o: f"{o['n']} | {o['brut_r']:+.3f} | {o['net_r']:+.3f} | {o['pf']:.2f}" if o else "0 | – | – | –"
    for d, a, b in sorted(adaylar, key=lambda x: -(x[1]["net_r"] if x[1] else -9)):
        isaret = " **(seçilen)**" if d == secilen else ""
        s.append(f"| {etiket(d)}{isaret} | {f(a)} | {f(b)} |")
    pozitif = sum(1 for _, _, b in adaylar if b and b["net_r"] > 0)
    gecen = sum(1 for _, _, b in adaylar if b and b["n"] >= 100 and b["net_r"] >= 0.15 and b["pf"] >= 1.3)
    s.append(f"\n48 adaydan örneklem dışında net R'si pozitif olan: {pozitif}; işlem sayısı, beklenti ve PF "
             f"eşiğini birlikte geçen: {gecen}.\n")

    (B.CIKTI / "devam_rapor.md").write_text("\n".join(s) + "\n", encoding="utf-8")
    with open(B.CIKTI / "devam_islemler.csv", "w", newline="", encoding="utf-8") as fh:
        alanlar = [a for a in (ic + dis)[0] if a != "rastgele_net_r"]
        w = csv.DictWriter(fh, fieldnames=alanlar, extrasaction="ignore")
        w.writeheader()
        for x in ic + dis:
            satir = dict(x)
            for a in ("giris_zamani", "cikis_zamani"):
                satir[a] = datetime.fromtimestamp(x[a] / 1000, timezone.utc).isoformat()
            w.writerow(satir)
    print("Seçilen:", etiket(secilen))


if __name__ == "__main__":
    main()
