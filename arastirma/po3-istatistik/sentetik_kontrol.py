"""Analizin doğruluk kontrolü: rastgele yürüyüş (random walk) verisinde dönüş oranı ~%50 çıkmalı.

Rastgele veride hiçbir avantaj yoktur. Analiz burada %50'den belirgin şekilde farklı bir
oran bulursa, ölçüm yönteminde hata (ör. geleceğe bakma) var demektir.
Kullanım:  python sentetik_kontrol.py
"""

import numpy as np
import pandas as pd
from scipy.stats import binomtest

import analiz


def rastgele_veri(gun: int, tohum: int) -> pd.DataFrame:
    rng = np.random.default_rng(tohum)
    n = 288 * gun
    kapanis = 100 * np.exp(np.cumsum(rng.normal(0, 0.0015, n)))
    acilis = np.r_[100, kapanis[:-1]]
    fitil = np.abs(rng.normal(0, 0.0007, (n, 2)))
    return pd.DataFrame({
        "ts": pd.date_range("2020-01-01", periods=n, freq="5min", tz="UTC"),
        "open": acilis,
        "high": np.maximum(acilis, kapanis) * (1 + fitil[:, 0]),
        "low": np.minimum(acilis, kapanis) * (1 - fitil[:, 1]),
        "close": kapanis,
    })


if __name__ == "__main__":
    olaylar = pd.concat([analiz.coin_analiz("BTC", rastgele_veri(2000, t)) for t in range(3)])
    hata = False
    for varyant in analiz.VARYANTLAR:
        v = olaylar[olaylar["varyant"] == varyant]
        for sutun in ("yaris1", "yaris2"):
            don, n = analiz.yaris_ozet(v, sutun)
            p = binomtest(don, n, 0.5).pvalue
            print(f"{varyant} {sutun}: dönüş %{100 * don / n:.1f} ({n} olay), p={p:.3f}")
            hata |= p < 0.01
        print(f"{varyant} yaris2 brüt R ortalaması: {v['yaris2_brut_r'].mean():+.3f} (≈0 olmalı)")
    print("SONUÇ:", "ŞÜPHELİ, ölçüm yöntemini kontrol et" if hata else "geçti")
