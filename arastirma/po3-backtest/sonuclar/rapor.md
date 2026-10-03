# PO3 Kural Seti v1 Backtesti: Sonuçlar

Kurallar: [../../po3-kural-seti-v1.md](../../po3-kural-seti-v1.md). Kod: `backtest.py`, parametreler: `kurallar.py`.

Veri: Binance USDT-M vadeli 5 dk mumlar ve geçmiş fonlama oranları, 17 coin, 2021-01-01 → 2026-09-30. Örneklem dışı (test) dönemi: 2024-06-01 sonrası.

Maliyetler: giriş ve hedef limit emir (maker %0.02), stop ve zaman çıkışı piyasa emri (taker %0.05 + coin bazında kayma %0,01–0,05), gerçek geçmiş fonlama oranları. Tüm R değerleri **net R** sütunlarında maliyetler düşülmüş haldedir.


## 00:00 UTC açılışı, hedef: Asya aralığının karşı tarafı

Huni: 21733 hafta içi gün → 8686 bias yönünde süpürme → 5919 geri kapanış → 2770 MSS → 2630 FVG → 810 dolan limit emir.

| Grup | İşlem | Kazanma | Brüt R | Net R | Net R %95 GA | PF | Medyan stop | En uzun kayıp serisi |
|---|---|---|---|---|---|---|---|---|
| Tümü | 810 | %23.5 | -0.067 | -0.222 | -0.356 – -0.088 | 0.75 | %0.66 | 17 |
| Örneklem içi | 443 | %22.1 | -0.179 | -0.324 | -0.487 – -0.160 | 0.64 | %0.72 | 16 |
| Örneklem dışı | 367 | %25.1 | +0.068 | -0.099 | -0.320 – +0.122 | 0.89 | %0.59 | 17 |
| Uzun | 391 | %25.1 | -0.037 | -0.188 | -0.381 – +0.005 | 0.79 | %0.70 | 23 |
| Kısa | 419 | %22.0 | -0.095 | -0.254 | -0.441 – -0.066 | 0.72 | %0.64 | 16 |

**Örneklem dışı, devam eşikleri:**

| Ölçüt | Eşik | Sonuç | Durum |
|---|---|---|---|
| İşlem sayısı | ≥ 100 | 367 | Geçti |
| Net beklenti | ≥ +0,15R | -0.099R | Geçmedi |
| Profit factor | ≥ 1,3 | 0.89 | Geçmedi |
| Maks. düşüş (%1 risk) | ≤ %20 | %55.7 | Geçmedi |
| Rastgele kıyastan iyi | p < 0,05 | p = 0.172 | Geçmedi |

Rastgele yönlü kıyas (aynı giriş anı, stop ve hedef, 20 tohum): ortalama net R -0.183 (tohumlar -0.364 … -0.057); model -0.099.


Sonuç dağılımı: hedef %20.6, stop %75.7, zaman %3.7. Ortalama kazanç +2.88R, ortalama kayıp -1.17R. Maliyetlerin brüt kâra oranı %22; fonlamanın payı işlem başına +0.0000R.


**Portföy (tüm dönem, 10.000 $ başlangıç, aynı yönde en fazla %3 açık risk):**

| Risk/işlem | Alınan işlem | Sınır yüzünden atlanan | Son sermaye | Yıllık getiri | Maks. düşüş |
|---|---|---|---|---|---|
| %1 | 772 | 38 | 1,393 $ | %-29.0 | %91.0 |
| %2 | 569 | 241 | 489 $ | %-40.9 | %97.5 |

Monte Carlo (işlem sırası 1000 kez karıştırıldı, %1 risk): medyan maks. düşüş %87.3, %95 kötü durumda %89.7.


Gereken kaldıraç (pozisyon / sermaye): %1 riskte medyan 1.5x, %90'lık 3.3x, en yüksek 9.4x; %2 riskte medyan 3.0x, %90'lık 6.7x, en yüksek 18.7x.


**Yıllara göre:**

| Yıl | İşlem | Kazanma | Net R | PF |
|---|---|---|---|---|
| 2021 | 140 | %20.7 | -0.295 | 0.66 |
| 2022 | 132 | %22.0 | -0.337 | 0.63 |
| 2023 | 128 | %21.1 | -0.447 | 0.54 |
| 2024 | 125 | %25.6 | -0.191 | 0.78 |
| 2025 | 184 | %23.4 | -0.140 | 0.85 |
| 2026 | 101 | %29.7 | +0.128 | 1.16 |

**Coinlere göre:**

| Grup | İşlem | Kazanma | Brüt R | Net R | Net R %95 GA | PF | Medyan stop | En uzun kayıp serisi |
|---|---|---|---|---|---|---|---|---|
| ADA | 59 | %27.1 | +0.078 | -0.083 | -0.625 – +0.459 | 0.90 | %0.64 | 7 |
| AVAX | 65 | %16.9 | -0.371 | -0.512 | -0.886 – -0.137 | 0.47 | %0.73 | 16 |
| BNB | 53 | %26.4 | -0.009 | -0.243 | -0.812 – +0.325 | 0.74 | %0.38 | 10 |
| BTC | 60 | %16.7 | -0.426 | -0.651 | -1.020 – -0.282 | 0.37 | %0.43 | 10 |
| CRV | 49 | %26.5 | -0.118 | -0.203 | -0.666 – +0.259 | 0.74 | %1.30 | 10 |
| DOGE | 58 | %10.3 | -0.399 | -0.563 | -1.039 – -0.087 | 0.46 | %0.58 | 32 |
| DOT | 56 | %25.0 | -0.117 | -0.265 | -0.718 – +0.188 | 0.70 | %0.66 | 10 |
| ETH | 53 | %32.1 | +0.279 | +0.128 | -0.431 – +0.687 | 1.16 | %0.60 | 6 |
| ETHFI | 32 | %18.8 | -0.458 | -0.596 | -1.035 – -0.158 | 0.37 | %0.90 | 16 |
| LINK | 73 | %19.2 | -0.111 | -0.268 | -0.734 – +0.199 | 0.72 | %0.63 | 11 |
| LTC | 49 | %20.4 | -0.185 | -0.376 | -0.927 – +0.176 | 0.61 | %0.52 | 9 |
| MMT | 8 | %37.5 | +0.490 | +0.378 | -1.332 – +2.089 | 1.53 | %1.17 | 4 |
| NEAR | 46 | %32.6 | +0.516 | +0.424 | -0.337 – +1.185 | 1.58 | %1.10 | 13 |
| PENGU | 15 | %46.7 | +0.877 | +0.761 | -0.368 – +1.891 | 2.21 | %0.84 | 3 |
| SOL | 48 | %22.9 | -0.155 | -0.297 | -0.791 – +0.197 | 0.67 | %0.63 | 10 |
| SUI | 40 | %35.0 | +0.451 | +0.331 | -0.458 – +1.120 | 1.45 | %0.69 | 6 |
| XRP | 46 | %19.6 | -0.169 | -0.322 | -0.845 – +0.202 | 0.65 | %0.61 | 11 |

## 00:00 UTC açılışı, hedef: sabit 2R

Huni: 21733 hafta içi gün → 8686 bias yönünde süpürme → 5919 geri kapanış → 2770 MSS → 2630 FVG → 713 dolan limit emir.

| Grup | İşlem | Kazanma | Brüt R | Net R | Net R %95 GA | PF | Medyan stop | En uzun kayıp serisi |
|---|---|---|---|---|---|---|---|---|
| Tümü | 713 | %34.8 | +0.032 | -0.095 | -0.202 – +0.012 | 0.87 | %0.71 | 13 |
| Örneklem içi | 390 | %33.3 | -0.007 | -0.124 | -0.267 – +0.019 | 0.84 | %0.79 | 13 |
| Örneklem dışı | 323 | %36.5 | +0.080 | -0.060 | -0.220 – +0.101 | 0.92 | %0.64 | 13 |
| Uzun | 358 | %36.3 | +0.092 | -0.035 | -0.188 – +0.118 | 0.95 | %0.72 | 19 |
| Kısa | 355 | %33.2 | -0.028 | -0.155 | -0.304 – -0.007 | 0.80 | %0.69 | 12 |

**Örneklem dışı, devam eşikleri:**

| Ölçüt | Eşik | Sonuç | Durum |
|---|---|---|---|
| İşlem sayısı | ≥ 100 | 323 | Geçti |
| Net beklenti | ≥ +0,15R | -0.060R | Geçmedi |
| Profit factor | ≥ 1,3 | 0.92 | Geçmedi |
| Maks. düşüş (%1 risk) | ≤ %20 | %36.6 | Geçmedi |
| Rastgele kıyastan iyi | p < 0,05 | p = 0.049 | Geçti |

Rastgele yönlü kıyas (aynı giriş anı, stop ve hedef, 20 tohum): ortalama net R -0.175 (tohumlar -0.317 … -0.064); model -0.060.


Sonuç dağılımı: hedef %33.2, stop %64.2, zaman %2.5. Ortalama kazanç +1.88R, ortalama kayıp -1.15R. Maliyetlerin brüt kâra oranı %19; fonlamanın payı işlem başına -0.0000R.


**Portföy (tüm dönem, 10.000 $ başlangıç, aynı yönde en fazla %3 açık risk):**

| Risk/işlem | Alınan işlem | Sınır yüzünden atlanan | Son sermaye | Yıllık getiri | Maks. düşüş |
|---|---|---|---|---|---|
| %1 | 693 | 20 | 4,734 $ | %-12.2 | %61.3 |
| %2 | 541 | 172 | 2,936 $ | %-19.2 | %75.4 |

Monte Carlo (işlem sırası 1000 kez karıştırıldı, %1 risk): medyan maks. düşüş %59.4, %95 kötü durumda %66.1.


Gereken kaldıraç (pozisyon / sermaye): %1 riskte medyan 1.4x, %90'lık 3.0x, en yüksek 7.8x; %2 riskte medyan 2.8x, %90'lık 6.1x, en yüksek 15.7x.


**Yıllara göre:**

| Yıl | İşlem | Kazanma | Net R | PF |
|---|---|---|---|---|
| 2021 | 126 | %27.8 | -0.256 | 0.67 |
| 2022 | 108 | %38.9 | +0.045 | 1.06 |
| 2023 | 118 | %29.7 | -0.281 | 0.66 |
| 2024 | 109 | %43.1 | +0.167 | 1.25 |
| 2025 | 156 | %36.5 | -0.041 | 0.94 |
| 2026 | 96 | %33.3 | -0.198 | 0.74 |

**Coinlere göre:**

| Grup | İşlem | Kazanma | Brüt R | Net R | Net R %95 GA | PF | Medyan stop | En uzun kayıp serisi |
|---|---|---|---|---|---|---|---|---|
| ADA | 52 | %40.4 | +0.179 | +0.046 | -0.366 – +0.457 | 1.06 | %0.71 | 5 |
| AVAX | 54 | %27.8 | -0.185 | -0.309 | -0.675 – +0.057 | 0.63 | %0.80 | 7 |
| BNB | 44 | %45.5 | +0.340 | +0.179 | -0.276 – +0.634 | 1.27 | %0.40 | 5 |
| BTC | 53 | %30.2 | -0.094 | -0.284 | -0.675 – +0.107 | 0.67 | %0.44 | 6 |
| CRV | 47 | %34.0 | +0.038 | -0.032 | -0.448 – +0.384 | 0.95 | %1.46 | 8 |
| DOGE | 51 | %17.6 | -0.460 | -0.607 | -0.934 – -0.281 | 0.36 | %0.62 | 15 |
| DOT | 48 | %37.5 | +0.125 | +0.004 | -0.425 – +0.432 | 1.01 | %0.67 | 8 |
| ETH | 48 | %43.8 | +0.314 | +0.199 | -0.224 – +0.623 | 1.32 | %0.68 | 5 |
| ETHFI | 27 | %22.2 | -0.333 | -0.450 | -0.945 – +0.044 | 0.49 | %0.92 | 12 |
| LINK | 66 | %27.3 | -0.182 | -0.325 | -0.662 – +0.012 | 0.62 | %0.65 | 12 |
| LTC | 45 | %33.3 | -0.048 | -0.207 | -0.627 – +0.214 | 0.74 | %0.58 | 8 |
| MMT | 7 | %28.6 | -0.172 | -0.262 | -1.218 – +0.694 | 0.63 | %1.17 | 3 |
| NEAR | 37 | %40.5 | +0.196 | +0.123 | -0.354 – +0.599 | 1.20 | %1.26 | 8 |
| PENGU | 13 | %53.8 | +0.662 | +0.590 | -0.249 – +1.430 | 2.28 | %1.07 | 3 |
| SOL | 43 | %32.6 | -0.060 | -0.178 | -0.605 – +0.250 | 0.77 | %0.67 | 6 |
| SUI | 36 | %55.6 | +0.619 | +0.527 | +0.027 – +1.028 | 2.05 | %0.71 | 4 |
| XRP | 42 | %35.7 | +0.071 | -0.054 | -0.506 – +0.399 | 0.93 | %0.63 | 4 |

## New York gece yarısı açılışı, hedef: Asya aralığının karşı tarafı

Huni: 21733 hafta içi gün → 7369 bias yönünde süpürme → 3955 geri kapanış → 1828 MSS → 1644 FVG → 552 dolan limit emir.

| Grup | İşlem | Kazanma | Brüt R | Net R | Net R %95 GA | PF | Medyan stop | En uzun kayıp serisi |
|---|---|---|---|---|---|---|---|---|
| Tümü | 552 | %26.4 | -0.020 | -0.192 | -0.351 – -0.033 | 0.78 | %0.60 | 16 |
| Örneklem içi | 322 | %27.6 | -0.076 | -0.244 | -0.434 – -0.054 | 0.72 | %0.63 | 16 |
| Örneklem dışı | 230 | %24.8 | +0.059 | -0.119 | -0.393 – +0.156 | 0.87 | %0.53 | 16 |
| Uzun | 274 | %25.9 | -0.117 | -0.287 | -0.495 – -0.078 | 0.68 | %0.63 | 12 |
| Kısa | 278 | %27.0 | +0.076 | -0.098 | -0.338 – +0.142 | 0.89 | %0.55 | 14 |

**Örneklem dışı, devam eşikleri:**

| Ölçüt | Eşik | Sonuç | Durum |
|---|---|---|---|
| İşlem sayısı | ≥ 100 | 230 | Geçti |
| Net beklenti | ≥ +0,15R | -0.119R | Geçmedi |
| Profit factor | ≥ 1,3 | 0.87 | Geçmedi |
| Maks. düşüş (%1 risk) | ≤ %20 | %54.0 | Geçmedi |
| Rastgele kıyastan iyi | p < 0,05 | p = 0.134 | Geçmedi |

Rastgele yönlü kıyas (aynı giriş anı, stop ve hedef, 20 tohum): ortalama net R -0.236 (tohumlar -0.478 … -0.059); model -0.119.


Sonuç dağılımı: hedef %24.5, stop %73.0, zaman %2.5. Ortalama kazanç +2.61R, ortalama kayıp -1.20R. Maliyetlerin brüt kâra oranı %24; fonlamanın payı işlem başına +0.0023R.


**Portföy (tüm dönem, 10.000 $ başlangıç, aynı yönde en fazla %3 açık risk):**

| Risk/işlem | Alınan işlem | Sınır yüzünden atlanan | Son sermaye | Yıllık getiri | Maks. düşüş |
|---|---|---|---|---|---|
| %1 | 547 | 5 | 3,254 $ | %-17.7 | %79.6 |
| %2 | 447 | 105 | 1,433 $ | %-28.7 | %92.9 |

Monte Carlo (işlem sırası 1000 kez karıştırıldı, %1 risk): medyan maks. düşüş %72.0, %95 kötü durumda %77.6.


Gereken kaldıraç (pozisyon / sermaye): %1 riskte medyan 1.7x, %90'lık 3.7x, en yüksek 9.4x; %2 riskte medyan 3.4x, %90'lık 7.5x, en yüksek 18.9x.


**Yıllara göre:**

| Yıl | İşlem | Kazanma | Net R | PF |
|---|---|---|---|---|
| 2021 | 88 | %21.6 | -0.384 | 0.57 |
| 2022 | 100 | %24.0 | -0.333 | 0.63 |
| 2023 | 87 | %32.2 | -0.168 | 0.80 |
| 2024 | 103 | %30.1 | -0.097 | 0.88 |
| 2025 | 94 | %16.0 | -0.515 | 0.49 |
| 2026 | 80 | %36.2 | +0.429 | 1.57 |

**Coinlere göre:**

| Grup | İşlem | Kazanma | Brüt R | Net R | Net R %95 GA | PF | Medyan stop | En uzun kayıp serisi |
|---|---|---|---|---|---|---|---|---|
| ADA | 34 | %29.4 | -0.001 | -0.157 | -0.766 – +0.451 | 0.81 | %0.60 | 5 |
| AVAX | 43 | %23.3 | +0.041 | -0.106 | -0.764 – +0.551 | 0.88 | %0.62 | 9 |
| BNB | 37 | %27.0 | -0.026 | -0.262 | -0.873 – +0.350 | 0.72 | %0.39 | 8 |
| BTC | 48 | %27.1 | +0.259 | -0.008 | -0.725 – +0.709 | 0.99 | %0.32 | 8 |
| CRV | 43 | %32.6 | +0.075 | -0.024 | -0.616 – +0.569 | 0.97 | %1.14 | 8 |
| DOGE | 39 | %30.8 | +0.167 | +0.017 | -0.577 – +0.611 | 1.02 | %0.54 | 5 |
| DOT | 24 | %25.0 | -0.236 | -0.433 | -1.047 – +0.182 | 0.53 | %0.50 | 8 |
| ETH | 34 | %23.5 | -0.076 | -0.276 | -0.949 – +0.397 | 0.71 | %0.41 | 9 |
| ETHFI | 13 | %38.5 | -0.100 | -0.229 | -0.987 – +0.528 | 0.68 | %0.90 | 5 |
| LINK | 50 | %26.0 | +0.032 | -0.132 | -0.682 – +0.418 | 0.85 | %0.62 | 9 |
| LTC | 37 | %21.6 | -0.152 | -0.382 | -1.036 – +0.272 | 0.62 | %0.45 | 15 |
| MMT | 5 | %40.0 | +0.645 | +0.541 | -1.695 – +2.777 | 1.79 | %0.92 | 2 |
| NEAR | 38 | %21.1 | -0.232 | -0.355 | -0.842 – +0.131 | 0.59 | %0.93 | 12 |
| PENGU | 9 | %33.3 | +0.564 | +0.442 | -1.184 – +2.067 | 1.59 | %0.68 | 3 |
| SOL | 42 | %21.4 | -0.185 | -0.361 | -0.882 – +0.161 | 0.62 | %0.45 | 9 |
| SUI | 21 | %23.8 | -0.265 | -0.396 | -1.005 – +0.213 | 0.54 | %0.72 | 5 |
| XRP | 35 | %28.6 | -0.183 | -0.336 | -0.800 – +0.128 | 0.59 | %0.63 | 8 |

## New York gece yarısı açılışı, hedef: sabit 2R

Huni: 21733 hafta içi gün → 7369 bias yönünde süpürme → 3955 geri kapanış → 1828 MSS → 1644 FVG → 499 dolan limit emir.

| Grup | İşlem | Kazanma | Brüt R | Net R | Net R %95 GA | PF | Medyan stop | En uzun kayıp serisi |
|---|---|---|---|---|---|---|---|---|
| Tümü | 499 | %34.3 | +0.018 | -0.132 | -0.260 – -0.003 | 0.83 | %0.63 | 14 |
| Örneklem içi | 288 | %35.4 | +0.046 | -0.099 | -0.270 – +0.071 | 0.87 | %0.67 | 14 |
| Örneklem dışı | 211 | %32.7 | -0.020 | -0.176 | -0.371 – +0.018 | 0.78 | %0.57 | 11 |
| Uzun | 254 | %33.5 | -0.011 | -0.164 | -0.343 – +0.015 | 0.79 | %0.63 | 11 |
| Kısa | 245 | %35.1 | +0.049 | -0.098 | -0.283 – +0.086 | 0.87 | %0.62 | 12 |

**Örneklem dışı, devam eşikleri:**

| Ölçüt | Eşik | Sonuç | Durum |
|---|---|---|---|
| İşlem sayısı | ≥ 100 | 211 | Geçti |
| Net beklenti | ≥ +0,15R | -0.176R | Geçmedi |
| Profit factor | ≥ 1,3 | 0.78 | Geçmedi |
| Maks. düşüş (%1 risk) | ≤ %20 | %40.0 | Geçmedi |
| Rastgele kıyastan iyi | p < 0,05 | p = 0.529 | Geçmedi |

Rastgele yönlü kıyas (aynı giriş anı, stop ve hedef, 20 tohum): ortalama net R -0.170 (tohumlar -0.341 … -0.056); model -0.176.


Sonuç dağılımı: hedef %33.1, stop %64.9, zaman %2.0. Ortalama kazanç +1.87R, ortalama kayıp -1.18R. Maliyetlerin brüt kâra oranı %22; fonlamanın payı işlem başına +0.0022R.


**Portföy (tüm dönem, 10.000 $ başlangıç, aynı yönde en fazla %3 açık risk):**

| Risk/işlem | Alınan işlem | Sınır yüzünden atlanan | Son sermaye | Yıllık getiri | Maks. düşüş |
|---|---|---|---|---|---|
| %1 | 496 | 3 | 4,896 $ | %-11.7 | %53.2 |
| %2 | 421 | 78 | 3,229 $ | %-17.9 | %69.9 |

Monte Carlo (işlem sırası 1000 kez karıştırıldı, %1 risk): medyan maks. düşüş %55.7, %95 kötü durumda %62.4.


Gereken kaldıraç (pozisyon / sermaye): %1 riskte medyan 1.6x, %90'lık 3.4x, en yüksek 9.4x; %2 riskte medyan 3.2x, %90'lık 6.8x, en yüksek 18.9x.


**Yıllara göre:**

| Yıl | İşlem | Kazanma | Net R | PF |
|---|---|---|---|---|
| 2021 | 73 | %30.1 | -0.250 | 0.68 |
| 2022 | 86 | %32.6 | -0.200 | 0.75 |
| 2023 | 86 | %34.9 | -0.121 | 0.85 |
| 2024 | 91 | %47.3 | +0.287 | 1.47 |
| 2025 | 88 | %26.1 | -0.381 | 0.56 |
| 2026 | 75 | %33.3 | -0.167 | 0.79 |

**Coinlere göre:**

| Grup | İşlem | Kazanma | Brüt R | Net R | Net R %95 GA | PF | Medyan stop | En uzun kayıp serisi |
|---|---|---|---|---|---|---|---|---|
| ADA | 34 | %35.3 | +0.047 | -0.086 | -0.587 – +0.415 | 0.89 | %0.70 | 6 |
| AVAX | 35 | %31.4 | -0.057 | -0.184 | -0.663 – +0.295 | 0.77 | %0.70 | 7 |
| BNB | 33 | %39.4 | +0.091 | -0.107 | -0.605 – +0.391 | 0.85 | %0.41 | 7 |
| BTC | 41 | %36.6 | +0.098 | -0.140 | -0.614 – +0.333 | 0.83 | %0.33 | 6 |
| CRV | 38 | %31.6 | -0.097 | -0.184 | -0.631 – +0.263 | 0.76 | %1.22 | 6 |
| DOGE | 36 | %41.7 | +0.250 | +0.113 | -0.389 – +0.615 | 1.17 | %0.58 | 4 |
| DOT | 22 | %40.9 | +0.227 | +0.051 | -0.613 – +0.715 | 1.07 | %0.53 | 3 |
| ETH | 30 | %30.0 | -0.100 | -0.271 | -0.789 – +0.248 | 0.68 | %0.45 | 5 |
| ETHFI | 13 | %30.8 | -0.077 | -0.205 | -1.018 – +0.608 | 0.75 | %0.90 | 5 |
| LINK | 41 | %26.8 | -0.195 | -0.350 | -0.782 – +0.082 | 0.60 | %0.63 | 7 |
| LTC | 38 | %34.2 | -0.011 | -0.205 | -0.676 – +0.267 | 0.75 | %0.48 | 6 |
| MMT | 4 | %0.0 | -0.852 | -0.968 | -1.301 – -0.635 | 0.00 | %1.12 | 4 |
| NEAR | 35 | %28.6 | -0.114 | -0.228 | -0.698 – +0.241 | 0.71 | %1.01 | 6 |
| PENGU | 7 | %28.6 | -0.055 | -0.135 | -1.204 – +0.934 | 0.80 | %1.06 | 3 |
| SOL | 36 | %30.6 | -0.101 | -0.253 | -0.718 – +0.211 | 0.69 | %0.51 | 5 |
| SUI | 21 | %42.9 | +0.286 | +0.180 | -0.488 – +0.847 | 1.28 | %0.72 | 5 |
| XRP | 35 | %42.9 | +0.286 | +0.165 | -0.351 – +0.681 | 1.25 | %0.63 | 5 |

## Sağlamlık: parametreler tek tek değiştirildiğinde (tüm dönem, net R)

| Değişiklik | UTC işlem | UTC net R | UTC PF | NY işlem | NY net R | NY PF |
|---|---|---|---|---|---|---|
| Temel (hedef Asya) | 810 | -0.222 | 0.75 | 552 | -0.192 | 0.78 |
| Asya bitişi 1 saat erken | 956 | -0.239 | 0.73 | 691 | -0.198 | 0.77 |
| Asya bitişi 1 saat geç | 702 | -0.234 | 0.74 | 537 | -0.228 | 0.75 |
| Geri kapanış N = 2 | 722 | -0.232 | 0.74 | 493 | -0.213 | 0.76 |
| Geri kapanış N = 5 | 879 | -0.204 | 0.77 | 630 | -0.196 | 0.78 |
| FVG bekleme X = 6 | 539 | -0.208 | 0.76 | 382 | -0.226 | 0.74 |
| FVG bekleme X = 24 | 1132 | -0.197 | 0.78 | 713 | -0.202 | 0.77 |
| Stop tamponu 0,3 ATR | 810 | -0.173 | 0.80 | 552 | -0.171 | 0.80 |
| Pivot 3 mum | 599 | -0.221 | 0.75 | 442 | -0.142 | 0.84 |
| Bias filtresi yok | 1411 | -0.197 | 0.77 | 1334 | -0.282 | 0.69 |
