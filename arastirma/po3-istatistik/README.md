# PO3 İstatistik Ön Çalışması (Aşama 3)

Yol haritasının ([../yol-haritasi-po3-amd.md](../yol-haritasi-po3-amd.md)) 3. aşaması: PO3/AMD modelinin temel varsayımlarını, strateji kurmadan önce sayılarla sınamak.

## Ölçülen sorular

1. Londra penceresinde Asya aralığının bir tarafı süpürülünce fiyat diğer tarafa mı gidiyor (dönüş), yoksa aynı yönde mi devam ediyor? Rastgele hareketten (%50) farkı anlamlı mı?
2. Günün tepesi ve dibi en sık hangi saatte oluşuyor?
3. Süpürmeden sonra seviyenin içine geri kapanış (sahte kırılım onayı) sonucu iyileştiriyor mu?
4. Basit bias kuralı (önceki gün kapanışı, önceki günün orta noktasının üstünde mi) günün yönünü tahmin ediyor mu?

Her soru iki gün açılışı için ayrı ölçülür: 00:00 UTC ve New York gece yarısı (ICT seansları: Asya 20:00–24:00, Londra 02:00–05:00 New York saati).

## Dosyalar

| Dosya | Görevi |
|---|---|
| `ayarlar.py` | Coin listesi, seans saatleri, maliyet varsayımları |
| `veri_indir.py` | Binance herkese açık arşivinden 5 dakikalık vadeli mumları indirir (API anahtarı gerekmez) |
| `analiz.py` | Ölçümleri yapar, `sonuclar/rapor.md` ve `sonuclar/gunluk_olaylar.csv` üretir |
| `sentetik_kontrol.py` | Doğruluk kontrolü: rastgele veride dönüş oranının ~%50 çıktığını doğrular |

İndirilen ham veri `veri/` klasörüne yazılır ve depoya eklenmez.

## Yöntem notları

- **Yarış ölçümü:** Başlangıç fiyatından dönüş hedefine (Asya aralığının karşı tarafı) ve aynı uzaklıktaki ters seviyeye eşit mesafe vardır. Rastgele piyasada dönüş oranı ~%50'dir.
- **Geleceğe bakma yok:** Günün sınıflandırması yalnızca ilk süpürülen tarafa göre yapılır. İlk sürümde Londra penceresinin tamamı kullanılıyordu; rastgele veri testi bunun sonuçları devam yönüne kaydırdığını gösterdi ve düzeltildi.
- **Maliyetler:** İşlem gibi düşünülen ölçümde komisyon (%0,05 tek yön, doğrulanmalı), coin likiditesine göre kayma (%0,01–0,05 tek yön) ve fonlama payı (%0,01) düşülür.
- Bu çalışma bir strateji backtest'i değildir; kural seti v1'deki MSS ve FVG onaylarını içermez.
