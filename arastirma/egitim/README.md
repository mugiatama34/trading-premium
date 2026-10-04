# SMC / ICT ve Price Action Eğitimi

Bu klasör, SMC (Smart Money Concepts), ICT (Inner Circle Trader), buyside/sellside likidite, saatlik bozulma, PD array, immediate reverse execution ve price action konularını başlangıç-orta seviyeye uygun şekilde, sırayla öğretmek için hazırlandı.

Eğitimin iki amacı var:

1. Bu kavramları **doğru ve tutarlı** öğrenmek: grafiği bu dille okuyabilmek.
2. Her kavramda **hangi kısmın test edilmiş, hangi kısmın topluluk anlatısı** olduğunu ayırabilmek. Bu projede PO3/AMD üzerine yapılan backtestler (PR #3) güvenilir bir avantaj bulamadı; bu eğitim de kavramları "kanıtlanmış kazanç yöntemi" gibi değil, test edilecek hipotezler olarak sunuyor.

## Modüller

Sırayla okunması önerilir; her modül bir öncekine dayanır.

| # | Modül | Konu |
|---|---|---|
| 1 | [Price action ve piyasa yapısı](01-price-action.md) | Mum okuma, swing tepe/dip, HH/HL/LH/LL, BOS/CHoCH, zaman dilimleri |
| 2 | [Likidite: BSL ve SSL](02-likidite-bsl-ssl.md) | Buyside/sellside likidite, eşit tepe/dip, süpürme, ERL/IRL |
| 3 | [SMC](03-smc.md) | BOS/CHoCH/MSS, order block, FVG, inducement, mitigation |
| 4 | [ICT kavramları](04-ict.md) | IPDA, killzone, PO3/AMD, OTE, SMT, terimler sözlüğü |
| 5 | [Premium, discount ve PD array](05-pd-array.md) | Equilibrium, PD array türleri, breaker, PD array matrisi |
| 6 | [Saatlik bozulma](06-saatlik-bozulma.md) | 1 saatlik yapı kırılımı ile onay, kontrol listesi |
| 7 | [Immediate reverse execution](07-immediate-reverse-execution.md) | Hemen ters giriş, onaylı giriş, IFVG, maliyet etkisi |
| 8 | [Birleştirme, risk ve test planı](08-birlestirme-ve-risk.md) | İşlem planı, pozisyon/kaldıraç hesabı, günlük, yol haritası |

Her modülün yapısı aynı: tanım → iddia edilen mantık → grafikte nasıl tanınır (metin grafikleriyle) → veride ne gördük → sık yapılan hatalar → nasıl test ederiz → kendini sına (cevaplar açılır kutuda).

## Gerçek veri bölümleri

- [`sonuclar/ornekler.md`](sonuclar/ornekler.md): BTCUSDT 1 saatlik Binance verisinden kurallarla otomatik seçilmiş grafik örnekleri (piyasa yapısı, eşit dip süpürmesi, işe yarayan ve stop olan birer saatlik bozulma kurulumu).
- [`sonuclar/istatistik.md`](sonuclar/istatistik.md): BTC, ETH, SOL 1 saatlik verisinde (2023-01 → 2026-08) dört iddianın basit kontrolü: eşit tepe/dip likiditesi, PDH/PDL süpürmesi ve giriş biçimleri, FVG doldurma ve tepki, premium/discount.
- [`kod/`](kod/): Bu sonuçları üreten Python kodu (yalnızca standart kütüphane; veri data.binance.vision'dan indirilir, API anahtarı kullanılmaz). `kavramlar.py` kavramların mekanik tanımlarını içerir ve sonraki backtestlerde yeniden kullanılabilir.

## Kısaca ne bulduk?

| Kavram | Durum |
|---|---|
| Eşit tepe/dip likiditesi | Kısmen destekleniyor (uzak seviyeler daha sık alınıyor) |
| Süpürme sonrası dönüş | Desteklenmiyor |
| FVG doldurma / tepki | Rastgele seviyeden farkı yok |
| Premium / discount | Belirsiz (ortalamaya dönüş ve momentum karışık) |
| Saatlik bozulma onayı | Onaysız girişten çok daha iyi, ama tek başına ≈ 0R |
| Hemen ters giriş | Dar stop ve maliyetler yüzünden net −0,30R |

Ayrıntılar Modül 8.7'de.

## Nasıl çalışmalı?

1. Bir modülü oku, metin grafiklerini kendi grafiğinde (TradingView, BTCUSDT.P, 1 saatlik) bul.
2. "Kendini sına" sorularını cevaplara bakmadan cevapla.
3. Sağ tarafı kapatarak (Bar Replay) kavramı canlıymış gibi işaretle; sonradan doğru mu çıktı not al.
4. Modül 8'deki işlem günlüğünü kâğıt üzerinde tut.
5. Bir kavram ilgini çektiyse "Nasıl test ederiz?" bölümündeki adımlarla backtest'e dönüştürmeyi iste.

## Kısaltmalar sözlüğü

| Kısaltma | Açılım | Türkçe |
|---|---|---|
| BSL / SSL | Buyside / Sellside Liquidity | Alış / satış tarafı likidite |
| PDH / PDL | Previous Day High / Low | Önceki gün tepesi / dibi |
| BOS | Break of Structure | Yapı kırılımı (trend yönünde) |
| CHoCH | Change of Character | Karakter değişimi (ters yönde ilk kırılım) |
| MSS | Market Structure Shift | Piyasa yapısı değişimi (ICT) |
| OB | Order Block | Emir bloğu |
| FVG | Fair Value Gap | Adil değer boşluğu |
| IFVG | Inversion FVG | Ters dönmüş FVG |
| CE | Consequent Encroachment | FVG'nin orta noktası |
| BPR | Balanced Price Range | Dengelenmiş fiyat aralığı |
| OTE | Optimal Trade Entry | %62–79 geri çekilme girişi |
| PO3 / AMD | Power of 3 / Accumulation-Manipulation-Distribution | Üç evre modeli |
| SMT | Smart Money Technique (divergence) | İlişkili varlıklar arası uyumsuzluk |
| ERL / IRL | External / Internal Range Liquidity | Dış / iç aralık likiditesi |
| HTF / LTF | Higher / Lower Timeframe | Üst / alt zaman dilimi |
| R | Risk birimi | 1R = işlemde riske edilen tutar |
| PF | Profit Factor | Toplam kazanç / toplam kayıp |
