"""Binance herkese açık veri arşivinden (data.binance.vision) USDT-M vadeli 5 dakikalık mumları indirir.

API anahtarı gerektirmez, borsaya bağlanmaz; yalnızca geçmiş veri dosyalarını indirir.
Kullanım:  python veri_indir.py            (tüm coin listesi)
           python veri_indir.py BTC ETH    (yalnızca seçilen coinler)
"""

import io
import sys
import urllib.error
import urllib.request
import zipfile
from datetime import date

import pandas as pd

from ayarlar import ARALIK, BASLANGIC, COINLER, VERI_KLASORU

ARSIV = "https://data.binance.vision/data/futures/um/monthly/klines"
SUTUNLAR = ["open_time", "open", "high", "low", "close", "volume"]


def aylar(baslangic: str):
    """Başlangıç ayından son tamamlanmış aya kadar 'YYYY-MM' listesi."""
    yil, ay = map(int, baslangic.split("-"))
    bugun = date.today()
    while (yil, ay) < (bugun.year, bugun.month):
        yield f"{yil:04d}-{ay:02d}"
        ay += 1
        if ay > 12:
            yil, ay = yil + 1, 1


def ay_indir(sembol: str, ay: str) -> pd.DataFrame | None:
    ad = f"{sembol}-{ARALIK}-{ay}.zip"
    onbellek = VERI_KLASORU / "ham" / ad  # daha önce indirilen aylar tekrar indirilmez
    if onbellek.exists():
        icerik = onbellek.read_bytes()
    elif onbellek.with_name(ad + ".404").exists():
        return None
    else:
        try:
            with urllib.request.urlopen(f"{ARSIV}/{sembol}/{ARALIK}/{ad}", timeout=60) as yanit:
                icerik = yanit.read()
        except urllib.error.HTTPError as hata:
            if hata.code == 404:  # coin o ay henüz listelenmemiş
                return None
            raise
        onbellek.parent.mkdir(parents=True, exist_ok=True)
        onbellek.write_bytes(icerik)
    with zipfile.ZipFile(io.BytesIO(icerik)) as z:
        ham = z.read(z.namelist()[0]).decode()
    # Yeni dosyalarda başlık satırı var, eskilerde yok
    ilk = ham.splitlines()[0]
    baslik = 0 if ilk.startswith("open_time") else None
    df = pd.read_csv(io.StringIO(ham), header=baslik, usecols=range(6))
    df.columns = SUTUNLAR
    return df


def coin_indir(coin: str) -> None:
    sembol = f"{coin}USDT"
    hedef = VERI_KLASORU / f"{sembol}-{ARALIK}.parquet"
    parcalar = []
    for ay in aylar(BASLANGIC):
        df = ay_indir(sembol, ay)
        if df is not None:
            parcalar.append(df)
    if not parcalar:
        print(f"{sembol}: arşivde veri bulunamadı (vadeli kontratı olmayabilir)")
        return
    df = pd.concat(parcalar, ignore_index=True)
    # Zaman damgası milisaniye; bazı yeni dosyalar mikrosaniye olabilir
    birim = "us" if df["open_time"].max() > 1e14 else "ms"
    df["ts"] = pd.to_datetime(df["open_time"], unit=birim, utc=True)
    df = df.drop(columns="open_time").drop_duplicates("ts").sort_values("ts")
    df.to_parquet(hedef, index=False)
    print(f"{sembol}: {len(df):,} mum, {df['ts'].min():%Y-%m-%d} → {df['ts'].max():%Y-%m-%d}")


if __name__ == "__main__":
    VERI_KLASORU.mkdir(parents=True, exist_ok=True)
    for coin in sys.argv[1:] or COINLER:
        coin_indir(coin.upper())
