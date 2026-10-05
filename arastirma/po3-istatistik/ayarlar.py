"""PO3 istatistik çalışmasının ortak ayarları. Kararlar: context/kararlar.md (2026-10-03)."""

from pathlib import Path

KLASOR = Path(__file__).parent
VERI_KLASORU = KLASOR / "veri"  # indirilen ham veri; depoya eklenmez (.gitignore)

COINLER = [
    "BTC", "ETH", "SOL", "ADA", "LINK", "ETHFI", "DOGE", "PENGU", "MMT",
    "AVAX", "DOT", "LTC", "CRV", "BNB", "NEAR", "XRP", "SUI",
]
ARALIK = "5m"
BASLANGIC = "2021-01"  # yeni coinler listelendikleri aydan başlar

# Seans tanımları: (başlangıç saati, bitiş saati) yerel saatle.
# "utc": kripto günlük mumu, gün 00:00 UTC'de açılır.
# "ny":  ICT tanımı, gün New York gece yarısı açılır (yaz/kış saati dahil);
#        Asya aralığı önceki akşam 20:00-24:00, Londra kill zone 02:00-05:00.
VARYANTLAR = {
    "utc": {"saat_dilimi": "UTC", "asya": (0, 6), "manipulasyon": (6, 10)},
    "ny": {"saat_dilimi": "America/New_York", "asya": (-4, 0), "manipulasyon": (2, 5)},
}

# Süpürmeden sonra seviyenin içine geri kapanış için beklenen en fazla mum sayısı
GERI_KAPANIS_MUM = 3

# Maliyet varsayımları (tek yön, fiyatın yüzdesi). Komisyon oranı doğrulanmalı.
KOMISYON = 0.05  # Binance USDT-M taker, standart seviye
FONLAMA = 0.01  # gün içi işlemde ortalama fonlama payı (işlem başına)
KAYMA = {  # coin likiditesine göre tek yön kayma
    "BTC": 0.01, "ETH": 0.01, "BNB": 0.02, "SOL": 0.02, "XRP": 0.02,
    "ETHFI": 0.05, "PENGU": 0.05, "MMT": 0.05, "CRV": 0.05,
}
VARSAYILAN_KAYMA = 0.03


def gidis_donus_maliyeti(coin: str) -> float:
    """Bir giriş + çıkışın toplam maliyeti, fiyatın oranı olarak (ör. 0.0013 = %0,13)."""
    kayma = KAYMA.get(coin, VARSAYILAN_KAYMA)
    return (2 * KOMISYON + 2 * kayma + FONLAMA) / 100
