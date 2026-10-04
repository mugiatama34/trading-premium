"""Eğitim örnekleri için Binance herkese açık veri arşivinden (data.binance.vision)
USDT-M vadeli 1 saatlik mumları indirir ve okur.

API anahtarı gerektirmez, borsaya bağlanmaz; yalnızca geçmiş veri dosyalarını indirir.
Yalnızca Python standart kütüphanesi kullanılır.
"""

import io
import urllib.error
import urllib.request
import zipfile
from datetime import date, datetime, timezone
from pathlib import Path

ARSIV = "https://data.binance.vision/data/futures/um/monthly/klines"
VERI_KLASORU = Path(__file__).parent / "veri"


class Mum:
    __slots__ = ("t", "o", "h", "l", "c")

    def __init__(self, t, o, h, l, c):
        self.t, self.o, self.h, self.l, self.c = t, o, h, l, c

    @property
    def zaman(self):
        return datetime.fromtimestamp(self.t / 1000, tz=timezone.utc)


def aylar(baslangic, bitis=None):
    """'YYYY-MM' biçiminde ay listesi; bitiş verilmezse son tamamlanmış aya kadar."""
    yil, ay = map(int, baslangic.split("-"))
    if bitis:
        by, ba = map(int, bitis.split("-"))
    else:
        bugun = date.today()
        by, ba = bugun.year, bugun.month - 1
        if ba == 0:
            by, ba = by - 1, 12
    while (yil, ay) <= (by, ba):
        yield f"{yil:04d}-{ay:02d}"
        ay += 1
        if ay > 12:
            yil, ay = yil + 1, 1


def _ay_oku(sembol, aralik, ay):
    ad = f"{sembol}-{aralik}-{ay}.zip"
    onbellek = VERI_KLASORU / ad  # indirilen aylar tekrar indirilmez
    if onbellek.exists():
        icerik = onbellek.read_bytes()
    else:
        try:
            with urllib.request.urlopen(f"{ARSIV}/{sembol}/{aralik}/{ad}", timeout=60) as yanit:
                icerik = yanit.read()
        except urllib.error.HTTPError as hata:
            if hata.code == 404:
                return []
            raise
        onbellek.parent.mkdir(parents=True, exist_ok=True)
        onbellek.write_bytes(icerik)
    with zipfile.ZipFile(io.BytesIO(icerik)) as z:
        satirlar = z.read(z.namelist()[0]).decode().splitlines()
    mumlar = []
    for satir in satirlar:
        p = satir.split(",")
        if not p[0].isdigit():  # yeni dosyalarda başlık satırı var
            continue
        mumlar.append(Mum(int(p[0]), float(p[1]), float(p[2]), float(p[3]), float(p[4])))
    return mumlar


def mumlar(sembol, baslangic, bitis=None, aralik="1h"):
    sonuc = []
    for ay in aylar(baslangic, bitis):
        sonuc.extend(_ay_oku(sembol, aralik, ay))
    return sonuc
