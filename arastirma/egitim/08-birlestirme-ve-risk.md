# Modül 8: Hepsini Birleştirmek, Risk Yönetimi ve Test Planı

> Önceki modüllerdeki parçaları tek bir işlem planında birleştiriyoruz. Ardından projenin risk kurallarıyla (işlem başına %1–2 risk, 10.000 $ örnek sermaye) pozisyon büyüklüğü ve kaldıraç hesabını, son olarak da bu planın nasıl test edileceğini anlatıyoruz.

## 8.1 Örnek bir SMC/ICT işlem planı (yukarıdan aşağıya)

```text
┌──────────────────────────────────────────────────────────────┐
│ 1. YÖN (Günlük / 4H)                                          │
│    Yapı yükseliş mi düşüş mü? Fiyat hangi likiditeye gidiyor? │
├──────────────────────────────────────────────────────────────┤
│ 2. BÖLGE (4H / 1H)                                            │
│    Fiyat premium mu discount mu? Hangi PD array'e yakın?      │
├──────────────────────────────────────────────────────────────┤
│ 3. LİKİDİTE                                                   │
│    Bölgede veya yakınında SSL/BSL süpürüldü mü?               │
├──────────────────────────────────────────────────────────────┤
│ 4. ONAY (1H)  → saatlik bozulma                               │
│    Süpürme öncesi son swing seviyesinin ötesinde kapanış      │
├──────────────────────────────────────────────────────────────┤
│ 5. GİRİŞ (15m / 5m)                                           │
│    Bozulmanın FVG'sine / OB'sine limit emir                   │
│    (veya hemen ters giriş: Modül 7'deki uyarılarla)           │
├──────────────────────────────────────────────────────────────┤
│ 6. RİSK                                                       │
│    Stop: süpürmenin ucu. Hedef: karşı likidite.               │
│    Pozisyon: sermayenin %1'i risk. Maliyet ≥ 0,15R ise girme. │
└──────────────────────────────────────────────────────────────┘
```

**Örnek senaryo (long):**

1. Günlük grafikte BTC yükselen yapıda (HH/HL), son HL korunuyor.
2. Fiyat önceki günün aralığının alt çeyreğinde (discount), altında 4H bullish FVG var.
3. 1H mum PDL'yi fitille aşıp üstünde kapatıyor (SSL süpürmesi).
4. Dört saat sonra 1H mum, süpürmeden önceki son swing tepenin üstünde kapatıyor (saatlik bozulma), arkasında FVG kalıyor.
5. 15 dakikalıkta fiyat bu FVG'nin orta noktasına (CE) geri geliyor; limit alış.
6. Stop: süpürmenin dibinin biraz altı. Hedef: önceki günün tepesi (BSL).

## 8.2 Risk hesabı: pozisyon büyüklüğü

Formül:

```text
Risk ($)          = Sermaye × risk oranı
Stop mesafesi (%) = |Giriş − Stop| / Giriş
Pozisyon büyüklüğü ($) = Risk ($) / Stop mesafesi (%)
Kaldıraç          = Pozisyon büyüklüğü / Sermaye
```

**Örnek:** Sermaye 10.000 $, risk %1 → 100 $. Giriş 94.766, stop 93.661 (Modül 6, Örnek 4).

- Stop mesafesi = (94.766 − 93.661) / 94.766 = **%1,17**
- Pozisyon = 100 / 0,0117 ≈ **8.550 $** (≈ 0,090 BTC)
- Kaldıraç = 8.550 / 10.000 ≈ **0,86x**

Burada önemli nokta: **riski kaldıraç değil, stop mesafesi ve pozisyon büyüklüğü belirler.** Kaldıraç yalnızca bu pozisyonu açmak için ne kadar teminat ayıracağını belirler. Aynı 100 $ risk, %0,3'lük dar stopla 33.300 $ pozisyon ve 3,3x kaldıraç gerektirir.

## 8.3 Kaldıraç nasıl seçilir?

Proje kuralı: kaldıraç sabit değil, her model için risk oranına göre belirlenir. Pratikte:

1. **Gereken kaldıraç** = pozisyon / sermaye. Bunun altına inemezsin, yoksa planlanan pozisyon açılmaz.
2. **Likidasyon güvenliği:** İzole marjinde likidasyon fiyatı, stopun **çok** ötesinde olmalı. Kabaca likidasyon mesafesi ≈ 1 / kaldıraç (bakım marjı hariç). 10x kaldıraçta likidasyon ~%10 uzaktadır; stop %1 uzaktaysa güvenli. 50x'te ~%2 uzaktadır; ani bir fitil hem stopu hem likidasyonu geçebilir.
3. **Teminatı küçük tut, gerisini dışarıda bırak:** Gereken kaldıraçtan biraz yüksek bir kaldıraç seçip (ör. gereken 0,86x ise 3–5x) yalnızca o pozisyonun teminatını borsaya koymak, karşı taraf riskini azaltır. Risk değişmez çünkü stop aynı.
4. **Aynı yönde toplam açık risk en fazla %3** (proje kuralı). Üç ayrı coinde aynı anda long açıp her birinde %1 risk aldıysan dördüncüye giremezsin.

Projedeki devam modeli için hesaplanan gereken kaldıraç: %1 riskte medyan 0,4x, %90'lık dilimde 0,9x, en yüksek 4,6x (PR #3, `devam_rapor.md`). Yani makul stoplarla kripto vadelide **yüksek kaldıraca gerek yoktur**; yüksek kaldıraç genellikle çok dar stop demektir ve Modül 7'deki maliyet sorununu getirir.

## 8.4 Maliyetler: her işlemin görünmeyen rakibi

| Kalem | Tipik değer (Binance USDT-M) | Not |
|---|---|---|
| Taker komisyonu | %0,05 / taraf | Piyasa emri, stop |
| Maker komisyonu | %0,02 / taraf | Limit emir (dolarsa) |
| Kayma (slippage) | %0,01–0,05 / taraf | Küçük coinlerde daha yüksek |
| Fonlama | ±%0,01 / 8 saat (tipik) | Long'lar genelde öder; uzun tutunca birikir |

Kural: **Maliyet (R) = toplam maliyet (%) / stop mesafesi (%)**. Maliyet 0,15R'yi geçiyorsa (yani stop, maliyetin ~7 katından yakınsa) o işlemin pozitif beklentiye ulaşması zordur. Bu eğitimde kullanılan varsayım: gidiş-dönüş yaklaşık %0,155 (12 saat tutuşta).

## 8.5 İşlem günlüğü

Her işlem (kâğıt üzerinde bile) için kaydet:

| Alan | Örnek |
|---|---|
| Tarih/saat (UTC) | 2025-01-13 06:00 |
| Coin, yön | BTC, short |
| Üst zaman dilimi yönü | 4H düşüş |
| Bölge | Premium, PDH |
| Likidite | PDH süpürüldü (00:00) |
| Onay | 1H bozulma, FVG var |
| Giriş / stop / hedef | 93.604 / 95.934 / 88.943 |
| Stop mesafesi, maliyet (R) | %2,49, 0,06R |
| Sonuç (R, maliyet dahil) | +1,94R |
| Kurala uydum mu? | Evet |
| Not | Hedef aynı gün geldi |

"Kurala uydum mu?" sütunu en önemlisidir. Kurala uymayan işlemler sistemin değil, disiplinin sonucudur; ayrı değerlendirilir.

## 8.6 Öğrenme ve test yol haritası

**1. Kavramları göz alıştırmasıyla öğren (1–2 hafta)**
- Her gün BTC 1H grafiğinde: swing tepe/dipleri, PDH/PDL, eşit tepe/dipleri, FVG'leri işaretle.
- Sağ tarafı kapatıp mum mum ilerleyerek (TradingView "Bar Replay") saatlik bozulmayı canlıymış gibi bulmaya çalış.

**2. Kurallarını yazıya dök**
- Her kavram için tek, net bir tanım (bu eğitimdeki `kod/kavramlar.py` tanımları başlangıç olabilir).
- Giriş, stop, hedef, iptal koşulu, işlem saatleri, maksimum işlem sayısı.

**3. Backtest (kod ile)**
- Kurallar koda dökülür; komisyon, kayma, fonlama dahil.
- Parametre seçimi yalnızca örneklem içi dönemde, sonuç örneklem dışında.
- Rastgele yön/giriş kıyası.
- Geçme eşikleri (proje kararı): ≥100 işlem, net ≥ +0,15R/işlem, PF ≥ 1,3, maks. düşüş ≤ %20, rastgeleden iyi, parametre değişimine dayanıklı.

**4. Paper trading**
- Eşikleri geçen model, gerçek zamanlı ama gerçek parasız en az birkaç ay denenir. Backtest ile canlı sonuç arasındaki fark (kayma, kaçan işlemler, duygusal hatalar) burada görülür.

**5. Gerçek para**
- Yalnızca paper trading başarılıysa ve tamamen senin kararınla. Bu projede ajan gerçek emir vermez.

## 8.7 Bu eğitimden çıkan dürüst özet

| Kavram | Veride ne gördük? | Durum |
|---|---|---|
| Piyasa yapısı (HH/HL) | Tanım; test gerektirmez | Araç |
| Eşit tepe/dip likiditesi | Uzak seviyelerde biraz daha sık alınıyor | Kısmen destekleniyor |
| PDH/PDL süpürmesi = dönüş | Coinlere göre tutarsız; avantaj yok | Desteklenmiyor |
| Asya aralığı PO3 (proje testi) | 100+ aday, hiçbiri maliyet sonrası pozitif değil | Desteklenmiyor |
| FVG doldurulur | Evet ama rastgele seviye kadar; tepki ≈ yazı tura | Avantaj yok |
| Premium/discount | Hafif ortalamaya dönüş + momentum karışık | Belirsiz |
| Saatlik bozulma onayı | Onaysız girişten çok iyi, ama ≈ 0R | Geliştirilmeye değer |
| Hemen ters giriş | Dar stop yüzünden net −0,30R | Bu haliyle zararlı |

Bu tablo SMC/ICT'nin "işe yaramadığını" kanıtlamaz: yalnızca basit, tek tanımlı versiyonların kriptoda, maliyetler sonrası tek başına yetmediğini gösterir. Bu kavramlar en çok **dil** olarak işe yarar: grafiği tutarlı şekilde okumanı, stop ve hedefi mantıklı yerlere koymanı sağlar. Avantaj (edge) ise ancak kurallar netleştirilip test edildiğinde ortaya çıkar ya da çıkmaz.

## 8.8 Kendini sına

1. 10.000 $ sermaye, %1 risk, giriş 3.000, stop 2.940 (ETH long). Pozisyon büyüklüğü ve gereken kaldıraç nedir?
2. Aynı işlemde maliyet %0,155 ise kaç R'dir?
3. 25x kaldıraç kullanmak riski otomatik olarak artırır mı?
4. Aynı anda BTC, ETH, SOL'de %1 riskle long'dasın. AVAX'ta long sinyali geldi. Ne yaparsın?
5. Backtest'te parametreyi neden yalnızca örneklem içi dönemde seçeriz?

<details>
<summary>Cevaplar</summary>

1. Stop mesafesi 60 / 3.000 = %2. Pozisyon = 100 / 0,02 = 5.000 $ (≈1,67 ETH). Kaldıraç 0,5x.
2. 0,155 / 2 ≈ 0,08R.
3. Hayır. Risk, stop mesafesi ve pozisyon büyüklüğüyle belirlenir. Ama yüksek kaldıraç likidasyonu stopa yaklaştırır ve genellikle çok dar stoplarla birlikte kullanıldığı için dolaylı olarak riski artırır.
4. Girmezsin: aynı yönde toplam açık risk %3 sınırına ulaşıldı.
5. Tüm veride en iyi parametreyi seçmek, geçmişe aşırı uyum (overfitting) demektir; örneklem dışı sonuç, modelin hiç görmediği veride nasıl davrandığını gösterir. Projedeki v2 testi bunun örneğidir: örneklem içinde +0,06R, dışında −0,19R.

</details>
