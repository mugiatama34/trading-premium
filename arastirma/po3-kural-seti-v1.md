# PO3 Kural Seti v1

Tarih: 2026-10-03. Durum: backtest edildi, devam eşiklerini geçmedi (sonuç: [po3-backtest/sonuclar/ozet.md](po3-backtest/sonuclar/ozet.md)).

Bu belge, yol haritasının ([yol-haritasi-po3-amd.md](yol-haritasi-po3-amd.md)) Aşama 2'deki taslak kuralı bilgisayarın uygulayabileceği kesinlikte yazar. Taslakta açık bırakılan sayılar (N, X, tampon, kısa vadeli tepe tanımı) burada sabitlendi. Kod karşılığı: `po3-backtest/kurallar.py` ve `po3-backtest/backtest.py`.

## Kurallar

Örnek yükseliş senaryosu için yazılmıştır. Düşüş senaryosu bunun aynasıdır (yüksek ↔ alçak, üstü ↔ altı).

| Adım | Kural | 00:00 UTC varyantı | New York varyantı |
|---|---|---|---|
| Piyasa | 17 coinin USDT-M perpetual kontratı, 5 dakikalık mumlar; yalnızca hafta içi günler | | |
| Bias | Önceki günün kapanışı önceki günün orta noktasının ((yüksek + alçak) / 2) üstündeyse yükseliş, değilse düşüş. Önceki gün eksik veriliyse işlem yok | Gün 00:00 UTC | Gün NY gece yarısı |
| Birikim | Asya aralığı: penceredeki en yüksek ve en alçak fiyat | 00:00–06:00 UTC | 20:00–24:00 NY (önceki akşam) |
| Manipülasyon | Bias yükselişse Asya alçağının altına inen ilk mum (süpürme), bu pencerede başlamalı | 06:00–10:00 UTC | 02:00–05:00 NY |
| Geri kapanış | Süpürme mumu dahil en fazla **N = 3** mum içinde, bir mum Asya alçağının üstünde kapanır | | |
| MSS | Süpürmeden önce oluşmuş son kısa vadeli tepenin üstünde kapanış. Kısa vadeli tepe: her iki yanındaki **2** mumdan yüksek olan mum. MSS belirli saatten önce olmalı | 12:00 UTC'ye kadar | 07:00 NY'ye kadar |
| FVG | Süpürmenin en uç mumundan sonra, MSS mumunun bir sonrasına kadar oluşan ilk yükseliş FVG'si: 3. mumun alçağı > 1. mumun yükseği | | |
| Giriş | FVG'nin üst kenarına (3. mumun alçağı) limit alış emri. Emir, FVG ve MSS tamamlandıktan sonra **X = 12** mum (1 saat) açık kalır. Fiyat limitin **altına inerse** dolmuş sayılır (yalnızca değmek yetmez). Fiyat dolum olmadan hedefe giderse emir iptal | | |
| Stop | Süpürmenin en uç noktası − **0,1 × ATR(14, 5 dk)** | | |
| Hedef | İki seçenek ayrı test edildi: (a) Asya aralığının karşı tarafı (Asya yükseği), (b) sabit 2R. Hedef girişin ötesinde değilse işlem yok | | |
| Zaman çıkışı | Açık pozisyon bu saatte piyasa emriyle kapatılır | 20:00 UTC | 16:00 NY |
| Sınırlar | Coin başına günde en fazla 1 işlem. Aynı yöndeki açık pozisyonların toplam riski sermayenin en fazla %3'ü | | |
| Pozisyon boyutu | Risk = sermayenin %1'i (karşılaştırma için %2 de hesaplandı); pozisyon = risk tutarı / (giriş − stop) | | |

## Belirsiz durumlar için temkinli varsayımlar

5 dakikalık mumda fiyatın mum içindeki sırası bilinmez. Bu durumlarda sonucu kötüleştiren varsayım seçildi:

- Aynı mumda hem stop hem hedef görülürse **stop** sayılır.
- Dolum mumunda yalnızca stop kontrol edilir; hedef bir sonraki mumdan itibaren aranır.

## Maliyet modeli

| Kalem | Varsayım |
|---|---|
| Giriş | Limit emir, maker komisyonu %0,02 |
| Hedef çıkışı | Limit emir, maker komisyonu %0,02 |
| Stop ve zaman çıkışı | Piyasa emri, taker komisyonu %0,05 + coin bazında kayma (BTC/ETH %0,01; BNB/SOL/XRP %0,02; ETHFI/PENGU/MMT/CRV %0,05; diğerleri %0,03) |
| Fonlama | Pozisyon açıkken geçen her fonlama anında gerçek geçmiş fonlama oranı uygulanır (pozitif oran: uzun öder, kısa alır) |

Komisyon oranları Binance'in standart seviyesine göre varsayıldı ve doğrulanmadı.

## Kaldıraç

Kaldıraç ayrı bir karar değildir; pozisyon büyüklüğünden çıkar: gereken kaldıraç = risk yüzdesi / stop mesafesi yüzdesi. Backtestte stop mesafesinin medyanı %0,6–0,7 olduğundan %1 riskte medyan kaldıraç 1,4–1,7x, işlemlerin %90'ında 3,7x'in altındaydı (en yüksek 9,4x). İzole marjinde tasfiye mesafesi yaklaşık 1 / kaldıraçtır; 9,4x'te bile bu ~%10,6'dır ve en dar stoplu işlemin stop mesafesinin 3 katından fazladır. Yani kaldıraç işlem bazında gerektiği kadar seçilirse tasfiye riski stopun çok ötesinde kalır. Model maliyet sonrası negatif beklentili olduğu için getiriyi artıracak bir risk yüzdesi yoktur: %2 risk yalnızca kaybı ve düşüşü büyütür.
