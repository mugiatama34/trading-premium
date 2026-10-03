# PO3 İstatistik Ön Çalışması: Özet ve Yorum

Tarih: 2026-10-03. Ayrıntılı tablolar: [rapor.md](rapor.md). Günlük ham ölçümler: `gunluk_olaylar.csv`.

## Kısa sonuç

**Ölçülen haliyle PO3/AMD varsayımı veride yok; maliyetler dahil hiçbir eşik geçilmedi.** Londra'da Asya aralığının bir tarafı süpürüldükten sonra fiyat karşı tarafa dönmüyor, hafifçe aynı yönde devam ediyor. Bu sonuç iki gün açılışında da, 17 coinin neredeyse tamamında ve her yıl için aynı.

## Veri

- Binance USDT-M vadeli 5 dakikalık mumlar, 2021-01 → 2026-09 (yeni coinler listelendikleri günden itibaren).
- 17 coinin hepsinin vadeli kontratı var. Kısa geçmişliler: SUI (2023-05), ETHFI (2024-03), PENGU (2024-12), MMT (2025-11, yalnızca ~330 gün).
- Toplam ~30.400 coin-günü (her varyant için).

## Devam eşikleri ile karşılaştırma (Yarış 2, tüm coinler, maliyetler dahil)

| Ölçüt | Eşik | 00:00 UTC | New York gece yarısı | Sonuç |
|---|---|---|---|---|
| İşlem başına ortalama net R | ≥ +0,15R | −0,100R | −0,147R | Geçmedi |
| Profit factor | ≥ 1,3 | 0,79 | 0,73 | Geçmedi |
| Maks. düşüş (%1 risk) | ≤ %20 | ~%100 | ~%100 | Geçmedi |
| Rastgeleden iyi mi? | %50'nin üstü | %48,6 dönüş | %47,1 dönüş | Hayır (biraz altında) |

Maliyetler: komisyon %0,05 tek yön (doğrulanmalı), coin likiditesine göre kayma %0,01–0,05 tek yön, fonlama payı %0,01. Ortalama durma mesafesi %2,6–3,2 olduğu için maliyet işlem başına yaklaşık 0,08–0,10R tutuyor. Maliyetsiz (brüt) sonuç da sıfırın altında: −0,018R ve −0,049R.

## Soru soru

1. **Süpürme sonrası dönüş:** Onaysız (Yarış 1) dönüş oranı %48,8 (UTC) ve %48,2 (NY). İkisi de %50'den anlamlı şekilde düşük (p < 0,01), yani hafif bir **devam** eğilimi var, dönüş yok.
2. **Günün tepe ve dibinin saati:** Tepe ve dipler en sık günün ilk ve son saatinde oluşuyor (00:00 ve 23:00). Bu kısmen matematiksel bir etki: rastgele harekette de uç noktalar günün başına ve sonuna yığılır. New York varyantında 09:00–10:00 (NY açılışı) çevresinde küçük bir artış var, ama Londra penceresinde (02:00–05:00) belirgin bir yığılma yok.
3. **Geri kapanış onayı:** Sonucu iyileştirmiyor. Onaylı dönüş oranı %48,6 (UTC) ve %47,1 (NY), onaysızdan bile biraz kötü.
4. **Bias kuralı:** Önceki günün kapanışı orta noktanın üstündeyse "yukarı" kuralı, günün yönünü %48,8 ve %48,3 doğru tahmin ediyor. Bu da yazı-turanın biraz altında.

Coin bazında hiçbir coin, maliyet sonrası anlamlı pozitif sonuç vermedi. En az kötü olanlar ETHFI, PENGU (UTC) ve MMT (NY). Bunların örneklemleri küçük, güven aralıkları sıfırı içeriyor; tek başına bir avantaj işareti sayılmamalı.

## Ters yön (devam) işlenebilir mi?

Devam eğilimi istatistiksel olarak var ama küçük: brüt avantaj yalnızca +0,02R (UTC) ile +0,05R (NY) arası. İşlem başına ~0,08–0,10R'lik maliyetten sonra bu da negatife dönüyor. Bu yüzden ters yönü işlemek de bu haliyle para kazandırmıyor.

## Sınırlar

- Bu bir strateji backtest'i değil. Kural seti v1'deki MSS (piyasa yapısı kırılımı) ve FVG (fiyat boşluğu) onayları burada yok. Ölçülen şey, modelin dayandığı temel varsayım.
- Stop ve hedef eşit uzaklıkta (1R'ye 1R). Farklı hedef oranları veya giriş filtreleri sonucu değiştirebilir, ama temel varsayımın veride olmaması bunu zorlaştırır.
- Maksimum düşüş hesabında aynı gün birden fazla coinde işlem açılabiliyor. %3 toplam açık risk sınırı uygulanmadı. Sınır uygulansa düşüş yavaşlar ama ortalama negatif kaldığı için yön değişmez.
- Komisyon oranı (%0,05 taker) Binance'in standart seviyesine göre varsayıldı ve doğrulanmadı.
- Analiz `analiz_saf.py` ile yapıldı, çünkü bu ortamda pandas ve scipy kurulamadı. Ölçüm mantığı `analiz.py` ile aynı. Rastgele veri kontrolü geçti: dönüş oranı %49,7–50,1 ve brüt R ≈ 0. Bu, ölçüm yönteminde geleceğe bakma hatası olmadığını gösteriyor. `analiz.py` pandas ile henüz çalıştırılıp karşılaştırılmadı.

## Önerilen sonraki adım

Yol haritasının eşiklerine göre PO3/AMD'nin bu basit hali için karar: **devam etme**. Seçenekler:

1. Kural seti v1'i MSS ve FVG onaylarıyla tam backtest etmek. Temel varsayım zayıf olduğundan beklenti düşük, ama ICT'nin asıl iddiası bu onaylarla ilgili.
2. Bulunan küçük **devam** eğilimini, daha düşük maliyetli girişlerle (limit emir ve maker komisyonu) ya da daha uzak hedeflerle araştırmak.
3. PO3'ü bırakıp başka bir model ailesine geçmek.

Karar kullanıcıya aittir.
