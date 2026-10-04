# Modül 7: Immediate Reverse Execution (Hemen Ters Giriş)

> Bu terimin tek bir resmî ICT tanımı bulunmuyor; farklı eğitmenler farklı şekilde kullanıyor. Bu modülde en yaygın anlamı esas alınıyor: **fiyat bir likidite seviyesini süpürüp ters döndüğü anda, onay (saatlik bozulma) beklemeden ters yönde işleme girmek.** İlgili iki ICT terimi (Immediate Rebalance ve Inversion FVG) de aşağıda anlatılıyor. Senin kaynağın başka bir şeyi kastediyorsa söyle, modülü uyarlayalım.

## 7.1 Üç giriş biçimi

Aynı senaryo: fiyat PDH'yi (önceki gün tepesi) süpürüyor, short düşünüyorsun.

| Giriş biçimi | Ne zaman girilir? | Stop | Artısı | Eksisi |
|---|---|---|---|---|
| **Hemen ters giriş** (immediate reverse) | Süpürme mumu içeride kapanınca (veya daha agresifi: seviyeye limit emirle) | Süpürme fitilinin ucu | En iyi fiyat, dar stop, büyük R | Yanlış sinyal çok; dar stop maliyeti büyütür |
| **Onaylı giriş** (saatlik bozulma) | 1H yapı kırılımının kapanışında (Modül 6) | Süpürmenin ucu | Daha az yanlış sinyal | Daha kötü fiyat, daha geniş stop |
| **Retest girişi** | Bozulmadan sonra FVG/OB'ye geri çekilmede limit emir | Süpürmenin ucu veya OB'nin ötesi | Onay + iyi fiyat | Bazı işlemler geri çekilme olmadan kaçar |

```text
Hemen ters giriş, short

        │  ← fitil PDH'nin üstünde: stoplar alındı
 ─ ─ ─ ─│─ ─ ─ ─ ─ PDH
       ▒▒▒  ← mum PDH'nin altında kapandı → BURADA SHORT (hemen)
       ▒▒▒     stop: fitilin ucu (çok yakın)
```

## 7.2 Neden cazip?

- **R oranı büyük görünür.** Stop fitil ucunda, birkaç on dolar ötede; hedef karşı likidite. 1:5, 1:10 gibi oranlar kâğıt üzerinde mümkün.
- **Dönüşün en başını yakalar.** Bu yüzden eğitim videolarında en etkileyici işlemler genellikle bu tiptir.

## 7.3 Veride ne çıktı?

Aynı süpürme olaylarında (BTC, ETH, SOL 1 saatlik, 2023-01 → 2026-08) iki giriş biçimi kıyaslandı; çıkış 12 saat sonra veya stop, **maliyetler dahil** ([`sonuclar/istatistik.md`](sonuclar/istatistik.md)):

| Giriş biçimi | İşlem | Brüt R (maliyetsiz, coin bazında) | Net R/işlem | %95 güven aralığı | Medyan stop |
|---|---|---|---|---|---|
| Hemen ters giriş | 1.886 | −0,01 … +0,09 | **−0,302** | −0,416 … −0,187 | %0,68 |
| Saatlik bozulma onaylı | 172 | −0,13 … +0,18 | −0,035 | −0,138 … +0,067 | %2,66 |

**Ders 1: Dar stop maliyeti büyütür.** Gidiş-dönüş maliyeti (komisyon + kayma + fonlama) fiyatın yaklaşık %0,155'i. Stop %0,68 uzaktaysa bu tek başına ~0,23R eder; stop daha da yakınsa maliyet 0,5R'yi geçer. Hemen ters giriş brüt olarak sıfır civarında iken net olarak her işlemde ~0,3R kaybettiriyor. Projedeki PO3 v1 testinde de aynı şey görülmüştü: dar stoplarla maliyet işlem başına 0,13–0,17R (PR #3).

**Ders 2: Onay, yanlış sinyalleri azaltıyor ama avantaj yaratmıyor.** Onaylı giriş, hemen ters girişten belirgin şekilde daha iyi; ama tek başına sıfırın üstüne çıkmıyor.

**Ders 3: Büyük R oranı ≠ kârlılık.** Önemli olan **beklenti**dir: (kazanma oranı × ortalama kazanç) − (kaybetme oranı × ortalama kayıp) − maliyet. 1:5 R oranlı bir yöntem %15 kazanma oranıyla kaybettirir.

## 7.4 İlgili ICT terimleri

### Immediate Rebalance

ICT'de, fiyatın bir FVG bırakmadan hemen dengelenerek devam ettiği durum: ardışık mumların fitilleri tam üst üste biner, boşluk kalmaz. ICT'ye göre bu durumda fiyatın geri dönüp boşluk doldurmasını beklemek gerekmez; hareket "hemen dengelendiği" için doğrudan devam edebilir. Pratik anlamı: "FVG retest'i bekliyorum ama gelmeyebilir" uyarısı.

### Inversion FVG (IFVG)

Bir FVG'nin kapanışla **tamamen geçilmesi** durumunda, bölge ters rol üstlenir. Örneğin bullish FVG'nin altında kapanış gelirse o bölge artık direnç kabul edilir. Bazı trader'lar "ters dönüş girişini" IFVG retest'i olarak yapar: süpürme → bullish FVG'nin aşağı kırılması → kırılan FVG'ye geri dönüşte short.

```text
Inversion FVG, short

   ███ ·····  ← bullish FVG (destek olması beklenirdi)
          ▒▒▒  ← FVG'nin altında kapanış: FVG "ters döndü"
          ▒▒▒
      ·····│  ← fiyat aynı bölgeye geri döner → artık direnç → short
            ▒▒▒
```

## 7.5 Hemen ters girişi kullanmak istersen

Veri, bu haliyle hemen ters girişi desteklemiyor. Yine de üzerinde çalışmak istersen (kâğıt üzerinde):

1. **Stopu maliyete göre ayarla.** Stop mesafesi en az maliyetin 8–10 katı olmalı (ör. %0,155 maliyetle en az %1,2–1,5). Bu R oranını küçültür ama gerçekçi hale getirir.
2. **Yalnızca güçlü bağlamda kullan.** Üst zaman dilimi PD array'i + premium/discount + killzone aynı yönü gösteriyorsa.
3. **Limit emir kullan.** Seviyeye önceden konan limit emir maker komisyonu öder (taker'ın yaklaşık yarısı) ve kayma olmaz; ama "bıçağı tutma" riski en yüksektir.
4. **Kısmi giriş.** Pozisyonun yarısıyla hemen, yarısıyla saatlik bozulmada girmek; iki yaklaşımın ortalamasını alır.

Her biri test edilmeden gerçek parayla kullanılmamalı (proje kuralı: önce backtest, sonra paper trading).

## 7.6 Sık yapılan hatalar

1. **Mum kapanmadan girmek.** Süpürme, mum içeride kapanana kadar süpürme değildir; kırılım olabilir.
2. **R oranına aşık olmak.** Kazanma oranı ve maliyeti hesaba katmadan "1:8 aldım" demek.
3. **Kaybettikten sonra hemen tekrar girmek.** Süpürme kırılıma dönerse ikinci kez ters girmek, kayıpları büyütür.
4. **Kaldıraçla dar stopu birleştirmek.** Dar stop yüksek kaldıraç ister; likidasyon fiyatı stopa yaklaşır, kayma ve fonlama etkisi büyür.

## 7.7 Nasıl test ederiz?

- Kod hazır: `kod/istatistik.py` içindeki `supurme_testi` iki giriş biçimini aynı olaylar üzerinde kıyaslıyor.
- Eklenecekler: (a) retest girişi (bozulmanın FVG'sine limit emir), (b) minimum stop mesafesi filtresi, (c) limit emirle maker komisyonu, (d) IFVG girişi.
- Kıyas her zaman aynı olay kümesinde yapılmalı; aksi halde fark giriş biçiminden değil farklı olaylardan gelebilir.

## 7.8 Kendini sına

1. Hemen ters girişin en büyük avantajı ve en büyük dezavantajı nedir?
2. Gidiş-dönüş maliyeti %0,155, stop %0,5 uzakta. Maliyet kaç R?
3. 1:5 R oranlı bir yöntemin başa baş kazanma oranı (maliyetsiz) nedir?
4. Inversion FVG nedir?
5. Veride hemen ters giriş neden brüt sıfıra yakınken net olarak çok negatif?

<details>
<summary>Cevaplar</summary>

1. Avantaj: en iyi fiyat ve büyük R. Dezavantaj: çok sayıda yanlış sinyal ve dar stop yüzünden maliyetin R cinsinden büyümesi.
2. 0,155 / 0,5 = 0,31R. Her işlem kazanmadan önce 0,31R geride başlar.
3. 1 / (1 + 5) ≈ %16,7.
4. Kapanışla tamamen geçilen FVG'nin ters yönde destek/direnç olarak kullanılması.
5. Medyan stop %0,68; birçok işlemde stop çok daha yakın. Maliyet stop mesafesine bölününce R cinsinden büyüyor ve ortalama brüt sonucu yiyor.

</details>
