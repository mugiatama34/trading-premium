# Modül 2: Likidite, Buyside ve Sellside Likidite

> SMC ve ICT'nin merkezindeki fikir şudur: fiyat rastgele dolaşmaz, **emirlerin biriktiği yerlere** gider. Bu modül o emirlerin nerede biriktiğini ve bunun ne kadarının veride göründüğünü anlatır.

## 2.1 Likidite ne demek?

Genel finansta likidite, "bir varlığı fiyatı fazla oynatmadan alıp satabilme kolaylığı"dır. SMC/ICT'de ise anlam daralır: **likidite = belirli bir fiyat seviyesinde bekleyen emir yığını**, özellikle stop emirleri.

Neden önemli? Büyük bir oyuncu (fon, piyasa yapıcı) büyük miktarda alış yapmak istiyorsa karşısında aynı büyüklükte **satıcı** bulması gerekir. Satıcıların toplu olarak beklediği yer, alıcıların stop-loss emirlerinin durduğu yerdir (bir uzun pozisyonun stop'u bir satış emridir). Anlatı şöyle der: büyük oyuncular fiyatı bu stopların olduğu yere götürür, stopları tetikler ve oluşan satış akışına karşı kendi alımlarını yapar.

> **Dürüst not:** Bu "büyük oyuncunun niyeti" anlatısı doğrudan gözlenemez. Kimin neden aldığını grafikten bilemeyiz. Gözlenebilen tek şey fiyatın bazı seviyelere gidip gitmediği ve sonra ne yaptığıdır. Bu yüzden aşağıda iddiaları değil, ölçülebilir kısımlarını test ediyoruz.

## 2.2 Buyside likidite (BSL)

**Buyside liquidity (alış tarafı likidite)**, tepelerin **üstünde** bekleyen alış emirleridir:

- Açığa satış (short) yapanların stop-loss emirleri (short'u kapatmak = almak).
- "Tepe kırılırsa alırım" diyenlerin kırılım (buy stop) emirleri.

BSL'nin tipik yerleri: swing tepeler, **eşit tepeler** (iki-üç tepe aynı seviyede), önceki günün/haftanın tepesi (PDH/PWH), seans tepeleri (Asya tepesi gibi).

## 2.3 Sellside likidite (SSL)

**Sellside liquidity (satış tarafı likidite)**, diplerin **altında** bekleyen satış emirleridir:

- Long pozisyonların stop-loss emirleri.
- "Dip kırılırsa satarım" kırılım emirleri.

Tipik yerleri: swing dipler, **eşit dipler**, PDL/PWL, seans dipleri, yükselen trend çizgisinin altı.

```text
 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ← BSL: short stopları + kırılım alışları
     /\        /\              (eşit tepeler = "çift kat" likidite)
    /  \      /  \
   /    \    /    \
  /      \  /      \
          \/
 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   ← SSL: long stopları + kırılım satışları
```

## 2.4 Likidite süpürmesi (sweep / raid / stop hunt)

Fiyat bir likidite seviyesini **fitille** geçer, stopları tetikler, sonra seviyenin **içine geri** kapatır. Buna sweep, raid, stop hunt veya "likidite alındı" denir.

```text
Sellside süpürmesi (SSL sweep)

   │ ███   │
   │ ███ ▒▒▒  ███
 ─ ─ ─ ─ ─ ─ ─│─ ─ ─ ─   ← eşit dipler / SSL
              │           ← fitil aşağı: stoplar tetiklendi
              (kapanış seviyenin üstünde)
```

İki farklı sonuç ayırt edilmelidir:

| Durum | Ne oldu? | Anlatının yorumu |
|---|---|---|
| **Süpürme (sweep)** | Fitil dışarı, kapanış içeri | "Likidite alındı, dönüş gelebilir" |
| **Kırılım (breakout)** | Kapanış dışarıda | "Seviye gerçekten kırıldı, devam gelebilir" |

## 2.5 Dış ve iç likidite (ERL / IRL)

ICT fiyatın iki tür hedef arasında gidip geldiğini söyler:

- **Dış aralık likiditesi (External Range Liquidity, ERL):** Bir aralığın en uç tepesi ve dibi (BSL/SSL).
- **İç aralık likiditesi (Internal Range Liquidity, IRL):** Aralığın içindeki dengesizlikler, özellikle FVG'ler (Modül 3).

Anlatı: "Fiyat dış likiditeyi aldıktan sonra iç likiditeye (FVG) döner; FVG'yi doldurduktan sonra karşı taraftaki dış likiditeye gider." Bu, hedef seçmek için bir çerçevedir.

## 2.6 Gerçek veriden örnek

[`sonuclar/ornekler.md`](sonuclar/ornekler.md) içindeki **Örnek 2**: 21 Şubat 2025'te BTC 1 saatlikte 98.030 ve 98.058'de iki eşit dip yaptı. 15:00 mumu bu seviyenin altına fitil attı ve üstünde kapattı; ders kitabı bir SSL süpürmesi. Ama sonrasında fiyat dönmedi; 12 saat sonra %1,8 daha aşağıdaydı. Bu örnek bilerek seçilmedi (kod ilk uygun örneği aldı) ve önemli bir dersi gösteriyor: **süpürme bir dönüş garantisi değildir.**

## 2.7 Veride ne görüyoruz?

`kod/istatistik.py` ile BTC, ETH ve SOL 1 saatlik verisinde (2023-01 → 2026-08) iki iddiaya bakıldı. Tam tablo: [`sonuclar/istatistik.md`](sonuclar/istatistik.md).

**İddia 1: "Eşit tepe/dipler likidite mıknatısıdır."**
Eşit seviyeler, aynı uzaklıktaki tek swing tepe/diplere göre 48 saat içinde biraz daha sık aşılıyor:

| Uzaklık (ATR cinsinden) | Eşit seviye aşılma oranı | Tek seviye aşılma oranı |
|---|---|---|
| 0–1 ATR | %87,8 | %87,2 |
| 1–2 ATR | %77,9 | %73,0 |
| 2–4 ATR | %62,7 | %53,7 |

Yorum: Uzak seviyelerde fark belirgin; yakın seviyelerde yok. Bu, iddianın **bir kısmını destekliyor**. Ama dikkat: eşit tepe/dipler daha çok yatay, sıkışan piyasalarda oluşur ve sıkışma sonrası genişleme zaten olağandır; yani fark "stop avından" değil piyasa koşulundan da gelebilir. Ayrıca "seviye alınacak" bilgisi tek başına işlem değildir: seviyeye kadar olan yolu yakalamak için girişi, stopu ve maliyeti de hesaba katmak gerekir.

**İddia 2: "Önceki gün tepesi/dibi süpürülünce fiyat döner."**
PDH/PDL süpürmesinden sonra 12 saatlik dönüş yönü oranı BTC'de %56,6, ETH'de %57,5, SOL'da %49,8. Ortalama getiriler ise tutarsız (BTC +%0,07, ETH −%0,03, SOL −%0,09). Yani **tutarlı bir dönüş avantajı görünmüyor**. Bu, projede daha önce Asya aralığı süpürmeleri için bulunan sonuçla aynı yönde: Londra'da Asya aralığı süpürüldüğünde dönüş oranı %47–49'du (PR #3, `arastirma/po3-istatistik/sonuclar/ozet.md`).

## 2.8 Sık yapılan hatalar

1. **Her tepeyi likidite saymak.** Her tepe bir gün aşılır; "likidite alındı" demek için hangi tepelerin önemli olduğunu önceden tanımla (PDH, eşit tepeler, seans tepeleri gibi).
2. **Süpürmeyi dönüş sinyali sanmak.** Veri bunu desteklemiyor; süpürme tek başına giriş değil, en fazla bir "bağlam"dır.
3. **Süpürmeyi geriye dönük tanımlamak.** Fitil atıp kapanan mum, ancak kapandığında süpürmedir. Mum açıkken seviye kırılım da olabilir.
4. **Stopunu herkesin koyduğu yere koymak.** Anlatı doğruysa en bariz yerdeki stop en kolay avlanan stoptur. Stopu, "fikrimin yanlış çıktığı yer"e koy, rastgele bariz bir seviyeye değil.

## 2.9 Nasıl test ederiz?

1. Likidite seviyelerini mekanik tanımla: PDH/PDL, eşit tepe/dip (%0,1 tolerans), seans tepe/dipleri.
2. Her seviye için "aşıldı mı, nasıl aşıldı (fitil/kapanış), sonra X saatte ne oldu?" tablosunu çıkar.
3. Rastgele seçilmiş seviyelerle kıyasla (ayna seviye, aynı uzaklık).
4. İşlem kuralına dönüştürdüğünde komisyon, kayma ve fonlamayı ekle; projede kabul edilen eşik net +0,15R/işlem ve PF ≥ 1,3'tür.

## 2.10 Kendini sına

1. Short pozisyonların stop emirleri hangi tarafın likiditesidir?
2. Bir mum PDH'yi aşıp üstünde kapattı. Süpürme mi, kırılım mı?
3. Eşit dipler neden "çift likidite" olarak görülür?
4. Veriye göre "PDH süpürüldü, şimdi short açarım" kuralı tek başına neden yetmez?
5. ERL ve IRL arasındaki fark nedir?

<details>
<summary>Cevaplar</summary>

1. Buyside likidite (BSL): short'un stopu bir alış emridir ve tepelerin üstünde durur.
2. Kırılım; kapanış seviyenin dışında.
3. İki dibi gören iki grup trader da stopunu aynı yerin hemen altına koyar; emir yığını kalınlaşır. Ayrıca "çift dip kırılırsa satarım" emirleri de oradadır.
4. Süpürme sonrası dönüş oranı coinler arasında %50–58 arasında değişiyor ve ortalama getiri tutarsız; maliyetler eklenince avantaj kalmıyor. Tek başına bağlamdır, sinyal değil.
5. ERL aralığın uç tepe/dipleridir (stop havuzları); IRL aralığın içindeki dengesizlik bölgeleridir (FVG gibi).

</details>
