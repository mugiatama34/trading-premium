"""Aşama 3 istatistik ön çalışması: Asya aralığı süpürmesi ve PO3 varsayımları.

Sorular (yol haritası, Aşama 3):
  1. Londra'da Asya aralığının bir tarafı süpürülünce fiyat diğer tarafa gider mi?
     Rastgele harekete (yazı-tura, %50) göre fark var mı?
  2. Günün en yüksek ve en düşük noktası en sık hangi saatte oluşuyor?
  3. Süpürmeden sonra seviyenin içine geri kapanış (sahte kırılım onayı) sonucu değiştiriyor mu?
  4. Basit bias kuralı (önceki gün kapanışı orta noktanın üstünde mi) günün yönünü tahmin ediyor mu?

"Yarış" ölçümü: başlangıç noktasından hedefe (dönüş) ve aynı uzaklıktaki ters seviyeye
(devam) eşit mesafe vardır. Fiyat rastgele hareket etseydi dönüş oranı ~%50 olurdu.
%50'nin anlamlı şekilde üstündeki bir oran, modelin dayandığı varsayımın veride olduğunu gösterir.

Kullanım:  python analiz.py         (veri/ altındaki tüm coinler)
"""

import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest

from ayarlar import (
    ARALIK, GERI_KAPANIS_MUM, KLASOR, VARYANTLAR, VERI_KLASORU, gidis_donus_maliyeti,
)

CIKTI = KLASOR / "sonuclar"


# ---------------------------------------------------------------- gün tablosu

def gun_dilimleri(df: pd.DataFrame, varyant: dict):
    """Her işlem günü için (gün, mumlar, açılıştan itibaren saat) üretir.

    Gün, yerel gece yarısında açılır. Asya penceresi önceki akşam başlıyorsa
    (New York varyantı) o mumlar da güne eklenir ve saatleri negatif olur.
    """
    tz = varyant["saat_dilimi"]
    zaman = df["ts"].dt.tz_convert("UTC").dt.tz_localize(None).to_numpy()
    utc = lambda t: t.tz_convert("UTC").tz_localize(None).to_datetime64()
    yerel = df["ts"].dt.tz_convert(tz)
    for gun in pd.date_range(yerel.iloc[0].date(), yerel.iloc[-1].date(), freq="D"):
        acilis = gun.tz_localize(tz)
        bas = (gun + pd.Timedelta(hours=min(varyant["asya"][0], 0))).tz_localize(tz)
        bitis = (gun + pd.Timedelta(days=1)).tz_localize(tz)
        i0, i1 = np.searchsorted(zaman, [utc(bas), utc(bitis)])
        g = df.iloc[i0:i1]
        rel = (zaman[i0:i1] - utc(acilis)) / np.timedelta64(1, "h")
        beklenen = (bitis - acilis).total_seconds() / 300
        yield gun.date(), g, rel, beklenen


def yaris(h, l, c, bas, ust, alt):
    """bas indeksinden itibaren önce hangi seviyeye değildiğini döndürür.

    Dönüş: ("ust" | "alt" | "belirsiz" | "yok", son indeks)
    "belirsiz": iki seviye aynı mumda; 5 dakikalık veride sıra bilinemez.
    """
    for i in range(bas, len(h)):
        u, a = h[i] >= ust, l[i] <= alt
        if u and a:
            return "belirsiz", i
        if u:
            return "ust", i
        if a:
            return "alt", i
    return "yok", len(h) - 1


def gun_olaylari(g, rel, beklenen_gun, varyant: dict, onceki: dict | None, maliyet: float):
    asya_bas, asya_bit = varyant["asya"]
    man_bas, man_bit = varyant["manipulasyon"]
    h, l, c, o = (g[k].to_numpy() for k in ("high", "low", "close", "open"))

    asya = (rel >= asya_bas) & (rel < asya_bit)
    gun = rel >= 0
    beklenen_asya = (asya_bit - asya_bas) * 12
    if asya.sum() < 0.9 * beklenen_asya or gun.sum() < 0.9 * beklenen_gun:
        return None  # eksik veri günü

    ah, al = h[asya].max(), l[asya].min()
    r = ah - al
    gun_idx = np.flatnonzero(gun)
    gun_h, gun_l = h[gun], l[gun]
    kayit = {
        "acilis": o[gun_idx[0]],
        "kapanis": c[gun_idx[-1]],
        "yuksek": gun_h.max(),
        "dusuk": gun_l.min(),
        "yuksek_saat": int(rel[gun_idx[np.argmax(gun_h)]]),
        "dusuk_saat": int(rel[gun_idx[np.argmin(gun_l)]]),
        "asya_yuksek": ah,
        "asya_dusuk": al,
    }
    if onceki is not None:
        orta = (onceki["yuksek"] + onceki["dusuk"]) / 2
        kayit["bias"] = "yukari" if onceki["kapanis"] > orta else "asagi"

    man = np.flatnonzero((rel >= man_bas) & (rel < man_bit))
    if r <= 0 or len(man) == 0:
        kayit["supurme"] = "veri_yok"
        return kayit
    # İlk süpürülen taraf belirleyicidir. Diğer tarafın sonradan süpürülmesi bir sonuçtur,
    # sınıflandırmaya katılmaz (aksi halde gelecekteki fiyat bilgisi sızar).
    ust_kirildi = man[h[man] > ah]
    alt_kirildi = man[l[man] < al]
    t_ust = ust_kirildi[0] if len(ust_kirildi) else None
    t_alt = alt_kirildi[0] if len(alt_kirildi) else None
    if t_ust is None and t_alt is None:
        kayit["supurme"] = "yok"
        return kayit
    if t_ust is not None and t_alt is not None and t_ust == t_alt:
        kayit["supurme"] = "ayni_mum"  # iki taraf aynı mumda; sıra bilinemez
        return kayit

    # yon=+1: Asya yükseği önce süpürüldü, beklenen dönüş aşağı.
    if t_alt is None or (t_ust is not None and t_ust < t_alt):
        yon, t, seviye, karsi = 1, t_ust, ah, al
    else:
        yon, t, seviye, karsi = -1, t_alt, al, ah
    kayit["supurme"] = "ust" if yon == 1 else "alt"
    if "bias" in kayit:
        # Yukarı bias'ta beklenen manipülasyon aşağıdır (alt taraf süpürülür)
        kayit["bias_uyumlu"] = (kayit["bias"] == "yukari") == (yon == -1)

    son = len(h)  # yarışlar gün sonuna kadar
    donus_tarafi = "alt" if yon == 1 else "ust"

    # Yarış 1: süpürme mumunun kapanışından, onay beklemeden, simetrik hedeflerle
    p1 = c[t]
    d1 = (p1 - karsi) * yon
    if d1 > 0:
        ust, alt = (p1 + d1, karsi) if yon == 1 else (karsi, p1 - d1)
        sonuc, _ = yaris(h, l, c, t + 1, ust, alt)
        kayit["yaris1"] = {"belirsiz": "belirsiz", "yok": "yok"}.get(
            sonuc, "donus" if sonuc == donus_tarafi else "devam")

    # Karşı tarafa gün sonuna kadar ulaşıldı mı?
    kalan = slice(t, son)
    kayit["karsi_taraf"] = bool((l[kalan] <= al).any() if yon == 1 else (h[kalan] >= ah).any())

    # Yarış 2: seviyenin içine geri kapanış (onay) sonrası, kapanış fiyatından simetrik
    for j in range(t, min(t + GERI_KAPANIS_MUM, son)):
        icinde = c[j] < seviye if yon == 1 else c[j] > seviye
        if icinde:
            break
    else:
        kayit["geri_kapanis"] = False
        return kayit
    p = c[j]
    d = (p - karsi) * yon  # hedefe uzaklık
    if d <= 0:
        kayit["geri_kapanis"] = False
        return kayit
    kayit["geri_kapanis"] = True
    ust, alt = (p + d, karsi) if yon == 1 else (karsi, p - d)
    sonuc, i = yaris(h, l, c, j + 1, ust, alt)
    maliyet_r = maliyet * p / d  # maliyetin R cinsinden karşılığı
    if sonuc == "yok":
        kayit["yaris2"] = "yok"
        brut = (p - c[i]) * yon / d  # gün sonunda zaman çıkışı
    elif sonuc == "belirsiz":
        kayit["yaris2"] = "belirsiz"
        brut = -1.0  # temkinli: zarar sayılır
    else:
        kayit["yaris2"] = "donus" if sonuc == donus_tarafi else "devam"
        brut = 1.0 if kayit["yaris2"] == "donus" else -1.0
    kayit["yaris2_brut_r"] = brut
    kayit["yaris2_net_r"] = brut - maliyet_r
    kayit["yaris2_mesafe_yuzde"] = 100 * d / p
    return kayit


def coin_analiz(coin: str, df: pd.DataFrame) -> pd.DataFrame:
    satirlar = []
    maliyet = gidis_donus_maliyeti(coin)
    for ad, varyant in VARYANTLAR.items():
        onceki = None
        for gun, g, rel, beklenen in gun_dilimleri(df, varyant):
            kayit = gun_olaylari(g, rel, beklenen, varyant, onceki, maliyet)
            if kayit is None:
                onceki = None
                continue
            kayit.update(coin=coin, varyant=ad, gun=gun)
            satirlar.append(kayit)
            onceki = kayit
    return pd.DataFrame(satirlar)


# ---------------------------------------------------------------- raporlama

def oran_satiri(basari: int, n: int) -> str:
    if n == 0:
        return "– | – | –"
    test = binomtest(basari, n, 0.5)
    ga = test.proportion_ci(confidence_level=0.95, method="wilson")
    return f"%{100 * basari / n:.1f} | %{100 * ga.low:.1f}–{100 * ga.high:.1f} | {test.pvalue:.3f}"


def yaris_ozet(df: pd.DataFrame, sutun: str) -> tuple[int, int]:
    s = df[sutun].dropna()
    don, dev = (s == "donus").sum(), (s == "devam").sum()
    return int(don), int(don + dev)


def net_r_satiri(df: pd.DataFrame) -> str:
    r = df["yaris2_net_r"].dropna()
    if len(r) < 2:
        return "– | –"
    se = r.std(ddof=1) / math.sqrt(len(r))
    return f"{r.mean():+.3f} | {r.mean() - 1.96 * se:+.3f} – {r.mean() + 1.96 * se:+.3f}"


def rapor_yaz(olaylar: pd.DataFrame, kapsam: pd.DataFrame) -> str:
    s = []
    s.append("# PO3 İstatistik Ön Çalışması: Sonuçlar\n")
    s.append(f"Veri: Binance USDT-M vadeli, {ARALIK} mumlar. Analiz betiği: `analiz.py`.\n")
    s.append("Tablolardaki **oran** dönüş yüzdesidir; **%95 GA** güven aralığıdır; **p** değeri "
             "%50'den (rastgele) farkın tesadüf olma olasılığıdır (0,05'in altı anlamlı kabul edilir).\n")
    s.append("**Net R**: Yarış 2'yi işlem gibi düşünür (geri kapanışta giriş, stop ve hedef eşit "
             "uzaklıkta, gün sonunda zaman çıkışı). Komisyon, kayma ve fonlama payı düşülmüştür; "
             "aynı mumda iki seviyeye değilen durumlar zarar sayılır. Devam eşiği: +0,15R.\n")
    s.append("Not: Bu bir strateji backtest'i değildir; kural seti v1'deki MSS ve FVG onayları "
             "yoktur. Modelin temel varsayımının veride olup olmadığını ölçer.\n")

    s.append("\n## Veri kapsamı\n")
    s.append("| Coin | Varyant | Gün sayısı | İlk gün | Son gün |\n|---|---|---|---|---|")
    for _, k in kapsam.iterrows():
        s.append(f"| {k.coin} | {k.varyant} | {k.gun_sayisi} | {k.ilk} | {k.son} |")

    for ad in VARYANTLAR:
        v = olaylar[olaylar["varyant"] == ad]
        if v.empty:
            continue
        baslik = "00:00 UTC açılışı" if ad == "utc" else "New York gece yarısı açılışı"
        s.append(f"\n## Varyant: {baslik}\n")

        dag = v["supurme"].value_counts(normalize=True) * 100
        s.append("**Londra penceresinde süpürme dağılımı:** " + ", ".join(
            f"{k} %{dag.get(k, 0):.1f}" for k in ("ust", "alt", "ayni_mum", "yok")) + "\n")
        tek = v[v["supurme"].isin(["ust", "alt"])]
        if not tek.empty:
            s.append(f"**Tek taraf süpürmesinden sonra gün içinde Asya aralığının karşı tarafına "
                     f"ulaşma oranı:** %{100 * tek['karsi_taraf'].mean():.1f} ({len(tek)} gün)\n")

        s.append("\n### Soru 1 ve 3: Süpürme sonrası dönüş mü devam mı?\n")
        s.append("| Ölçüm | Dönüş / toplam | Oran | %95 GA | p |\n|---|---|---|---|---|")
        for etiket, alt_df, sutun in [
            ("Yarış 1: süpürme mumu kapanışından (onaysız)", tek, "yaris1"),
            ("Yarış 2: geri kapanış sonrası (onaylı)", tek, "yaris2"),
            ("Yarış 2, bias ile uyumlu", tek[tek.get("bias_uyumlu") == True], "yaris2"),
            ("Yarış 2, bias'a ters", tek[tek.get("bias_uyumlu") == False], "yaris2"),
        ]:
            if sutun not in alt_df:
                continue
            don, n = yaris_ozet(alt_df, sutun)
            s.append(f"| {etiket} | {don} / {n} | {oran_satiri(don, n)} |")

        s.append("\n### Yarış 2 işlem gibi düşünülürse (maliyetler dahil)\n")
        s.append("| Grup | İşlem | Kazanma | Ort. mesafe | Brüt R | Net R | Net R %95 GA |\n"
                 "|---|---|---|---|---|---|---|")
        y2 = tek.dropna(subset=["yaris2_net_r"]) if "yaris2_net_r" in tek else tek.iloc[0:0]
        gruplar = [("Tümü", y2)] + [(c, y2[y2["coin"] == c]) for c in sorted(y2["coin"].unique())]
        if "bias_uyumlu" in y2:
            gruplar.insert(1, ("Bias uyumlu", y2[y2["bias_uyumlu"] == True]))
        for etiket, gdf in gruplar:
            if gdf.empty:
                continue
            kaz = (gdf["yaris2"] == "donus").mean() * 100
            s.append(f"| {etiket} | {len(gdf)} | %{kaz:.1f} | %{gdf['yaris2_mesafe_yuzde'].mean():.2f} | "
                     f"{gdf['yaris2_brut_r'].mean():+.3f} | {net_r_satiri(gdf)} |")

        if not y2.empty:
            s.append("\n**Yıllara göre (Yarış 2, tüm coinler):**\n")
            s.append("| Yıl | İşlem | Kazanma | Net R |\n|---|---|---|---|")
            yil = pd.to_datetime(y2["gun"]).dt.year
            for y, gdf in y2.groupby(yil):
                s.append(f"| {y} | {len(gdf)} | %{(gdf['yaris2'] == 'donus').mean() * 100:.1f} | "
                         f"{gdf['yaris2_net_r'].mean():+.3f} |")

        s.append("\n### Soru 2: Günün tepesi ve dibi hangi saatte oluşuyor?\n")
        s.append("Saatler günün açılışından itibaren sayılır (0 = açılış saati, yerel saat).\n")
        s.append("| Saat | Tepe % | Dip % |\n|---|---|---|")
        ht = v["yuksek_saat"].value_counts(normalize=True) * 100
        dt = v["dusuk_saat"].value_counts(normalize=True) * 100
        for saat in range(24):
            s.append(f"| {saat:02d} | {ht.get(saat, 0):.1f} | {dt.get(saat, 0):.1f} |")

        s.append("\n### Soru 4: Bias kuralı günün yönünü tahmin ediyor mu?\n")
        b = v.dropna(subset=["bias"])
        dogru = int((((b["kapanis"] > b["acilis"]) & (b["bias"] == "yukari")) |
                     ((b["kapanis"] < b["acilis"]) & (b["bias"] == "asagi"))).sum())
        s.append("| Doğru / toplam | Oran | %95 GA | p |\n|---|---|---|---|")
        s.append(f"| {dogru} / {len(b)} | {oran_satiri(dogru, len(b))} |")
    return "\n".join(s) + "\n"


def main(veri_klasoru: Path = VERI_KLASORU, cikti: Path = CIKTI) -> None:
    dosyalar = sorted(veri_klasoru.glob(f"*-{ARALIK}.parquet"))
    if not dosyalar:
        raise SystemExit(f"{veri_klasoru} altında veri yok. Önce veri_indir.py çalıştırılmalı.")
    parcalar = []
    for dosya in dosyalar:
        coin = dosya.name.split("USDT")[0]
        df = pd.read_parquet(dosya)
        parcalar.append(coin_analiz(coin, df))
        print(f"{coin}: tamam")
    olaylar = pd.concat(parcalar, ignore_index=True)
    kapsam = (olaylar.groupby(["coin", "varyant"])["gun"]
              .agg(gun_sayisi="count", ilk="min", son="max").reset_index())
    cikti.mkdir(parents=True, exist_ok=True)
    olaylar.to_csv(cikti / "gunluk_olaylar.csv", index=False)
    (cikti / "rapor.md").write_text(rapor_yaz(olaylar, kapsam), encoding="utf-8")
    print(f"Rapor: {cikti / 'rapor.md'}")


if __name__ == "__main__":
    main()
