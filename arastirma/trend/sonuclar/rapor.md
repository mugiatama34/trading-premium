# Trend Takibi Modeli: Sonuçlar

Kod ve kurallar: `trend.py` (dosyanın başında). Veri: Binance USDT-M vadeli, 5 dk mumlardan üretilen günlük mumlar (00:00 UTC) ve gerçek fonlama oranları, 17 coin, 2021-01 → 2026-09.

Maliyetler: giriş ve çıkış piyasa emri (taker %0,05 + coin bazında kayma %0,01–0,05), gerçek fonlama. Komisyon oranı doğrulanmadı.

Örneklem içi: 2021-01 → 2024-06-01. Örneklem dışı: sonrası → 2026-09. Bu dönem trend modeli için ilk kez kullanıldı.


## Seçilen aday: N=20, stop 3×ATR, yalnızca uzun

Seçim yalnızca örneklem içi sonuçlara göre yapıldı (16 uygun aday arasında en yüksek net R).

| Grup | İşlem | Kazanma | Brüt R | Net R | Net R %95 GA | PF | Medyan stop | En uzun kayıp serisi |
|---|---|---|---|---|---|---|---|---|
| Örneklem içi | 239 | %38.5 | +0.621 | +0.536 | +0.191 – +0.882 | 2.25 | %17.27 | 17 |
| Örneklem dışı | 202 | %37.1 | +0.305 | +0.272 | -0.041 – +0.585 | 1.63 | %16.37 | 36 |
| Örneklem dışı, uzun | 202 | %37.1 | +0.305 | +0.272 | -0.041 – +0.585 | 1.63 | %16.37 | 36 |

**Örneklem dışı, devam eşikleri:**

| Ölçüt | Eşik | Sonuç | Durum |
|---|---|---|---|
| İşlem sayısı | ≥ 100 | 202 | Geçti |
| Net beklenti | ≥ +0,15R | +0.272R | Geçti |
| Profit factor | ≥ 1,3 | 1.63 | Geçti |
| Maks. düşüş (%1 risk) | ≤ %20 | %10.3 | Geçti |
| Rastgele kıyastan iyi | p < 0,05 | p = 0.045 | Geçti |

Rastgele yönlü kıyas (aynı giriş günü, aynı stop kuralı, 20 tohum): ortalama net R +0.084 (tohumlar -0.075 … +0.264); model +0.272.


Örneklem dışında ortalama kazanç +1.89R, ortalama kayıp -0.68R. Pozisyon süresi medyan 16 gün. İşlem başına maliyet 0.033R (fonlama +0.022R). Veri sonunda açık kalan: 16.


**Açık pozisyonlara dikkat:** Örneklem dışındaki net R'nin önemli bir kısmı veri sonunda hâlâ açık pozisyonlardan geliyor (son kapanıştan değerlendi). Açık pozisyonlar iz süren stoplarından kapansaydı ortalama net R +0.184, PF 1.41 olurdu. Yalnızca kapanmış 186 işlemin ortalaması +0.133R.


**Portföy (10.000 $ başlangıç, aynı yönde en fazla %3 açık risk):**

| Dönem | Risk/işlem | Alınan işlem | Atlanan | Son sermaye | Yıllık getiri | Maks. düşüş |
|---|---|---|---|---|---|---|
| Örneklem içi | %1 | 82 | 157 | 14,741 $ | %12.0 | %11.4 |
| Örneklem içi | %2 | 28 | 211 | 12,066 $ | %5.7 | %12.2 |
| Örneklem dışı | %1 | 55 | 147 | 11,556 $ | %6.4 | %10.3 |
| Örneklem dışı | %2 | 20 | 182 | 11,887 $ | %7.7 | %8.9 |

Monte Carlo (örneklem dışı, %1 risk, sınırsız sıralı): medyan maks. düşüş %11.8, %95 kötü durumda %18.2.


Pozisyon büyüklüğü / sermaye: %1 riskte medyan 0.1x, %90'lık 0.1x, en yüksek 0.2x; %2 riskte medyan 0.1x, %90'lık 0.2x, en yüksek 0.5x.


**Yıllara göre (tüm dönem, giriş yılına göre):**

| Yıl | İşlem | Kazanma | Net R | PF |
|---|---|---|---|---|
| 2021 | 70 | %51.4 | +1.146 | 4.67 |
| 2022 | 54 | %20.4 | -0.356 | 0.34 |
| 2023 | 73 | %42.5 | +0.932 | 3.31 |
| 2024 | 97 | %32.0 | +0.416 | 1.86 |
| 2025 | 64 | %43.8 | +0.095 | 1.25 |
| 2026 | 83 | %36.1 | +0.094 | 1.21 |

**Coinlere göre (örneklem dışı):**

| Grup | İşlem | Kazanma | Brüt R | Net R | Net R %95 GA | PF | Medyan stop | En uzun kayıp serisi |
|---|---|---|---|---|---|---|---|---|
| ADA | 13 | %30.8 | +0.132 | +0.097 | -1.160 – +1.355 | 1.17 | %16.59 | 4 |
| AVAX | 12 | %33.3 | +0.201 | +0.171 | -0.644 – +0.986 | 1.40 | %16.80 | 3 |
| BNB | 12 | %50.0 | +0.436 | +0.387 | -0.514 – +1.288 | 2.35 | %10.62 | 4 |
| BTC | 13 | %38.5 | +0.273 | +0.206 | -0.617 – +1.029 | 1.52 | %9.83 | 4 |
| CRV | 12 | %41.7 | +0.884 | +0.852 | -1.318 – +3.022 | 2.97 | %19.10 | 2 |
| DOGE | 12 | %50.0 | +0.329 | +0.294 | -0.355 – +0.942 | 2.14 | %15.64 | 2 |
| DOT | 12 | %25.0 | -0.408 | -0.428 | -0.751 – -0.104 | 0.19 | %16.14 | 8 |
| ETH | 12 | %33.3 | +0.195 | +0.149 | -0.779 – +1.076 | 1.27 | %13.14 | 6 |
| ETHFI | 13 | %15.4 | -0.062 | -0.081 | -0.927 – +0.764 | 0.86 | %23.75 | 7 |
| LINK | 17 | %29.4 | -0.146 | -0.178 | -0.730 – +0.374 | 0.67 | %17.21 | 4 |
| LTC | 12 | %41.7 | +0.128 | +0.078 | -0.577 – +0.733 | 1.19 | %12.37 | 5 |
| MMT | 6 | %33.3 | -0.478 | -0.462 | -1.027 – +0.104 | 0.24 | %20.79 | 3 |
| NEAR | 13 | %30.8 | +0.484 | +0.458 | -0.732 – +1.648 | 2.21 | %18.81 | 5 |
| PENGU | 8 | %50.0 | +0.480 | +0.480 | -0.723 – +1.684 | 2.46 | %19.94 | 2 |
| SOL | 12 | %41.7 | +0.183 | +0.148 | -0.472 – +0.768 | 1.50 | %16.18 | 3 |
| SUI | 11 | %54.5 | +0.615 | +0.589 | -0.249 – +1.428 | 3.13 | %18.91 | 4 |
| XRP | 12 | %41.7 | +1.858 | +1.819 | -1.810 – +5.447 | 5.95 | %13.06 | 3 |

## Tüm adaylar (örneklem içi sıralı)

Örneklem dışı sütunları seçimde kullanılmadı. Portföy sütunları %1 risk ve %3 toplam risk sınırıyla.

| Aday | İçi işlem | İçi net R | İçi PF | İçi maks. düşüş | Dışı işlem | Dışı net R | Dışı PF | Dışı yıllık | Dışı maks. düşüş |
|---|---|---|---|---|---|---|---|---|---|
| N=20, stop 3×ATR, yalnızca uzun **(seçilen)** | 239 | +0.536 | 2.25 | %11.4 | 202 | +0.272 | 1.63 | %6.4 | %10.3 |
| N=20, stop 2×ATR, yalnızca uzun | 328 | +0.438 | 1.91 | %11.2 | 250 | +0.301 | 1.68 | %7.6 | %12.8 |
| N=20, stop 4×ATR, yalnızca uzun | 198 | +0.426 | 1.98 | %10.5 | 159 | +0.283 | 1.69 | %5.1 | %7.9 |
| N=50, stop 3×ATR, yalnızca uzun | 151 | +0.352 | 1.74 | %5.5 | 121 | +0.310 | 1.66 | %-0.8 | %11.3 |
| N=20, stop 3×ATR, iki yön | 366 | +0.345 | 1.88 | %10.7 | 331 | +0.176 | 1.46 | %7.3 | %9.4 |
| N=50, stop 2×ATR, yalnızca uzun | 202 | +0.276 | 1.53 | %9.8 | 151 | +0.272 | 1.58 | %7.1 | %8.5 |
| N=20, stop 2×ATR, iki yön | 535 | +0.265 | 1.58 | %9.4 | 481 | +0.116 | 1.26 | %9.2 | %13.7 |
| N=50, stop 3×ATR, iki yön | 254 | +0.229 | 1.54 | %6.1 | 227 | +0.168 | 1.43 | %-0.2 | %10.0 |
| N=20, stop 4×ATR, iki yön | 281 | +0.224 | 1.58 | %13.2 | 226 | +0.228 | 1.63 | %5.1 | %7.1 |
| N=50, stop 4×ATR, yalnızca uzun | 128 | +0.199 | 1.41 | %8.1 | 103 | +0.291 | 1.63 | %4.8 | %8.2 |
| N=50, stop 2×ATR, iki yön | 324 | +0.171 | 1.34 | %8.6 | 279 | +0.150 | 1.35 | %6.6 | %10.4 |
| N=100, stop 2×ATR, yalnızca uzun | 126 | +0.119 | 1.23 | %9.7 | 89 | +0.387 | 1.79 | %2.5 | %10.7 |
| N=50, stop 4×ATR, iki yön | 213 | +0.117 | 1.29 | %8.9 | 187 | +0.156 | 1.41 | %2.9 | %6.8 |
| N=100, stop 3×ATR, yalnızca uzun | 99 | +0.112 | 1.21 | %7.8 | 65 | +0.616 | 2.67 | %4.2 | %6.3 |
| N=100, stop 3×ATR, iki yön | 157 | +0.081 | 1.18 | %5.8 | 133 | +0.261 | 1.79 | %4.0 | %6.3 |
| N=100, stop 2×ATR, iki yön | 193 | +0.069 | 1.14 | %10.4 | 165 | +0.195 | 1.44 | %2.0 | %9.2 |
| N=100, stop 4×ATR, yalnızca uzun | 85 | -0.055 | 0.90 | %8.7 | 55 | +0.595 | 2.75 | %6.3 | %3.9 |
| N=100, stop 4×ATR, iki yön | 143 | -0.079 | 0.83 | %9.2 | 117 | +0.234 | 1.75 | %6.7 | %4.0 |

18 adaydan örneklem dışında net R'si pozitif olan: 18.

