# Devam (Kırılım) Modeli: Sonuçlar

Kod ve kurallar: `devam.py` (dosyanın başında). Maliyetler: retest girişi ve hedef maker %0,02; piyasa girişi, stop ve zaman çıkışı taker %0,05 + coin bazında kayma; gerçek fonlama.

Örneklem içi: 2021-01 → 2024-06-01. Örneklem dışı: sonrası → 2026-09.


## Seçilen aday: NY, giriş retest, stop karsi, hedef gun, bias var

Seçim yalnızca örneklem içi sonuçlara göre yapıldı (48 uygun aday arasında en yüksek net R).

| Grup | İşlem | Kazanma | Brüt R | Net R | Net R %95 GA | PF | Medyan stop | En uzun kayıp serisi |
|---|---|---|---|---|---|---|---|---|
| Örneklem içi | 4054 | %38.3 | +0.019 | -0.029 | -0.096 – +0.038 | 0.94 | %2.69 | 38 |
| Örneklem dışı | 3537 | %42.1 | +0.031 | -0.019 | -0.061 – +0.022 | 0.96 | %2.31 | 39 |

**Örneklem dışı, devam eşikleri:**

| Ölçüt | Eşik | Sonuç | Durum |
|---|---|---|---|
| İşlem sayısı | ≥ 100 | 3537 | Geçti |
| Net beklenti | ≥ +0,15R | -0.019R | Geçmedi |
| Profit factor | ≥ 1,3 | 0.96 | Geçmedi |
| Maks. düşüş (%1 risk) | ≤ %20 | %85.1 | Geçmedi |
| Rastgele kıyastan iyi | p < 0,05 | p = 0.004 | Geçti |

Rastgele yönlü kıyas (20 tohum): ortalama net R -0.068 (tohumlar -0.127 … -0.038); model -0.019.


Örneklem dışı sonuç dağılımı: hedef %0.0, stop %41.6, zaman %58.4. İşlem başına maliyet 0.051R.


**Örneklem dışı portföy (10.000 $, aynı yönde en fazla %3 açık risk):**

| Risk/işlem | Alınan işlem | Atlanan | Son sermaye | Yıllık getiri | Maks. düşüş |
|---|---|---|---|---|---|
| %1 | 1798 | 1739 | 2,054 $ | %-49.3 | %85.1 |
| %2 | 765 | 2772 | 1,666 $ | %-53.6 | %85.5 |

Monte Carlo (örneklem dışı, %1 risk): medyan maks. düşüş %73.9, %95 kötü durumda %82.9.


Gereken kaldıraç: %1 riskte medyan 0.4x, %90'lık 0.9x, en yüksek 4.6x; %2 riskte medyan 0.8x, %90'lık 1.8x, en yüksek 9.3x.


**Yıllara göre (tüm dönem):**

| Yıl | İşlem | Kazanma | Net R | PF |
|---|---|---|---|---|
| 2021 | 1158 | %45.8 | +0.033 | 1.08 |
| 2022 | 1081 | %34.0 | -0.177 | 0.67 |
| 2023 | 1185 | %38.4 | +0.095 | 1.17 |
| 2024 | 1421 | %39.5 | -0.042 | 0.92 |
| 2025 | 1502 | %40.0 | -0.074 | 0.86 |
| 2026 | 1244 | %42.1 | +0.020 | 1.04 |

**Coinlere göre (örneklem dışı):**

| Grup | İşlem | Kazanma | Brüt R | Net R | Net R %95 GA | PF | Medyan stop | En uzun kayıp serisi |
|---|---|---|---|---|---|---|---|---|
| ADA | 233 | %42.9 | +0.031 | -0.019 | -0.175 – +0.138 | 0.96 | %2.29 | 7 |
| AVAX | 209 | %45.5 | +0.071 | +0.019 | -0.150 – +0.188 | 1.04 | %2.36 | 10 |
| BNB | 238 | %38.2 | -0.036 | -0.106 | -0.250 – +0.038 | 0.80 | %1.48 | 9 |
| BTC | 198 | %44.9 | +0.152 | +0.082 | -0.106 – +0.271 | 1.16 | %1.23 | 8 |
| CRV | 202 | %38.1 | -0.167 | -0.210 | -0.340 – -0.081 | 0.60 | %3.01 | 7 |
| DOGE | 206 | %43.2 | +0.127 | +0.076 | -0.102 – +0.254 | 1.17 | %2.27 | 8 |
| DOT | 230 | %43.5 | -0.011 | -0.060 | -0.205 – +0.085 | 0.87 | %2.34 | 9 |
| ETH | 207 | %44.9 | +0.187 | +0.137 | -0.087 – +0.361 | 1.29 | %1.76 | 9 |
| ETHFI | 238 | %40.3 | -0.073 | -0.111 | -0.249 – +0.026 | 0.77 | %3.67 | 12 |
| LINK | 228 | %44.7 | +0.024 | -0.025 | -0.182 – +0.131 | 0.95 | %2.32 | 9 |
| LTC | 215 | %40.5 | -0.004 | -0.067 | -0.244 – +0.109 | 0.88 | %1.85 | 7 |
| MMT | 93 | %40.9 | -0.005 | -0.054 | -0.323 – +0.215 | 0.89 | %3.64 | 8 |
| NEAR | 230 | %43.9 | +0.074 | +0.036 | -0.121 – +0.193 | 1.08 | %2.91 | 6 |
| PENGU | 152 | %45.4 | +0.111 | +0.072 | -0.138 – +0.282 | 1.14 | %3.53 | 5 |
| SOL | 213 | %42.7 | -0.019 | -0.067 | -0.223 – +0.090 | 0.87 | %2.11 | 11 |
| SUI | 211 | %37.0 | -0.057 | -0.098 | -0.260 – +0.065 | 0.82 | %2.77 | 10 |
| XRP | 234 | %39.7 | +0.144 | +0.087 | -0.108 – +0.282 | 1.17 | %1.83 | 9 |

## Tüm adaylar (örneklem içi sıralı)

Örneklem dışı sütunları seçimde kullanılmadı.

| Aday | İçi işlem | İçi brüt R | İçi net R | İçi PF | Dışı işlem | Dışı brüt R | Dışı net R | Dışı PF |
|---|---|---|---|---|---|---|---|---|
| NY, giriş retest, stop karsi, hedef gun, bias var **(seçilen)** | 4054 | +0.019 | -0.029 | 0.94 | 3537 | +0.031 | -0.019 | 0.96 |
| NY, giriş retest, stop karsi, hedef gun, bias yok | 7280 | +0.016 | -0.032 | 0.94 | 5996 | -0.020 | -0.071 | 0.87 |
| NY, giriş retest, stop karsi, hedef 1R, bias yok | 7193 | -0.000 | -0.035 | 0.92 | 5950 | +0.010 | -0.028 | 0.94 |
| NY, giriş piyasa, stop karsi, hedef 1R, bias yok | 5718 | +0.014 | -0.039 | 0.91 | 4969 | +0.029 | -0.029 | 0.93 |
| UTC, giriş piyasa, stop karsi, hedef 2R, bias yok | 4291 | +0.012 | -0.042 | 0.90 | 3621 | -0.012 | -0.074 | 0.84 |
| UTC, giriş piyasa, stop karsi, hedef 1R, bias yok | 4291 | +0.006 | -0.043 | 0.89 | 3621 | +0.004 | -0.052 | 0.88 |
| NY, giriş retest, stop karsi, hedef 1R, bias var | 4004 | -0.008 | -0.043 | 0.90 | 3509 | +0.038 | +0.000 | 1.00 |
| NY, giriş piyasa, stop karsi, hedef 2R, bias var | 3321 | +0.012 | -0.044 | 0.90 | 3051 | +0.033 | -0.031 | 0.93 |
| UTC, giriş retest, stop karsi, hedef 1R, bias yok | 7705 | -0.015 | -0.045 | 0.89 | 6505 | -0.029 | -0.063 | 0.85 |
| NY, giriş piyasa, stop karsi, hedef 1R, bias var | 3321 | +0.004 | -0.047 | 0.89 | 3051 | +0.046 | -0.010 | 0.97 |
| NY, giriş piyasa, stop karsi, hedef gun, bias var | 3321 | +0.012 | -0.049 | 0.90 | 3051 | +0.019 | -0.048 | 0.89 |
| NY, giriş piyasa, stop karsi, hedef 2R, bias yok | 5718 | +0.009 | -0.049 | 0.90 | 4969 | +0.006 | -0.059 | 0.87 |
| NY, giriş retest, stop karsi, hedef 2R, bias yok | 7276 | -0.010 | -0.051 | 0.90 | 5995 | -0.001 | -0.047 | 0.91 |
| NY, giriş piyasa, stop karsi, hedef gun, bias yok | 5718 | +0.008 | -0.055 | 0.89 | 4969 | -0.010 | -0.079 | 0.84 |
| UTC, giriş retest, stop karsi, hedef 2R, bias yok | 7728 | -0.021 | -0.057 | 0.87 | 6515 | -0.038 | -0.078 | 0.83 |
| UTC, giriş retest, stop karsi, hedef gun, bias yok | 7728 | -0.017 | -0.057 | 0.88 | 6516 | -0.053 | -0.097 | 0.80 |
| UTC, giriş piyasa, stop karsi, hedef gun, bias yok | 4291 | -0.000 | -0.058 | 0.87 | 3621 | -0.026 | -0.090 | 0.80 |
| NY, giriş retest, stop karsi, hedef 2R, bias var | 4052 | -0.020 | -0.061 | 0.88 | 3536 | +0.034 | -0.011 | 0.98 |
| UTC, giriş piyasa, stop orta, hedef 1R, bias yok | 4291 | +0.024 | -0.062 | 0.88 | 3621 | +0.017 | -0.081 | 0.85 |
| NY, giriş piyasa, stop orta, hedef 1R, bias var | 3321 | +0.022 | -0.064 | 0.87 | 3051 | +0.070 | -0.025 | 0.95 |
| NY, giriş piyasa, stop orta, hedef 1R, bias yok | 5718 | +0.025 | -0.065 | 0.87 | 4969 | +0.029 | -0.069 | 0.87 |
| UTC, giriş piyasa, stop orta, hedef 2R, bias yok | 4291 | +0.026 | -0.069 | 0.89 | 3621 | -0.004 | -0.112 | 0.83 |
| UTC, giriş piyasa, stop karsi, hedef 2R, bias var | 1915 | -0.026 | -0.080 | 0.83 | 1739 | +0.003 | -0.058 | 0.87 |
| UTC, giriş retest, stop karsi, hedef 1R, bias var | 3397 | -0.050 | -0.082 | 0.81 | 3118 | -0.009 | -0.043 | 0.90 |
| UTC, giriş retest, stop orta, hedef 1R, bias yok | 7540 | -0.028 | -0.083 | 0.84 | 6377 | -0.047 | -0.109 | 0.80 |
| NY, giriş piyasa, stop orta, hedef 2R, bias yok | 5718 | +0.014 | -0.085 | 0.87 | 4969 | +0.015 | -0.093 | 0.86 |
| NY, giriş piyasa, stop orta, hedef 2R, bias var | 3321 | +0.008 | -0.086 | 0.86 | 3051 | +0.056 | -0.049 | 0.92 |
| UTC, giriş piyasa, stop karsi, hedef 1R, bias var | 1915 | -0.039 | -0.089 | 0.79 | 1739 | +0.013 | -0.042 | 0.90 |
| UTC, giriş piyasa, stop orta, hedef 1R, bias var | 1915 | -0.004 | -0.090 | 0.83 | 1739 | +0.042 | -0.054 | 0.89 |
| NY, giriş retest, stop orta, hedef 1R, bias var | 3774 | -0.028 | -0.093 | 0.83 | 3279 | +0.024 | -0.045 | 0.91 |
| NY, giriş retest, stop orta, hedef 1R, bias yok | 6789 | -0.028 | -0.095 | 0.83 | 5597 | -0.006 | -0.078 | 0.86 |
| UTC, giriş retest, stop karsi, hedef 2R, bias var | 3410 | -0.059 | -0.096 | 0.80 | 3126 | -0.008 | -0.048 | 0.90 |
| UTC, giriş retest, stop karsi, hedef gun, bias var | 3410 | -0.056 | -0.097 | 0.80 | 3127 | -0.031 | -0.074 | 0.84 |
| UTC, giriş retest, stop orta, hedef 2R, bias yok | 7705 | -0.036 | -0.101 | 0.85 | 6505 | -0.068 | -0.140 | 0.80 |
| UTC, giriş piyasa, stop orta, hedef gun, bias yok | 4291 | +0.006 | -0.101 | 0.85 | 3621 | -0.050 | -0.170 | 0.76 |
| UTC, giriş piyasa, stop karsi, hedef gun, bias var | 1915 | -0.045 | -0.103 | 0.78 | 1739 | -0.014 | -0.078 | 0.83 |
| UTC, giriş retest, stop orta, hedef 1R, bias var | 3309 | -0.048 | -0.105 | 0.81 | 3040 | -0.020 | -0.082 | 0.85 |
| NY, giriş retest, stop orta, hedef 2R, bias yok | 7193 | -0.042 | -0.120 | 0.83 | 5950 | -0.009 | -0.093 | 0.87 |
| NY, giriş piyasa, stop orta, hedef gun, bias yok | 5718 | -0.014 | -0.126 | 0.82 | 4969 | -0.025 | -0.147 | 0.79 |
| NY, giriş retest, stop orta, hedef 2R, bias var | 4004 | -0.050 | -0.126 | 0.82 | 3509 | +0.042 | -0.040 | 0.94 |
| NY, giriş piyasa, stop orta, hedef gun, bias var | 3321 | -0.020 | -0.126 | 0.82 | 3051 | +0.025 | -0.093 | 0.86 |
| UTC, giriş retest, stop orta, hedef gun, bias yok | 7728 | -0.048 | -0.127 | 0.82 | 6516 | -0.110 | -0.196 | 0.74 |
| UTC, giriş piyasa, stop orta, hedef 2R, bias var | 1915 | -0.036 | -0.131 | 0.80 | 1739 | +0.020 | -0.086 | 0.87 |
| NY, giriş retest, stop orta, hedef gun, bias yok | 7280 | -0.047 | -0.142 | 0.82 | 5996 | -0.051 | -0.153 | 0.81 |
| UTC, giriş retest, stop orta, hedef 2R, bias var | 3397 | -0.089 | -0.156 | 0.77 | 3118 | -0.033 | -0.106 | 0.85 |
| NY, giriş retest, stop orta, hedef gun, bias var | 4054 | -0.075 | -0.168 | 0.79 | 3537 | +0.039 | -0.061 | 0.92 |
| UTC, giriş piyasa, stop orta, hedef gun, bias var | 1915 | -0.073 | -0.180 | 0.75 | 1739 | -0.024 | -0.143 | 0.80 |
| UTC, giriş retest, stop orta, hedef gun, bias var | 3410 | -0.111 | -0.192 | 0.75 | 3127 | -0.071 | -0.158 | 0.79 |

48 adaydan örneklem dışında net R'si pozitif olan: 1; işlem sayısı, beklenti ve PF eşiğini birlikte geçen: 0.

