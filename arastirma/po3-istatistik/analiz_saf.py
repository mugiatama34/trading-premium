"""analiz.py'nin ek paket gerektirmeyen (yalnızca standart Python) karşılığı.

Neden var: Bulut ortamında pandas/numpy/scipy kurulamadığında aynı ölçümleri yapabilmek için.
Ölçüm mantığı analiz.py ile birebir aynıdır (gün dilimleme, yarışlar, maliyetler, testler).
Ek olarak Yarış 2 için profit factor ve %1 riskte maksimum düşüş hesaplar (devam eşikleri).

Veriyi pandas'a çevirmeden doğrudan `veri/ham/` altındaki Binance zip dosyalarından okur
(veri_indir.py bu dosyaları indirirken saklar).

Kullanım:  python analiz_saf.py               (veri/ham altındaki tüm coinler)
           python analiz_saf.py --sentetik    (rastgele veride doğruluk kontrolü)
"""

import csv
import io
import math
import random
import sys
import zipfile
from bisect import bisect_left
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from ayarlar import ARALIK, COINLER, GERI_KAPANIS_MUM, KLASOR, VARYANTLAR, VERI_KLASORU, gidis_donus_maliyeti

CIKTI = KLASOR / "sonuclar"
HAM = VERI_KLASORU / "ham"
SAAT_MS = 3_600_000
RISK = 0.01  # Yarış 2 sermaye eğrisi: işlem başına sermayenin %1'i


# ---------------------------------------------------------------- veri

def coin_oku(coin: str):
    """Zip dosyalarından (ts_ms, open, high, low, close) listeleri; zamana göre sıralı, tekrarsız."""
    satirlar = {}
    for dosya in sorted(HAM.glob(f"{coin}USDT-{ARALIK}-*.zip")):
        with zipfile.ZipFile(dosya) as z:
            ham = z.read(z.namelist()[0]).decode()
        okuyucu = csv.reader(io.StringIO(ham))
        for r in okuyucu:
            if not r or r[0] == "open_time":
                continue
            ts = int(r[0])
            if ts > 1e14:  # bazı yeni dosyalar mikrosaniye
                ts //= 1000
            satirlar[ts] = (float(r[1]), float(r[2]), float(r[3]), float(r[4]))
    ts = sorted(satirlar)
    return {
        "ts": ts,
        "open": [satirlar[t][0] for t in ts],
        "high": [satirlar[t][1] for t in ts],
        "low": [satirlar[t][2] for t in ts],
        "close": [satirlar[t][3] for t in ts],
    }


def ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


def gun_dilimleri(veri: dict, varyant: dict):
    """analiz.gun_dilimleri ile aynı: (gün, dilim, rel saatler, beklenen mum sayısı)."""
    tz = ZoneInfo(varyant["saat_dilimi"])
    ts = veri["ts"]
    ilk = datetime.fromtimestamp(ts[0] / 1000, timezone.utc).astimezone(tz).date()
    son = datetime.fromtimestamp(ts[-1] / 1000, timezone.utc).astimezone(tz).date()
    gun = ilk
    while gun <= son:
        gece = datetime(gun.year, gun.month, gun.day)
        acilis = ms(gece.replace(tzinfo=tz))
        bas = ms((gece + timedelta(hours=min(varyant["asya"][0], 0))).replace(tzinfo=tz))
        bitis = ms((gece + timedelta(days=1)).replace(tzinfo=tz))
        i0, i1 = bisect_left(ts, bas), bisect_left(ts, bitis)
        dilim = {k: veri[k][i0:i1] for k in ("open", "high", "low", "close")}
        rel = [(t - acilis) / SAAT_MS for t in ts[i0:i1]]
        yield gun, dilim, rel, (bitis - acilis) / 300_000
        gun += timedelta(days=1)


# ---------------------------------------------------------------- ölçümler

def yaris(h, l, bas, ust, alt):
    for i in range(bas, len(h)):
        u, a = h[i] >= ust, l[i] <= alt
        if u and a:
            return "belirsiz", i
        if u:
            return "ust", i
        if a:
            return "alt", i
    return "yok", len(h) - 1


def gun_olaylari(g, rel, beklenen_gun, varyant, onceki, maliyet):
    asya_bas, asya_bit = varyant["asya"]
    man_bas, man_bit = varyant["manipulasyon"]
    h, l, c, o = g["high"], g["low"], g["close"], g["open"]

    asya = [i for i, r in enumerate(rel) if asya_bas <= r < asya_bit]
    gun_idx = [i for i, r in enumerate(rel) if r >= 0]
    if len(asya) < 0.9 * (asya_bit - asya_bas) * 12 or len(gun_idx) < 0.9 * beklenen_gun:
        return None

    ah, al = max(h[i] for i in asya), min(l[i] for i in asya)
    r = ah - al
    i_yuksek = max(gun_idx, key=lambda i: (h[i], -i))  # eşitlikte ilk mum (np.argmax gibi)
    i_dusuk = min(gun_idx, key=lambda i: (l[i], i))
    kayit = {
        "acilis": o[gun_idx[0]], "kapanis": c[gun_idx[-1]],
        "yuksek": h[i_yuksek], "dusuk": l[i_dusuk],
        "yuksek_saat": int(rel[i_yuksek]), "dusuk_saat": int(rel[i_dusuk]),
        "asya_yuksek": ah, "asya_dusuk": al,
    }
    if onceki is not None:
        orta = (onceki["yuksek"] + onceki["dusuk"]) / 2
        kayit["bias"] = "yukari" if onceki["kapanis"] > orta else "asagi"

    man = [i for i, x in enumerate(rel) if man_bas <= x < man_bit]
    if r <= 0 or not man:
        kayit["supurme"] = "veri_yok"
        return kayit
    t_ust = next((i for i in man if h[i] > ah), None)
    t_alt = next((i for i in man if l[i] < al), None)
    if t_ust is None and t_alt is None:
        kayit["supurme"] = "yok"
        return kayit
    if t_ust is not None and t_ust == t_alt:
        kayit["supurme"] = "ayni_mum"
        return kayit

    if t_alt is None or (t_ust is not None and t_ust < t_alt):
        yon, t, seviye, karsi = 1, t_ust, ah, al
    else:
        yon, t, seviye, karsi = -1, t_alt, al, ah
    kayit["supurme"] = "ust" if yon == 1 else "alt"
    if "bias" in kayit:
        kayit["bias_uyumlu"] = (kayit["bias"] == "yukari") == (yon == -1)

    son = len(h)
    donus_tarafi = "alt" if yon == 1 else "ust"

    p1 = c[t]
    d1 = (p1 - karsi) * yon
    if d1 > 0:
        ust, alt = (p1 + d1, karsi) if yon == 1 else (karsi, p1 - d1)
        sonuc, _ = yaris(h, l, t + 1, ust, alt)
        kayit["yaris1"] = {"belirsiz": "belirsiz", "yok": "yok"}.get(
            sonuc, "donus" if sonuc == donus_tarafi else "devam")

    kayit["karsi_taraf"] = (any(x <= al for x in l[t:son]) if yon == 1
                            else any(x >= ah for x in h[t:son]))

    for j in range(t, min(t + GERI_KAPANIS_MUM, son)):
        if (c[j] < seviye) if yon == 1 else (c[j] > seviye):
            break
    else:
        kayit["geri_kapanis"] = False
        return kayit
    p = c[j]
    d = (p - karsi) * yon
    if d <= 0:
        kayit["geri_kapanis"] = False
        return kayit
    kayit["geri_kapanis"] = True
    ust, alt = (p + d, karsi) if yon == 1 else (karsi, p - d)
    sonuc, i = yaris(h, l, j + 1, ust, alt)
    maliyet_r = maliyet * p / d
    if sonuc == "yok":
        kayit["yaris2"] = "yok"
        brut = (p - c[i]) * yon / d
    elif sonuc == "belirsiz":
        kayit["yaris2"] = "belirsiz"
        brut = -1.0
    else:
        kayit["yaris2"] = "donus" if sonuc == donus_tarafi else "devam"
        brut = 1.0 if kayit["yaris2"] == "donus" else -1.0
    kayit["yaris2_brut_r"] = brut
    kayit["yaris2_net_r"] = brut - maliyet_r
    kayit["yaris2_mesafe_yuzde"] = 100 * d / p
    return kayit


def coin_analiz(coin: str, veri: dict, maliyet: float | None = None) -> list[dict]:
    satirlar = []
    maliyet = gidis_donus_maliyeti(coin) if maliyet is None else maliyet
    for ad, varyant in VARYANTLAR.items():
        onceki = None
        for gun, g, rel, beklenen in gun_dilimleri(veri, varyant):
            kayit = gun_olaylari(g, rel, beklenen, varyant, onceki, maliyet)
            if kayit is None:
                onceki = None
                continue
            kayit.update(coin=coin, varyant=ad, gun=gun)
            satirlar.append(kayit)
            onceki = kayit
    return satirlar


# ---------------------------------------------------------------- istatistik (scipy yerine)

Z95 = 1.959963984540054


def binom_p(k: int, n: int) -> float:
    """İki yönlü kesin binom testi, p=0,5 (scipy.stats.binomtest ile aynı tanım)."""
    logpmf = [math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) - n * math.log(2)
              for i in range(n + 1)]
    sinir = logpmf[k] + math.log1p(1e-7)
    return min(1.0, sum(math.exp(x) for x in logpmf if x <= sinir))


def wilson(k: int, n: int):
    z2 = Z95 ** 2
    merkez = (k + z2 / 2) / (n + z2)
    yari = Z95 / (n + z2) * math.sqrt(k * (n - k) / n + z2 / 4)
    return merkez - yari, merkez + yari


def oran_satiri(basari: int, n: int) -> str:
    if n == 0:
        return "– | – | –"
    alt, ust = wilson(basari, n)
    return f"%{100 * basari / n:.1f} | %{100 * alt:.1f}–{100 * ust:.1f} | {binom_p(basari, n):.3f}"


def yaris_ozet(kayitlar, sutun):
    s = [k.get(sutun) for k in kayitlar]
    don, dev = s.count("donus"), s.count("devam")
    return don, don + dev


def ortalama(x):
    return sum(x) / len(x)


def net_r_satiri(r) -> str:
    if len(r) < 2:
        return "– | –"
    m = ortalama(r)
    se = math.sqrt(sum((v - m) ** 2 for v in r) / (len(r) - 1)) / math.sqrt(len(r))
    return f"{m:+.3f} | {m - Z95 * se:+.3f} – {m + Z95 * se:+.3f}"


def profit_factor(r) -> float:
    kazanc = sum(v for v in r if v > 0)
    kayip = -sum(v for v in r if v < 0)
    return kazanc / kayip if kayip else math.inf


def max_dusus(kayitlar) -> float:
    """İşlemler tarih sırasıyla, her biri o anki sermayenin %1'i riskle (bileşik). Yüzde döner."""
    sermaye, tepe, dd = 1.0, 1.0, 0.0
    for k in sorted(kayitlar, key=lambda k: (k["gun"], k["coin"])):
        sermaye *= 1 + RISK * k["yaris2_net_r"]
        tepe = max(tepe, sermaye)
        dd = max(dd, 1 - sermaye / tepe)
    return 100 * dd


# ---------------------------------------------------------------- raporlama

def rapor_yaz(olaylar: list[dict]) -> str:
    s = []
    s.append("# PO3 İstatistik Ön Çalışması: Sonuçlar\n")
    s.append(f"Veri: Binance USDT-M vadeli, {ARALIK} mumlar. Analiz betiği: `analiz_saf.py` "
             "(`analiz.py` ile aynı ölçüm mantığı, ek paket gerektirmez).\n")
    s.append("Tablolardaki **oran** dönüş yüzdesidir; **%95 GA** güven aralığıdır; **p** değeri "
             "%50'den (rastgele) farkın tesadüf olma olasılığıdır (0,05'in altı anlamlı kabul edilir).\n")
    s.append("**Net R**: Yarış 2'yi işlem gibi düşünür (geri kapanışta giriş, stop ve hedef eşit "
             "uzaklıkta, gün sonunda zaman çıkışı). Komisyon, kayma ve fonlama payı düşülmüştür; "
             "aynı mumda iki seviyeye değilen durumlar zarar sayılır. Devam eşiği: +0,15R.\n")
    s.append("**PF** (profit factor): net kazançların toplamı / net kayıpların toplamı (eşik 1,3). "
             "**Maks. düşüş**: işlemler tarih sırasıyla, her biri sermayenin %1'i riskle bileşik "
             "uygulandığında en büyük tepeden düşüş (eşik %20). Basitleştirme: aynı gün birden fazla "
             "coinde işlem olabilir, %3 toplam açık risk sınırı burada uygulanmadı.\n")
    s.append("Not: Bu bir strateji backtest'i değildir; kural seti v1'deki MSS ve FVG onayları "
             "yoktur. Modelin temel varsayımının veride olup olmadığını ölçer.\n")

    s.append("\n## Veri kapsamı\n")
    s.append("| Coin | Varyant | Gün sayısı | İlk gün | Son gün |\n|---|---|---|---|---|")
    grup = defaultdict(list)
    for k in olaylar:
        grup[(k["coin"], k["varyant"])].append(k["gun"])
    for (coin, var), gunler in sorted(grup.items()):
        s.append(f"| {coin} | {var} | {len(gunler)} | {min(gunler)} | {max(gunler)} |")

    for ad in VARYANTLAR:
        v = [k for k in olaylar if k["varyant"] == ad]
        if not v:
            continue
        baslik = "00:00 UTC açılışı" if ad == "utc" else "New York gece yarısı açılışı"
        s.append(f"\n## Varyant: {baslik}\n")

        dag = Counter(k["supurme"] for k in v)
        s.append("**Londra penceresinde süpürme dağılımı:** " + ", ".join(
            f"{x} %{100 * dag[x] / len(v):.1f}" for x in ("ust", "alt", "ayni_mum", "yok")) + "\n")
        tek = [k for k in v if k["supurme"] in ("ust", "alt")]
        if tek:
            s.append(f"**Tek taraf süpürmesinden sonra gün içinde Asya aralığının karşı tarafına "
                     f"ulaşma oranı:** %{100 * ortalama([k['karsi_taraf'] for k in tek]):.1f} ({len(tek)} gün)\n")

        s.append("\n### Soru 1 ve 3: Süpürme sonrası dönüş mü devam mı?\n")
        s.append("| Ölçüm | Dönüş / toplam | Oran | %95 GA | p |\n|---|---|---|---|---|")
        for etiket, alt_k, sutun in [
            ("Yarış 1: süpürme mumu kapanışından (onaysız)", tek, "yaris1"),
            ("Yarış 2: geri kapanış sonrası (onaylı)", tek, "yaris2"),
            ("Yarış 2, bias ile uyumlu", [k for k in tek if k.get("bias_uyumlu") is True], "yaris2"),
            ("Yarış 2, bias'a ters", [k for k in tek if k.get("bias_uyumlu") is False], "yaris2"),
        ]:
            don, n = yaris_ozet(alt_k, sutun)
            s.append(f"| {etiket} | {don} / {n} | {oran_satiri(don, n)} |")

        s.append("\n### Yarış 2 işlem gibi düşünülürse (maliyetler dahil)\n")
        s.append("| Grup | İşlem | Kazanma | Ort. mesafe | Brüt R | Net R | Net R %95 GA | PF | Maks. düşüş |\n"
                 "|---|---|---|---|---|---|---|---|---|")
        y2 = [k for k in tek if "yaris2_net_r" in k]
        gruplar = [("Tümü", y2), ("Bias uyumlu", [k for k in y2 if k.get("bias_uyumlu") is True])]
        gruplar += [(c, [k for k in y2 if k["coin"] == c]) for c in sorted({k["coin"] for k in y2})]
        for etiket, g in gruplar:
            if not g:
                continue
            net = [k["yaris2_net_r"] for k in g]
            kaz = 100 * ortalama([k["yaris2"] == "donus" for k in g])
            s.append(f"| {etiket} | {len(g)} | %{kaz:.1f} | %{ortalama([k['yaris2_mesafe_yuzde'] for k in g]):.2f} | "
                     f"{ortalama([k['yaris2_brut_r'] for k in g]):+.3f} | {net_r_satiri(net)} | "
                     f"{profit_factor(net):.2f} | %{max_dusus(g):.1f} |")

        if y2:
            s.append("\n**Yıllara göre (Yarış 2, tüm coinler):**\n")
            s.append("| Yıl | İşlem | Kazanma | Net R |\n|---|---|---|---|")
            yillar = defaultdict(list)
            for k in y2:
                yillar[k["gun"].year].append(k)
            for y in sorted(yillar):
                g = yillar[y]
                s.append(f"| {y} | {len(g)} | %{100 * ortalama([k['yaris2'] == 'donus' for k in g]):.1f} | "
                         f"{ortalama([k['yaris2_net_r'] for k in g]):+.3f} |")

        s.append("\n### Soru 2: Günün tepesi ve dibi hangi saatte oluşuyor?\n")
        s.append("Saatler günün açılışından itibaren sayılır (0 = açılış saati, yerel saat).\n")
        s.append("| Saat | Tepe % | Dip % |\n|---|---|---|")
        ht, dt = Counter(k["yuksek_saat"] for k in v), Counter(k["dusuk_saat"] for k in v)
        for saat in range(24):
            s.append(f"| {saat:02d} | {100 * ht[saat] / len(v):.1f} | {100 * dt[saat] / len(v):.1f} |")

        s.append("\n### Soru 4: Bias kuralı günün yönünü tahmin ediyor mu?\n")
        b = [k for k in v if "bias" in k]
        dogru = sum(1 for k in b if (k["kapanis"] > k["acilis"] and k["bias"] == "yukari")
                    or (k["kapanis"] < k["acilis"] and k["bias"] == "asagi"))
        s.append("| Doğru / toplam | Oran | %95 GA | p |\n|---|---|---|---|")
        s.append(f"| {dogru} / {len(b)} | {oran_satiri(dogru, len(b))} |")
    return "\n".join(s) + "\n"


def csv_yaz(olaylar: list[dict], yol) -> None:
    sutunlar = []
    for k in olaylar:
        for a in k:
            if a not in sutunlar:
                sutunlar.append(a)
    with open(yol, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=sutunlar)
        w.writeheader()
        w.writerows(olaylar)


# ---------------------------------------------------------------- sentetik kontrol

def rastgele_veri(gun: int, tohum: int) -> dict:
    """sentetik_kontrol.rastgele_veri ile aynı yapı: log-normal rastgele yürüyüş + rastgele fitiller."""
    rng = random.Random(tohum)
    n = 288 * gun
    bas = ms(datetime(2020, 1, 1, tzinfo=timezone.utc))
    veri = {"ts": [], "open": [], "high": [], "low": [], "close": []}
    log_fiyat, onceki = math.log(100), 100.0
    for i in range(n):
        log_fiyat += rng.gauss(0, 0.0015)
        kap = math.exp(log_fiyat)
        veri["ts"].append(bas + i * 300_000)
        veri["open"].append(onceki)
        veri["high"].append(max(onceki, kap) * (1 + abs(rng.gauss(0, 0.0007))))
        veri["low"].append(min(onceki, kap) * (1 - abs(rng.gauss(0, 0.0007))))
        veri["close"].append(kap)
        onceki = kap
    return veri


def sentetik_kontrol() -> None:
    olaylar = [k for t in range(3) for k in coin_analiz("BTC", rastgele_veri(2000, t), maliyet=0.0)]
    hata = False
    for varyant in VARYANTLAR:
        v = [k for k in olaylar if k["varyant"] == varyant]
        for sutun in ("yaris1", "yaris2"):
            don, n = yaris_ozet(v, sutun)
            p = binom_p(don, n)
            print(f"{varyant} {sutun}: dönüş %{100 * don / n:.1f} ({n} olay), p={p:.3f}")
            hata |= p < 0.01
        r = [k["yaris2_brut_r"] for k in v if "yaris2_brut_r" in k]
        print(f"{varyant} yaris2 brüt R ortalaması: {ortalama(r):+.3f} (≈0 olmalı)")
    print("SONUÇ:", "ŞÜPHELİ, ölçüm yöntemini kontrol et" if hata else "geçti")


def main() -> None:
    coinler = [c for c in COINLER if any(HAM.glob(f"{c}USDT-{ARALIK}-*.zip"))]
    if not coinler:
        raise SystemExit(f"{HAM} altında veri yok. Önce veri_indir.py çalıştırılmalı.")
    olaylar = []
    for coin in coinler:
        olaylar += coin_analiz(coin, coin_oku(coin))
        print(f"{coin}: tamam", flush=True)
    CIKTI.mkdir(parents=True, exist_ok=True)
    csv_yaz(olaylar, CIKTI / "gunluk_olaylar.csv")
    (CIKTI / "rapor.md").write_text(rapor_yaz(olaylar), encoding="utf-8")
    print(f"Rapor: {CIKTI / 'rapor.md'}")


if __name__ == "__main__":
    sentetik_kontrol() if "--sentetik" in sys.argv else main()
