# Kişisel Trading Yol Haritası: PO3 / AMD Modeli

Hazırlanma tarihi: 2026-10-03
Durum: Taslak; açık sorular 2026-10-03'te kullanıcı tarafından yanıtlandı

Bu belge, Elliott Wave denemesinden sonra PO3 (Power of 3) / AMD (Accumulation–Manipulation–Distribution) modelini önce sağlam şekilde öğrenmek, sonra ölçülebilir kurallara çevirip backtest ve paper trading ile sınamak için aşamalı bir plan sunar.

Projenin bağlayıcı kuralları bu planın her aşamasında geçerlidir: gerçek emir ve API anahtarı yok; yalnızca analiz, backtest ve paper trading; sonuçlar komisyon, kayma (slippage) ve fonlama maliyeti dahil raporlanır; işlem başına sermayenin %1–2'si risk; başlangıç sermayesi 10.000 $; kodlar Python; çıktılar `arastirma/` altında.

---

## Özet: 7 aşama

| Aşama | Konu | Tahmini süre | Bitti sayılması için |
|---|---|---|---|
| 0 | Elliott Wave'den ders ve hazırlık | 1 hafta | İşlem günlüğü şablonu hazır, veri kaynağı belli |
| 1 | PO3/AMD kavramlarını öğrenme | 2–3 hafta | 30 günlük grafik elle işaretlenmiş, kavram sözlüğü kendi cümlelerinle yazılmış |
| 2 | Kural seti v1 (mekanik tanımlar) | 1–2 hafta | Başka biri okuyunca aynı grafikte aynı işlemi bulabileceği kadar net kurallar |
| 3 | İstatistik ön çalışma | 1–2 hafta | "Asya aralığı süpürülünce dönüş olur mu?" sorusuna sayıyla cevap |
| 4 | Backtest (maliyetler dahil) | 2–4 hafta | Örneklem dışı (out-of-sample) testte maliyet sonrası pozitif beklenti ya da net "çalışmıyor" sonucu |
| 5 | Paper trading | en az 8–12 hafta / 50+ işlem | Paper sonuçları backtest ile tutarlı |
| 6 | Değerlendirme ve karar | 1 hafta | Devam / düzelt / bırak kararı yazılı |

Süreler yön göstermek içindir; acele etmek yerine her aşamanın "bitti" ölçütünü sağlamak önemlidir.

---

## Aşama 0: Elliott Wave'den çıkarılacak ders

Elliott Wave'in çoğu kişide işe yaramamasının ana sebebi yöntemin **öznel** olmasıdır:

- Aynı grafik birden fazla geçerli dalga sayımına izin verir. Sayım yanlış çıkınca "aslında bu dalga 4'ün uzantısıymış" diye yeniden sayılır. Yöntem hiçbir zaman açıkça "yanıldı" demez, bu yüzden test edilemez.
- Geçmiş grafikte sayım çok net görünür (geriye dönük bakış yanılgısı), canlı piyasada ise sağ kenarda hangi dalgada olduğunu bilmek çok zordur.
- Giriş, stop ve hedef kuralları kişiye göre değişir; bu da sonuçların tekrarlanabilir olmamasına yol açar.

**Ders:** Sorun büyük ihtimalle senin değil, yöntemin ölçülemez olmasıdır. **Aynı tuzak PO3/AMD ve genel olarak ICT/SMC kavramları için de geçerlidir.** "Manipülasyon" ve "likidite süpürmesi" geçmiş grafikte her yerde görülebilir. Bu yüzden bu yol haritasının en önemli kuralı şudur:

> Bir kavram, bilgisayarın da aynı şekilde bulabileceği bir tanıma dönüştürülemiyorsa, ona dayanarak işlem yapılmaz.

Ayrıca dürüst bir not: ICT/SMC kavramlarının kâr ettirdiğine dair bağımsız, hakemli bir kanıt yoktur. Bu, modelin işe yaramadığı anlamına gelmez; ama kanıtın senin kendi testlerinden gelmesi gerektiği anlamına gelir.

### Hazırlık işleri

- **İşlem günlüğü:** Her işaretleme ve paper işlem için tarih, seans, bias (yön beklentisi), süpürülen likidite, giriş, stop, hedef, sonuç (R cinsinden), ekran görüntüsü ve "kurala uydu mu?" alanları.
- **Veri:** Binance'in herkese açık geçmiş veri arşivi (data.binance.vision) API anahtarı gerektirmez. İzlenecek coin listesinin (BTC, ETH, SOL, ADA, LINK, ETHFI, DOGE, PENGU, MMT, AVAX, DOT, LTC, CRV, BNB, NEAR, XRP, SUI) USDT vadeli (perpetual) 1 dakikalık mumları ve fonlama oranı (funding rate) geçmişi indirilir.
- **Grafik aracı:** TradingView ücretsiz sürüm, UTC saat diliminde ayarlı.

---

## Aşama 1: PO3/AMD'nin incelikleri

### 1.1 Temel fikir

Her mumun dört fiyatı vardır: açılış (O), en yüksek (H), en düşük (L), kapanış (C). PO3 fikri, güçlü bir yükseliş mumunun genellikle şu sırayla oluştuğunu söyler:

1. **Accumulation (Birikim):** Açılış etrafında dar, yatay bir hareket. Büyük oyuncular pozisyon toplar.
2. **Manipulation (Manipülasyon / "Judas swing"):** Fiyat gerçek yönün tersine, açılışın altına iner. Bu düşüş, stopları tetikler ve yanlış yöne işlem açanları içeri çeker. Mumun en düşük noktası (L) burada oluşur.
3. **Distribution (Dağıtım / genişleme):** Fiyat asıl yönde hızla hareket eder ve mum, açılıştan uzakta, en yükseğe yakın kapanır.

Düşüş mumu için tam tersi: açılışın üstüne sahte bir yükseliş, sonra sert düşüş.

Bu yapı her zaman diliminde aranabilir (haftalık, günlük, 4 saatlik, 1 saatlik). En yaygın kullanım: **günlük mumu** PO3 olarak düşünmek ve gün içi seansları bu üç evreyle eşleştirmek.

### 1.2 Seans yapısı (kripto için uyarlama)

Kripto 7/24 işlem görür; ama hacim ve volatilite yine geleneksel piyasa seanslarına göre şekillenir. Saatler UTC'dir; yaz/kış saati geçişinde 1 saat kayabilir, kural setinde sabitlenmelidir.

| Evre | Tipik seans (UTC) | Ne beklenir |
|---|---|---|
| Accumulation | Asya: ~00:00–06:00 | Dar aralık. **Asya yükseği ve alçağı** günün ilk likidite seviyeleri olur. |
| Manipulation | Londra açılışı: ~07:00–10:00 | Asya aralığının bir tarafının süpürülmesi (sahte kırılım). |
| Distribution | New York: ~12:00–16:00 | Asıl yönde genişleme; çoğu zaman Asya aralığının diğer tarafına ya da önceki gün yükseği/alçağına gider. |

Önemli incelikler:

- **"Gün açılışı" hangisi?** Kripto günlük mumu 00:00 UTC'de açılır. ICT ise New York gece yarısı açılışını (yaklaşık 04:00/05:00 UTC) kullanır. İkisini de test et, birini seç ve sabit tut.
- **Hafta sonları** düşük hacimlidir; PO3 yapısı daha zayıf olabilir. Kural setinde ayrı ele alınmalı (başlangıçta hafta sonunu dışarıda bırakmak makul).
- **Haber günleri** (ABD enflasyon verisi CPI, Fed faiz kararı FOMC) seans düzenini bozar. Bu günler ayrı etiketlenmeli.

### 1.3 Likidite: modelin kalbi

"Likidite" burada, birçok stop emrinin biriktiği fiyat seviyeleri demektir. Fiyat bu seviyelere çekilir çünkü büyük emirlerin karşı tarafı orada bulunur.

- **BSL (buy-side liquidity):** Belirgin tepelerin üstü (açığa satanların stopları).
- **SSL (sell-side liquidity):** Belirgin diplerin altı (alıcıların stopları).
- Tipik seviyeler: Asya yükseği/alçağı, önceki gün yükseği/alçağı (PDH/PDL), önceki hafta yükseği/alçağı, **eşit tepeler / eşit dipler** (çift tepe gibi görünen yerler).
- **Süpürme (sweep) ile kırılım (breakout) farkı:** Süpürmede fiyat seviyeyi geçer ama kısa sürede geri döner ve seviyenin içinde kapanır. Kırılımda ise seviyenin dışında kalır ve devam eder. Bu ayrım, modelin en kritik ve en kolay yanılınan kısmıdır.
- **Draw on liquidity (likiditenin çekimi):** Fiyatın büyük resimde hangi likidite havuzuna doğru gittiği. Günün yön beklentisi (bias) buna göre kurulur.

### 1.4 Manipülasyonun bittiğini gösteren onaylar

Sadece "süpürüldü" diye işleme girmek en sık yapılan hatadır. Süpürmeden sonra yönün döndüğüne dair onay aranır:

- **Displacement (güçlü itki):** Süpürmeden sonra ortalamanın belirgin üstünde büyüklükte, tek yönlü mumlar.
- **MSS / CHoCH (piyasa yapısı değişimi):** Alt zaman diliminde (örneğin 5 dakika), süpürmeden sonra oluşan son kısa vadeli tepenin üstünde kapanış (yükseliş senaryosu için).
- **FVG (fair value gap / dengesiz fiyat boşluğu):** Üç mumluk dizide 1. mumun yükseği ile 3. mumun alçağı arasında kalan, fiyatın hızlı geçtiği boşluk. Giriş için sık kullanılan geri çekilme bölgesidir.
- **Order block:** Güçlü itkiden önceki son ters yönlü mum. FVG'ye göre tanımı daha esnektir, bu yüzden testte ikinci planda tutulmalı.
- **OTE (optimal trade entry):** İtki hareketinin %62–79 Fibonacci geri çekilme bölgesi.
- **Premium / discount:** Günlük aralığın üst yarısı pahalı (premium), alt yarısı ucuz (discount). Yükseliş senaryosunda alım discount bölgesinde aranır.
- **SMT divergence:** BTC yeni dip yaparken ETH yapmıyorsa (ya da tersi), süpürmenin sahte olduğuna işaret sayılır. Kripto için ölçülebilir ve test edilmeye değer bir onaydır.

### 1.5 Sık yapılan hatalar

1. **Geriye dönük etiketleme:** Kapanmış bir günde AMD'yi her zaman bulursun. Asıl soru, Londra seansında sağ kenardayken bunu bilip bilemeyeceğindir.
2. **Her hareketi manipülasyon saymak:** Gerçek kırılımı süpürme sanıp trende karşı işlem açmak.
3. **Onaysız giriş:** Süpürme anında, MSS ve displacement beklemeden girmek.
4. **Büyük resmi (HTF bias) yok saymak:** Günlük/4 saatlik yön yukarıyken düşüş PO3'ü aramak.
5. **Seans dışında işlem:** Model zamana bağlıdır; kill zone dışındaki kurulumlar genelde zayıftır.
6. **Çok dar stop:** Kripto vadelide komisyon + kayma bir giriş-çıkış için yaklaşık %0,1–0,15 tutabilir. %0,3'lük bir stopta bu, riskin üçte birini maliyete gömer. Dar stoplu modeller kâğıt üzerinde iyi, maliyet sonrası kötü görünür.
7. **Aşırı filtre:** Her yeni kavramı (OB, FVG, OTE, SMT, kill zone...) filtre olarak eklemek, işlem sayısını çok düşürür ve geçmişe aşırı uyum (overfitting) yaratır.
8. **Birden fazla kaynak karıştırmak:** Farklı eğitmenlerin farklı tanımları karıştırıldığında kurallar tutarsızlaşır. Tek tanım seç ve yaz.

### 1.6 Bu aşamadaki pratik çalışma

- Kavram sözlüğünü **kendi cümlelerinle** yaz (`arastirma/po3-kavram-sozlugu.md`).
- BTCUSDT için **30 günü** günlük olarak elle işaretle: Asya aralığı, hangi taraf süpürüldü, MSS oldu mu, gün nasıl kapandı.
- Bunu "sağ kenar" disipliniyle yap: grafiği Londra açılışında durdur (TradingView "bar replay"), karar ver, sonra ileri sar. Kararını sonucu görmeden günlüğe yaz.
- Hedef: Kaç günde net bir PO3 yapısı vardı, kaçında yoktu, kaçında yanlış tarafı tahmin ettin? Bu sayılar sonraki aşamalar için ilk ipucudur.

---

## Aşama 2: Kural seti v1

Amaç, Aşama 1'de öğrendiklerini **bilgisayarın uygulayabileceği** kurallara çevirmektir. Aşağıdaki bir başlangıç taslağıdır; parametreler sonradan test edilecek.

| Bileşen | Taslak kural (v1) |
|---|---|
| Piyasa | BTC, ETH, SOL, ADA, LINK, ETHFI, DOGE, PENGU, MMT, AVAX, DOT, LTC, CRV, BNB, NEAR, XRP, SUI (USDT perpetual); hafta içi günler |
| Bias | Önceki günün kapanışı, önceki günün orta noktasının üstündeyse yükseliş, altındaysa düşüş (basit ve ölçülebilir; alternatifler sonra test edilir) |
| Accumulation | Asya aralığı = 00:00–06:00 UTC en yüksek ve en düşük |
| Manipulation | 06:00–10:00 UTC arasında, bias'a ters taraftaki Asya seviyesinin süpürülmesi: fiyat seviyeyi geçer, 5 dakikalık mum en fazla N mum içinde seviyenin içine geri kapanır |
| Onay | Süpürmeden sonra 5 dakikalıkta, son kısa vadeli tepe/dip seviyesinin ötesinde kapanış (MSS) |
| Giriş | MSS hareketinin oluşturduğu ilk FVG'ye limit emir; X mum içinde dolmazsa iptal |
| Stop | Süpürme ucunun ötesi + küçük tampon (ör. 0,1 × ATR) |
| Hedef | Asya aralığının karşı tarafı veya sabit 2R; ikisi de test edilir |
| Zaman çıkışı | 20:00 UTC'de açık pozisyon kapatılır |
| Günlük sınır | Günde en fazla 1 işlem |
| Pozisyon boyutu | Risk = sermayenin %1'i; pozisyon büyüklüğü = risk tutarı / (giriş − stop mesafesi) |

**Kaldıraç nasıl belirlenecek?** Kaldıraç ayrı bir karar değil, pozisyon büyüklüğünün sonucudur. Örnek: 10.000 $ sermaye, %1 risk = 100 $; stop mesafesi %0,5 ise pozisyon 20.000 $ olur, yani en az 2x kaldıraç gerekir. Her model için şu yazılı gerekçe çıkarılacak:

- Stop mesafelerinin dağılımına göre gereken kaldıraç aralığı,
- Tasfiye (liquidation) fiyatının stopun çok ötesinde kalması şartı (izole marjin, tasfiye mesafesi en az stop mesafesinin 3 katı),
- Beklenen getiri / maksimum düşüş oranını en iyi yapan risk yüzdesi (%1 ile %2 arasında).

Kural setinin çıktısı: `arastirma/po3-kural-seti-v1.md`. Kural değiştikçe sürüm numarası artırılır (v1.1, v2...) ve neyin neden değiştiği yazılır.

---

## Aşama 3: İstatistik ön çalışma (strateji değil, soru)

Backtest'ten önce modelin temel varsayımlarını tek tek sayılarla sına. Bunlar ucuz, hızlı ve çok öğreticidir:

1. Asya aralığının bir tarafı Londra'da süpürüldüğünde, gün içinde diğer tarafa gitme oranı nedir? Rastgele bir günle karşılaştırıldığında anlamlı fark var mı?
2. Günlük mumların yüzde kaçı "açılışın ters tarafında dip/tepe yapıp, açılıştan uzakta kapanma" (PO3) şeklindedir? Günün dip veya tepesi en sık hangi saatte oluşuyor?
3. Süpürme + MSS olan günler ile süpürme olup MSS olmayan günler arasında sonuç farkı var mı?
4. Bias kuralı, günün yönünü yazı-turadan daha iyi tahmin ediyor mu?

Bu soruların cevabı "fark yok" çıkarsa, backtest'e geçmeden kural seti gözden geçirilir. Bu, para ve zaman kaybetmeden yapılan en değerli eleme adımıdır.

Çıktı: `arastirma/po3-istatistik/` altında Python betikleri ve sonuç raporu.

---

## Aşama 4: Backtest

### Maliyet modeli (zorunlu)

- **Komisyon:** Binance USDT-M vadeli için standart seviyede maker yaklaşık %0,02, taker yaklaşık %0,05 (backtest öncesi güncel oranlar doğrulanmalı).
- **Kayma:** Piyasa emirleri ve stoplar için işlem başına en az 1–2 tik + volatiliteye bağlı ek; limit girişlerde "dokundu ama dolmadı" ihtimali hesaba katılmalı (fiyat seviyeyi sadece değmişse dolmuş sayma).
- **Fonlama:** Pozisyon 00:00, 08:00, 16:00 UTC fonlama anlarında açıksa geçmiş fonlama oranı uygulanır.
- Sonuçlar hem maliyet öncesi hem maliyet sonrası raporlanır; karar maliyet sonrasına göre verilir.

### Test düzeni

- **Veri:** En az 3–4 yıl (farklı piyasa dönemleri: boğa, ayı, yatay).
- **Ayrım:** Verinin ilk ~%60'ı geliştirme (in-sample), sonrası dokunulmayan test (out-of-sample). Daha sonra walk-forward (kayan pencere) testi.
- **Kıyas (baseline):** Aynı seans, aynı stop ve hedef ama rastgele yönlü girişler. Model bu rastgele versiyonu anlamlı şekilde geçemiyorsa avantajı yoktur.
- **Sağlamlık:** Parametreleri biraz değiştirince (ör. Asya bitişi 05:00 / 06:00 / 07:00) sonuç çöküyorsa model kırılgandır.
- **Monte Carlo:** İşlem sırasını karıştırarak olası en kötü düşüş (drawdown) dağılımı.

### Raporlanacak ölçüler

İşlem sayısı, kazanma oranı, ortalama kazanç/kayıp (R cinsinden), beklenti (expectancy, işlem başına ortalama R), profit factor, maksimum düşüş, en uzun kayıp serisi, yıllık getiri, maliyetlerin brüt kâra oranı, seans/gün/coin bazında kırılım.

### Devam etmek için eşikler (2026-10-03'te kabul edildi)

- Örneklem dışı testte en az 100 işlem,
- Maliyet sonrası beklenti ≥ +0,15R,
- Profit factor ≥ 1,3,
- %1 riskle maksimum düşüş ≤ %20,
- Rastgele kıyas modelinden anlamlı şekilde iyi,
- Parametre değişikliklerinde sonuç kabaca korunuyor.

Çıktı: `arastirma/po3-backtest/` altında kod ve rapor.

---

## Aşama 5: Paper trading

- Backtest eşiklerini geçen kural seti **değiştirilmeden** paper trading ile izlenir. Gerçek emir verilmez, API anahtarı kullanılmaz; canlı fiyat herkese açık veriden alınır ya da işlemler günlüğe elle kaydedilir.
- Süre: en az 8–12 hafta **ve** en az 50 işlem.
- Her işlem için: kurala uyuldu mu, dolum fiyatı backtest varsayımına göre ne kadar farklı, hissettiğin duygu (korku, FOMO).
- Karşılaştırma: Paper sonuçları backtest'in beklenti aralığında mı? Kazanma oranı ve ortalama R çok sapıyorsa backtest'teki varsayımlar (özellikle dolum ve kayma) gözden geçirilir.

---

## Aşama 6: Değerlendirme ve karar

Üç olası sonuç:

1. **Devam:** Paper sonuçları backtest ile tutarlı ve maliyet sonrası pozitif. Gerçek parayla kullanma kararı yalnızca senindir; bu durumda bile çok küçük sermaye ve %0,5 risk ile başlamak önerilir.
2. **Düzelt:** Fikir umut verici ama bir bileşen zayıf (ör. bias kuralı). Yeni kural sürümü yazılır ve Aşama 3'ten tekrar geçer.
3. **Bırak:** Maliyet sonrası avantaj yok. Bu da başarılı bir sonuçtur: para kaybetmeden yanlış bir yolu elemiş olursun. Öğrenilen altyapı (veri, backtest, günlük) bir sonraki modelde aynen kullanılır.

---

## Bu haftadan başlamak için ilk 5 adım

1. İşlem günlüğü şablonunu oluştur (tablo veya not uygulaması, yukarıdaki alanlarla).
2. TradingView'ı UTC'ye ayarla; BTCUSDT 15 dakikalıkta Asya aralığını işaretleyen basit bir alışkanlık edin.
3. Son 30 iş günü için bar replay ile "sağ kenar" işaretleme çalışmasına başla.
4. Kavram sözlüğünü kendi cümlelerinle yazmaya başla; anlamadığın kavramı not et.
5. Hazır olduğunda, Aşama 3'teki ilk istatistik sorusu (Asya süpürmesi sonrası karşı tarafa gitme oranı) için Python çalışmasını iste.

---

## Verilen kararlar (2026-10-03)

- **Gün açılışı:** 00:00 UTC ve New York gece yarısı açılışı ikisi de test edilir; sonuçlar yan yana raporlanır.
- **Coin listesi:** BTC, ETH, SOL, ADA, LINK, ETHFI, DOGE, PENGU, MMT, AVAX, DOT, LTC, CRV, BNB, NEAR, XRP, SUI.
- **Devam eşikleri:** Aşama 4'teki eşikler kabul edildi.

### Coin listesiyle ilgili notlar

- **Geçmiş verinin uzunluğu farklı:** ETHFI (2024), PENGU (2024 sonu) ve MMT (2025) gibi yeni coinlerde 3–4 yıllık veri yok. Her coin kendi mevcut geçmişiyle test edilir ve geçmiş süresi raporda belirtilir. Kısa geçmişli coinlerin sonuçları, tek başına karar vermek için yeterli sayılmaz; tüm listenin birleşik sonucuna katkı olarak değerlendirilir.
- **Vadeli işlem bulunurluğu:** Her coinin Binance USDT-M perpetual kontratı ve veri arşivi olduğu veri indirme aşamasında doğrulanır; olmayan coin raporda not edilir.
- **Likidite farkı:** Küçük coinlerde kayma (slippage) daha yüksektir. Maliyet modeli coin bazında, işlem hacmine göre ayarlanır.
- **SMT onayı:** Ana çift BTC–ETH olarak kalır; diğer coinler için SMT ayrıca ele alınmaz.
- **Toplam risk:** Aynı anda birden fazla coinde sinyal çıkabilir. Bu coinler büyük ölçüde birlikte hareket ettiği için aynı yöndeki açık pozisyonların toplam riski sermayenin en fazla %3'ü ile sınırlanır (2026-10-03'te kabul edildi).
