"""PO3 kural seti v1 parametreleri. Kuralların yazılı hali: ../po3-kural-seti-v1.md

Saatler, günün açılışından itibaren yerel saat cinsindendir (negatif = önceki akşam).
"""

import sys
from dataclasses import dataclass, replace
from pathlib import Path

KLASOR = Path(__file__).parent
ISTATISTIK = KLASOR.parent / "po3-istatistik"
sys.path.insert(0, str(ISTATISTIK))  # coin listesi, kayma tablosu ve veri okuma oradan

from ayarlar import COINLER, KAYMA, VARSAYILAN_KAYMA, VERI_KLASORU  # noqa: E402

FONLAMA_KLASORU = VERI_KLASORU / "fonlama"

# Maliyetler (tek yön, fiyatın yüzdesi). Binance USDT-M standart seviye; güncel oran doğrulanmalı.
MAKER = 0.02  # limit giriş ve limit hedef
TAKER = 0.05  # stop ve zaman çıkışı (piyasa emri)

SERMAYE = 10_000
TOPLAM_RISK_SINIRI = 3.0  # aynı yöndeki açık pozisyonların toplam riski, sermayenin yüzdesi
ORNEKLEM_DISI_BASLANGIC = "2024-06-01"  # verinin ilk ~%60'ı geliştirme, sonrası test


@dataclass(frozen=True)
class Kurallar:
    ad: str
    saat_dilimi: str
    asya: tuple[float, float]  # Asya aralığı (birikim)
    manipulasyon: tuple[float, float]  # süpürmenin başlaması gereken pencere
    mss_son: float  # MSS bu saatten önce kapanmalı
    cikis: float  # zaman çıkışı
    geri_kapanis_mum: int = 3  # süpürmeden sonra seviyenin içine kapanış için en fazla mum (N)
    fvg_bekleme_mum: int = 12  # FVG limit emri en fazla bu kadar mum bekler (X), sonra iptal
    stop_tampon_atr: float = 0.1
    hedef: str = "asya"  # "asya" = Asya aralığının karşı tarafı, "2R" / "1.5R" / "3R" = sabit R katı
    bias: bool = True  # False: bias filtresi yok, ilk süpürülen taraf işlenir
    pivot: int = 2  # kısa vadeli tepe/dip: her iki yanında bu kadar mum daha alçak/yüksek
    # v2: stop mesafesi fiyatın bu yüzdesinden kısaysa "filtre" işlemi atlar, "genislet" stopu bu
    # mesafeye uzatır, "yok" (v1) bir şey yapmaz
    min_stop_yuzde: float = 0.0
    min_stop_modu: str = "yok"


UTC = Kurallar("utc", "UTC", asya=(0, 6), manipulasyon=(6, 10), mss_son=12, cikis=20)
NY = Kurallar("ny", "America/New_York", asya=(-4, 0), manipulasyon=(2, 5), mss_son=7, cikis=16)
TEMEL = {"utc": UTC, "ny": NY}


def kayma(coin: str) -> float:
    return KAYMA.get(coin, VARSAYILAN_KAYMA)


def degistir(k: Kurallar, **alanlar) -> Kurallar:
    return replace(k, **alanlar)
