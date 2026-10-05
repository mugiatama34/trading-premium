# PO3 Kural Seti v2 (geniş stop): Sonuçlar

Kod: `v2_secim.py` (seçim kuralı dosyanın başında), motor: `backtest.py`. Kurallar: [../../po3-kural-seti-v2.md](../../po3-kural-seti-v2.md). Maliyetler v1 ile aynı: maker %0,02 giriş ve hedef, taker %0,05 + kayma stop ve zaman çıkışı, gerçek fonlama.

Örneklem içi: 2021-01 → 2024-06-01. Örneklem dışı: sonrası → 2026-09.


## Seçilen v2: NY, stop ≥ %1.5 (genislet), hedef 2R

Seçim yalnızca örneklem içi sonuçlara göre yapıldı (44 uygun aday arasında en yüksek net R).

| Grup | İşlem | Kazanma | Brüt R | Net R | Net R %95 GA | PF | Medyan stop | En uzun kayıp serisi |
|---|---|---|---|---|---|---|---|---|
| Örneklem içi | 331 | %43.5 | +0.115 | +0.060 | -0.082 – +0.201 | 1.11 | %1.50 | 10 |
| Örneklem dışı | 248 | %31.9 | -0.136 | -0.193 | -0.345 – -0.042 | 0.71 | %1.50 | 13 |

**Örneklem dışı, devam eşikleri:**

| Ölçüt | Eşik | Sonuç | Durum |
|---|---|---|---|
| İşlem sayısı | ≥ 100 | 248 | Geçti |
| Net beklenti | ≥ +0,15R | -0.193R | Geçmedi |
| Profit factor | ≥ 1,3 | 0.71 | Geçmedi |
| Maks. düşüş (%1 risk) | ≤ %20 | %47.6 | Geçmedi |
| Rastgele kıyastan iyi | p < 0,05 | p = 0.892 | Geçmedi |

Rastgele yönlü kıyas (20 tohum): ortalama net R -0.105 (tohumlar -0.253 … -0.019); model -0.193.


Örneklem dışı sonuç dağılımı: hedef %18.5, stop %58.9, zaman %22.6. Ortalama kazanç +1.45R, ortalama kayıp -0.96R. İşlem başına maliyet 0.057R.


**Örneklem dışı portföy (10.000 $, aynı yönde en fazla %3 açık risk):**

| Risk/işlem | Alınan işlem | Atlanan | Son sermaye | Yıllık getiri | Maks. düşüş |
|---|---|---|---|---|---|
| %1 | 236 | 12 | 6,607 $ | %-16.3 | %47.6 |
| %2 | 179 | 69 | 5,645 $ | %-21.7 | %60.7 |

Monte Carlo (örneklem dışı, %1 risk): medyan maks. düşüş %42.2, %95 kötü durumda %47.0.


Gereken kaldıraç: %1 riskte medyan 0.7x, %90'lık 0.7x, en yüksek 0.7x; %2 riskte medyan 1.3x, %90'lık 1.3x, en yüksek 1.3x.


**Yıllara göre (tüm dönem):**

| Yıl | İşlem | Kazanma | Net R | PF |
|---|---|---|---|---|
| 2021 | 88 | %35.2 | -0.169 | 0.75 |
| 2022 | 102 | %44.1 | +0.049 | 1.09 |
| 2023 | 91 | %42.9 | +0.053 | 1.10 |
| 2024 | 118 | %39.8 | +0.017 | 1.03 |
| 2025 | 97 | %26.8 | -0.351 | 0.51 |
| 2026 | 83 | %42.2 | +0.107 | 1.20 |

**Coinlere göre (örneklem dışı):**

| Grup | İşlem | Kazanma | Brüt R | Net R | Net R %95 GA | PF | Medyan stop | En uzun kayıp serisi |
|---|---|---|---|---|---|---|---|---|
| ADA | 16 | %50.0 | +0.424 | +0.376 | -0.369 – +1.121 | 1.71 | %1.50 | 3 |
| AVAX | 18 | %33.3 | -0.050 | -0.105 | -0.742 – +0.531 | 0.85 | %1.50 | 6 |
| BNB | 17 | %52.9 | +0.367 | +0.314 | -0.222 – +0.849 | 2.03 | %1.50 | 3 |
| BTC | 17 | %29.4 | -0.181 | -0.231 | -0.813 – +0.352 | 0.66 | %1.50 | 5 |
| CRV | 14 | %35.7 | -0.053 | -0.112 | -0.850 – +0.625 | 0.84 | %1.50 | 5 |
| DOGE | 15 | %26.7 | -0.236 | -0.299 | -0.854 – +0.257 | 0.54 | %1.50 | 7 |
| DOT | 10 | %20.0 | -0.435 | -0.500 | -1.244 – +0.244 | 0.41 | %1.50 | 7 |
| ETH | 14 | %42.9 | -0.086 | -0.136 | -0.729 – +0.457 | 0.75 | %1.50 | 2 |
| ETHFI | 13 | %30.8 | -0.148 | -0.215 | -0.926 – +0.496 | 0.69 | %1.50 | 3 |
| LINK | 20 | %20.0 | -0.424 | -0.488 | -0.956 – -0.020 | 0.37 | %1.50 | 8 |
| LTC | 17 | %23.5 | -0.546 | -0.613 | -1.046 – -0.179 | 0.25 | %1.50 | 8 |
| MMT | 5 | %40.0 | +0.318 | +0.268 | -1.119 – +1.656 | 1.51 | %1.50 | 3 |
| NEAR | 16 | %18.8 | -0.452 | -0.511 | -1.043 – +0.021 | 0.36 | %1.50 | 8 |
| PENGU | 10 | %20.0 | -0.339 | -0.397 | -1.183 – +0.389 | 0.50 | %1.50 | 5 |
| SOL | 20 | %30.0 | -0.098 | -0.152 | -0.670 – +0.367 | 0.75 | %1.50 | 9 |
| SUI | 15 | %20.0 | -0.506 | -0.569 | -1.054 – -0.084 | 0.29 | %1.50 | 5 |
| XRP | 11 | %54.5 | +0.485 | +0.437 | -0.386 – +1.261 | 2.05 | %1.50 | 3 |

## Tüm adaylar (örneklem içi sıralı)

Örneklem dışı sütunları seçimde kullanılmadı; seçimin şansa bağlı olup olmadığını görmek için verilir.

| Aday | İçi işlem | İçi net R | İçi PF | Dışı işlem | Dışı net R | Dışı PF |
|---|---|---|---|---|---|---|
| UTC, v1, hedef Asya | 443 | -0.324 | 0.64 | 367 | -0.099 | 0.89 |
| UTC, v1, hedef 2R | 390 | -0.124 | 0.84 | 323 | -0.060 | 0.92 |
| NY, v1, hedef Asya | 322 | -0.244 | 0.72 | 230 | -0.119 | 0.87 |
| NY, v1, hedef 2R | 288 | -0.099 | 0.87 | 211 | -0.176 | 0.78 |
| NY, stop ≥ %1.5 (filtre), hedef 2R | 36 | +0.157 | 1.25 | 14 | -0.893 | 0.00 |
| NY, stop ≥ %1 (filtre), hedef 2R | 80 | +0.136 | 1.22 | 40 | -0.564 | 0.34 |
| NY, stop ≥ %1.5 (filtre), hedef 1.5R | 34 | +0.136 | 1.24 | 14 | -0.283 | 0.60 |
| NY, stop ≥ %0.8 (filtre), hedef 2R | 112 | +0.120 | 1.19 | 62 | -0.446 | 0.46 |
| NY, stop ≥ %0.8 (filtre), hedef 1.5R | 105 | +0.118 | 1.21 | 55 | -0.396 | 0.49 |
| NY, stop ≥ %1 (filtre), hedef 1.5R | 76 | +0.114 | 1.20 | 38 | -0.457 | 0.43 |
| NY, stop ≥ %0.8 (filtre), hedef 3R | 117 | +0.069 | 1.10 | 65 | -0.562 | 0.37 |
| NY, stop ≥ %1.5 (genislet), hedef 2R **(seçilen)** | 331 | +0.060 | 1.11 | 248 | -0.193 | 0.71 |
| NY, stop ≥ %1 (filtre), hedef Asya | 78 | +0.042 | 1.07 | 39 | -0.631 | 0.26 |
| NY, stop ≥ %1.5 (genislet), hedef 1.5R | 323 | +0.035 | 1.07 | 242 | -0.119 | 0.80 |
| NY, stop ≥ %1 (filtre), hedef 3R | 82 | +0.034 | 1.05 | 40 | -0.724 | 0.21 |
| NY, stop ≥ %0.6 (filtre), hedef 1.5R | 148 | +0.032 | 1.05 | 92 | -0.219 | 0.69 |
| NY, stop ≥ %1.5 (genislet), hedef 3R | 334 | +0.029 | 1.05 | 250 | -0.297 | 0.57 |
| UTC, stop ≥ %1.5 (filtre), hedef 2R | 78 | -0.006 | 0.99 | 30 | +0.003 | 1.01 |
| UTC, stop ≥ %0.8 (filtre), hedef 2R | 189 | -0.011 | 0.98 | 102 | -0.219 | 0.71 |
| NY, stop ≥ %0.8 (filtre), hedef Asya | 115 | -0.012 | 0.98 | 59 | -0.381 | 0.54 |
| NY, stop ≥ %0.6 (genislet), hedef 1.5R | 285 | -0.013 | 0.98 | 210 | -0.154 | 0.78 |
| NY, stop ≥ %0.8 (genislet), hedef 3R | 332 | -0.027 | 0.97 | 246 | -0.215 | 0.74 |
| NY, stop ≥ %0.6 (filtre), hedef 2R | 162 | -0.037 | 0.95 | 102 | -0.271 | 0.65 |
| NY, stop ≥ %1 (genislet), hedef 3R | 333 | -0.046 | 0.94 | 248 | -0.173 | 0.78 |
| NY, stop ≥ %0.6 (filtre), hedef 3R | 175 | -0.047 | 0.94 | 110 | -0.430 | 0.51 |
| NY, stop ≥ %1 (genislet), hedef 2R | 324 | -0.048 | 0.93 | 237 | -0.116 | 0.83 |
| NY, stop ≥ %0.8 (genislet), hedef 1.5R | 302 | -0.058 | 0.91 | 218 | -0.136 | 0.80 |
| UTC, stop ≥ %1 (filtre), hedef 2R | 149 | -0.062 | 0.91 | 75 | -0.164 | 0.77 |
| NY, stop ≥ %1.5 (genislet), hedef Asya | 322 | -0.066 | 0.88 | 230 | -0.125 | 0.78 |
| UTC, stop ≥ %0.6 (filtre), hedef 2R | 262 | -0.066 | 0.91 | 171 | -0.180 | 0.76 |
| NY, stop ≥ %0.6 (genislet), hedef 2R | 311 | -0.069 | 0.91 | 225 | -0.171 | 0.78 |
| UTC, stop ≥ %1.5 (genislet), hedef 2R | 454 | -0.074 | 0.88 | 377 | -0.149 | 0.77 |
| UTC, stop ≥ %0.8 (filtre), hedef 1.5R | 172 | -0.075 | 0.88 | 92 | -0.168 | 0.75 |
| NY, stop ≥ %1 (genislet), hedef 1.5R | 313 | -0.087 | 0.86 | 224 | -0.087 | 0.86 |
| UTC, stop ≥ %0.6 (filtre), hedef 1.5R | 233 | -0.088 | 0.87 | 152 | -0.229 | 0.68 |
| NY, stop ≥ %0.6 (genislet), hedef 3R | 328 | -0.088 | 0.89 | 241 | -0.213 | 0.75 |
| NY, stop ≥ %1.5 (filtre), hedef 3R | 38 | -0.089 | 0.88 | 14 | -0.893 | 0.00 |
| NY, stop ≥ %0.8 (genislet), hedef 2R | 319 | -0.090 | 0.87 | 233 | -0.181 | 0.76 |
| UTC, stop ≥ %0.8 (genislet), hedef 3R | 453 | -0.093 | 0.88 | 374 | -0.049 | 0.94 |
| UTC, stop ≥ %1.5 (filtre), hedef 1.5R | 74 | -0.098 | 0.85 | 30 | +0.249 | 1.53 |
| UTC, stop ≥ %1.5 (genislet), hedef 1.5R | 441 | -0.106 | 0.82 | 368 | -0.084 | 0.86 |
| UTC, stop ≥ %0.8 (filtre), hedef 3R | 198 | -0.112 | 0.85 | 105 | -0.170 | 0.78 |
| UTC, stop ≥ %0.8 (genislet), hedef 2R | 433 | -0.113 | 0.84 | 354 | -0.028 | 0.96 |
| UTC, stop ≥ %0.6 (genislet), hedef 2R | 419 | -0.114 | 0.85 | 344 | -0.036 | 0.95 |
| UTC, stop ≥ %0.8 (genislet), hedef 1.5R | 398 | -0.122 | 0.82 | 332 | -0.013 | 0.98 |
| UTC, stop ≥ %1 (genislet), hedef 2R | 443 | -0.133 | 0.81 | 365 | -0.043 | 0.94 |
| UTC, stop ≥ %0.6 (genislet), hedef 1.5R | 372 | -0.136 | 0.80 | 311 | -0.101 | 0.85 |
| UTC, stop ≥ %1 (filtre), hedef 1.5R | 139 | -0.143 | 0.78 | 71 | -0.128 | 0.81 |
| NY, stop ≥ %0.8 (genislet), hedef Asya | 322 | -0.146 | 0.80 | 230 | -0.137 | 0.81 |
| NY, stop ≥ %1.5 (filtre), hedef Asya | 36 | -0.146 | 0.77 | 13 | -0.659 | 0.19 |
| NY, stop ≥ %1 (genislet), hedef Asya | 322 | -0.151 | 0.78 | 230 | -0.100 | 0.85 |
| UTC, stop ≥ %1 (genislet), hedef 3R | 456 | -0.151 | 0.80 | 378 | -0.126 | 0.83 |
| NY, stop ≥ %0.6 (filtre), hedef Asya | 171 | -0.158 | 0.79 | 103 | -0.298 | 0.64 |
| UTC, stop ≥ %1 (genislet), hedef 1.5R | 416 | -0.172 | 0.74 | 344 | -0.024 | 0.96 |
| UTC, stop ≥ %1.5 (genislet), hedef 3R | 458 | -0.173 | 0.74 | 381 | -0.134 | 0.80 |
| NY, stop ≥ %0.6 (genislet), hedef Asya | 322 | -0.184 | 0.76 | 230 | -0.143 | 0.82 |
| UTC, stop ≥ %0.6 (filtre), hedef 3R | 280 | -0.187 | 0.77 | 183 | -0.169 | 0.79 |
| UTC, stop ≥ %0.8 (filtre), hedef Asya | 192 | -0.194 | 0.75 | 102 | -0.132 | 0.82 |
| UTC, stop ≥ %1.5 (genislet), hedef Asya | 443 | -0.196 | 0.69 | 367 | -0.062 | 0.89 |
| UTC, stop ≥ %0.6 (genislet), hedef 3R | 448 | -0.198 | 0.76 | 365 | -0.037 | 0.95 |
| UTC, stop ≥ %0.8 (genislet), hedef Asya | 443 | -0.199 | 0.74 | 367 | -0.028 | 0.96 |
| UTC, stop ≥ %1 (genislet), hedef Asya | 443 | -0.219 | 0.70 | 367 | -0.022 | 0.97 |
| UTC, stop ≥ %1.5 (filtre), hedef Asya | 76 | -0.228 | 0.68 | 30 | +0.084 | 1.16 |
| UTC, stop ≥ %1 (filtre), hedef 3R | 154 | -0.235 | 0.70 | 76 | -0.151 | 0.80 |
| UTC, stop ≥ %0.6 (genislet), hedef Asya | 443 | -0.247 | 0.70 | 367 | -0.020 | 0.97 |
| UTC, stop ≥ %1 (filtre), hedef Asya | 148 | -0.249 | 0.68 | 74 | -0.090 | 0.87 |
| UTC, stop ≥ %0.6 (filtre), hedef Asya | 276 | -0.265 | 0.68 | 182 | -0.168 | 0.79 |
| UTC, stop ≥ %1.5 (filtre), hedef 3R | 80 | -0.287 | 0.62 | 31 | +0.034 | 1.06 |

64 adaydan örneklem dışında net R'si pozitif olan: 4; beklenti ve PF eşiğini birlikte geçen: 1.

