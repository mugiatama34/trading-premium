"""Binance herkese açık veri arşivinden (data.binance.vision) USDT-M vadeli geçmiş fonlama oranlarını indirir.

API anahtarı gerektirmez, borsaya bağlanmaz. Aylık zip dosyaları ../po3-istatistik/veri/fonlama altına yazılır.
5 dakikalık mumlar için: ../po3-istatistik/veri_indir.py
Kullanım:  python fonlama_indir.py            (tüm coin listesi)
           python fonlama_indir.py BTC ETH    (yalnızca seçilen coinler)
"""

import sys
import urllib.error
import urllib.request

from datetime import date

from kurallar import COINLER, FONLAMA_KLASORU
from ayarlar import BASLANGIC

ARSIV = "https://data.binance.vision/data/futures/um/monthly/fundingRate"


def aylar(baslangic: str):
    """Başlangıç ayından son tamamlanmış aya kadar 'YYYY-MM' listesi."""
    yil, ay = map(int, baslangic.split("-"))
    bugun = date.today()
    while (yil, ay) < (bugun.year, bugun.month):
        yield f"{yil:04d}-{ay:02d}"
        ay += 1
        if ay > 12:
            yil, ay = yil + 1, 1


def coin_indir(coin: str) -> None:
    sembol = f"{coin}USDT"
    adet = 0
    for ay in aylar(BASLANGIC):
        ad = f"{sembol}-fundingRate-{ay}.zip"
        hedef = FONLAMA_KLASORU / ad
        if hedef.exists():
            adet += 1
            continue
        try:
            with urllib.request.urlopen(f"{ARSIV}/{sembol}/{ad}", timeout=60) as yanit:
                hedef.write_bytes(yanit.read())
            adet += 1
        except urllib.error.HTTPError as hata:
            if hata.code != 404:  # 404: coin o ay henüz listelenmemiş
                raise
    print(f"{sembol}: {adet} aylık fonlama dosyası")


if __name__ == "__main__":
    FONLAMA_KLASORU.mkdir(parents=True, exist_ok=True)
    for coin in sys.argv[1:] or COINLER:
        coin_indir(coin.upper())
