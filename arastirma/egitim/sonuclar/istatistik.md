# Eğitim İçin Basit Veri Kontrolleri

Veri: Binance USDT-M vadeli, 1 saatlik mumlar, 2023-01 → 2026-08, BTC, ETH, SOL. Kod: `kod/istatistik.py`.

Bunlar strateji testi değil, kavramların veride iz bırakıp bırakmadığına dair ilk bakıştır. Tek bir mekanik tanım kullanıldı; farklı tanımlar farklı sonuç verebilir.

## 1) Eşit tepe/dipler gerçekten "mıknatıs" mı? (Modül 2)

Soru: Eşit tepe/dip (iki tepe/dip %0,1 içinde) üzerindeki likidite, tek bir swing tepe/dibe göre daha sık mı alınıyor? Ölçüt: seviyenin 48 saat içinde aşılma oranı.

| Uzaklık | Eşit seviye | Tek seviye |
|---|---|---|
| 0-1 ATR | %87.8 (n=739) | %87.2 (n=6374) |
| 1-2 ATR | %77.9 (n=890) | %73.0 (n=7507) |
| 2-4 ATR | %62.7 (n=391) | %53.7 (n=3161) |

## 2) Önceki gün tepe/dip süpürmesi ve giriş biçimleri (Modül 2, 5, 6)

Süpürme: mum önceki günün tepesini (PDH) fitille aşıp altında kapatıyor (PDL için tersi); günün ilk aşımı sayılır. Kırılım: aşan mum dışarıda kapatıyor.
Getiriler beklenen dönüş yönünde, 12 saat sonrası, maliyetsiz. R değerleri maliyet dahil (net).

| Coin | Süpürme sayısı | 12s dönüş yönü oranı | Ort. 12s getiri (süpürme) | Ort. 12s getiri (kırılım, aynı yön) | Hemen ters giriş net R (brüt) | Onaylı giriş: işlem / net R (brüt) |
|---|---|---|---|---|---|---|
| BTC | 625 | %56.6 | %+0.068 | %-0.038 | -0.461 (-0.007) | 67 / -0.001 (+0.088) |
| ETH | 633 | %57.5 | %-0.027 | %+0.029 | -0.265 (+0.017) | 61 / -0.195 (-0.125) |
| SOL | 628 | %49.8 | %-0.093 | %+0.170 | -0.179 (+0.091) | 44 / +0.135 (+0.177) |

Üç coin birlikte: hemen ters giriş 1886 işlem, net -0.302R (%95 GA -0.416 … -0.187); onaylı giriş 172 işlem, net -0.035R (%95 GA -0.138 … +0.067).

Medyan stop mesafesi: hemen ters girişte %0.68, onaylı girişte %2.66. Gidiş-dönüş maliyeti yaklaşık %0.155 olduğundan dar stop, maliyetin R cinsinden büyümesine yol açar.

Not: Kırılım sütunu süpürmeyle aynı yönde ölçülür; negatifse kırılımdan sonra fiyat kırılım yönünde devam etme eğilimindedir (PO3 çalışmasındaki devam eğilimiyle tutarlı).

## 3) FVG'ler doldurulur mu, dokunulunca tepki verir mi? (Modül 3, 4)

1 saatlik, fiyatın en az %0,1'i büyüklüğünde 11820 FVG.

| Ölçüt | Sonuç |
|---|---|
| 24 saatte FVG orta noktasına dönüş | %77.6 |
| 24 saatte aynı uzaklıktaki ayna seviyeye gidiş (kıyas) | %77.9 |
| Orta noktaya dokunduktan sonra simetrik hedefin stoptan önce gelmesi (rastgele ≈ %50, maliyetsiz) | %50.5 (n=9008) |

## 4) Premium / discount: ucuz bölgeden alım daha mı iyi? (Modül 5)

Fiyatın önceki gün aralığındaki konumu ve sonraki 24 saatin ortalama getirisi (üç coin, 4 saatte bir örnek, maliyetsiz).

| Bölge | Örnek | Ort. 24s getiri | Yükselme oranı |
|---|---|---|---|
| 1) PDL altı | 2780 | %+0.056 | %51.3 |
| 2) Discount (0-%25) | 3321 | %+0.212 | %54.6 |
| 3) Discount (%25-50) | 5318 | %+0.118 | %52.3 |
| 4) Premium (%50-75) | 5438 | %+0.163 | %51.1 |
| 5) Premium (%75-100) | 3798 | %+0.183 | %48.3 |
| 6) PDH üstü | 3411 | %+0.325 | %49.4 |

