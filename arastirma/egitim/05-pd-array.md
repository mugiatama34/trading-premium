# Modül 5: Premium, Discount ve PD Array

> **PD Array** (Premium/Discount Array), ICT'de "fiyatın tepki vermesi beklenen bölgelerin" ortak adıdır. Bu modül önce premium/discount fikrini, sonra PD array türlerini ve hangi sırayla önemsendiklerini anlatır.

## 5.1 Premium, discount ve equilibrium

Bir fiyat aralığı seç (ör. dünün tepesi ile dibi, ya da son belirgin swing dip ile swing tepe):

```text
Aralık tepesi  ─────────────────  %100
                                          PREMIUM (pahalı bölge)
                                          → satış aranır
Equilibrium    ─ ─ ─ ─ ─ ─ ─ ─ ─  %50   (denge, "adil fiyat")
                                          DISCOUNT (ucuz bölge)
                                          → alış aranır
Aralık dibi    ─────────────────  %0
```

**Kural (iddia):** Yükseliş beklediğinde yalnızca discount'tan al; düşüş beklediğinde yalnızca premium'dan sat. "Ucuzdan al, pahalıdan sat" fikrinin yapılandırılmış hali.

**Hangi aralık?** Burası belirsizliğin kaynağıdır. Günlük aralık, haftalık aralık, son swing aralığı ya da IPDA 20/40/60 gün aralığı farklı sonuçlar verir. Bir aralık seç ve hep onu kullan.

## 5.2 Veride premium/discount

BTC, ETH, SOL 1 saatlik verisinde fiyatın **önceki günün aralığındaki konumu** ile sonraki 24 saatin getirisi ([`sonuclar/istatistik.md`](sonuclar/istatistik.md), maliyetsiz):

| Bölge | Ort. 24s getiri | Yükselme oranı |
|---|---|---|
| PDL altı | +%0,06 | %51,3 |
| Discount (%0–25) | +%0,21 | %54,6 |
| Discount (%25–50) | +%0,12 | %52,3 |
| Premium (%50–75) | +%0,16 | %51,1 |
| Premium (%75–100) | +%0,18 | %48,3 |
| PDH üstü | +%0,33 | %49,4 |

**Yorum:** Derin discount'ta (alt çeyrek) yükselme oranı en yüksek (%54,6), premium'un üst çeyreğinde en düşük (%48,3); yani bir parça "ortalamaya dönüş" izi var. Ama **ortalama getiri** en yüksek PDH'nin üstündeyken: fiyat dünün tepesinin üstündeyken zaman zaman güçlü devam ediyor (momentum). Kısacası premium/discount tek başına net bir avantaj vermiyor; iki zıt etki (ortalamaya dönüş ve momentum) birbirine karışıyor. Ayrıca bu dönemde kripto genel olarak yükseldiği için tüm bölgelerin ortalaması pozitif; bu yön etkisi, bölgeden bağımsız.

## 5.3 PD array türleri

PD array, fiyatın tepki verebileceği **her türlü** bölgeye verilen addır. En sık kullanılanlar:

| PD array | Tanım | Yön |
|---|---|---|
| **Old high / old low** | Eski tepe veya dip (likidite havuzu) | Hedef / dönüş yeri |
| **Rejection block** | Uzun fitillerin oluşturduğu bölge (fitil gövdeden fitil ucuna) | Ret bölgesi |
| **Order block (OB)** | Displacement öncesi son ters mum (Modül 3) | Destek/direnç |
| **Fair value gap (FVG)** | Üç mumlu boşluk (Modül 3) | Destek/direnç |
| **Liquidity void** | Tek yönlü, çok mumlu boşluk; büyük FVG dizisi | Doldurulma hedefi |
| **Breaker block** | Likidite süpürüp sonra kırılan OB; ters yönde çalışır | Destek/direnç |
| **Mitigation block** | Breaker gibi, ama öncesinde likidite süpürmesi yok (başarısız swing) | Destek/direnç |
| **Volume imbalance** | Ardışık iki mumun gövdeleri arasındaki boşluk (fitiller örtüşür) | Küçük dengesizlik |
| **Propulsion block** | OB'nin içine dokunup itme veren mum | Destek/direnç |

### Breaker block

```text
Bullish breaker
                         D
                        / \
           B           /   \
          /\          /     E  ← B'deki eski bearish OB'ye dönüş = bullish breaker girişi
         /  \        /
        /    \      /
   L1  /      \    /
    \ /        \  /
     \/         \/
                L2  ← L1'in altına inildi (SSL süpürmesi)
```

1. B tepesini yapan yükselişin son yükseliş mumu, düşüşten önceki **bearish OB**'dir.
2. Fiyat düşer ve L1 dibinin altına iner (L2): sellside likidite süpürüldü.
3. Güçlü bir yükselişle B'nin üstünde kapanış gelir (MSS), fiyat D'ye çıkar.
4. Fiyat B'deki eski OB bölgesine geri döner (E). Bu bölge artık **bullish breaker**'dır.

Mantık: Bearish OB'nin tutmaması, satıcıların "yenildiğini" gösterir; o bölgeye dönüş artık alım fırsatı sayılır.

## 5.4 PD array matrisi (sıralama)

ICT, PD array'lerin premium ve discount'ta belirli bir sırayla dizildiğini anlatır. Kaynaklarda sıralama küçük farklarla verilir; yaygın versiyon şöyledir (aralığın ucundan dengeye doğru):

```text
PREMIUM (satış için, tepeden aşağı)
  1. Old high (eski tepe, BSL)
  2. Rejection block
  3. Bearish order block
  4. Fair value gap
  5. Liquidity void
  6. Bearish breaker
  7. Mitigation block
─ ─ ─ ─ ─ ─ EQUILIBRIUM %50 ─ ─ ─ ─ ─ ─
  7. Mitigation block
  6. Bullish breaker
  5. Liquidity void
  4. Fair value gap
  3. Bullish order block
  2. Rejection block
  1. Old low (eski dip, SSL)
DISCOUNT (alış için, dipten yukarı)
```

**Nasıl kullanılır?**

1. Üst zaman diliminde aralığı belirle; fiyat premium'da mı discount'ta mı?
2. Discount'taysan ve yükseliş bekliyorsan, altındaki bullish PD array'leri (FVG, OB, breaker) işaretle.
3. Fiyat bu bölgelerden birine geldiğinde alt zaman diliminde onay ara (Modül 6).
4. Hedef: premium tarafındaki PD array'ler, özellikle old high (BSL).

**Not:** "Hangi PD array'in tutacağını" önceden bilemezsin; matris bir öncelik listesidir, kesinlik değildir.

## 5.5 Sık yapılan hatalar

1. **Aralığı işlemden sonra seçmek.** Aralık seçimi esnek bırakılınca her giriş "discount'ta" gösterilebilir.
2. **Premium'da almak, discount'ta satmak (bilmeden).** Özellikle FOMO ile kırılıma girerken olur. Kendini kontrol etmek için girişten önce aralıktaki yüzdeyi yaz.
3. **Grafiği PD array ile doldurmak.** Her zaman diliminde her türü çizince fiyat her yerde bir bölgeye "dokunur". En fazla 2–3 bölgeyle çalış.
4. **Discount = alım sinyali sanmak.** Düşen trendde discount daha da ucuzlayabilir. PD array'ler ancak yön (bias) belirlendikten sonra anlamlıdır.

## 5.6 Nasıl test ederiz?

- Premium/discount için ilk kaba kontrol yapıldı (yukarıdaki tablo). Sonraki adım: aralık tanımını değiştirerek (haftalık, 20 gün) aynı tabloyu çıkarmak ve sonucun tanıma duyarlı olup olmadığını görmek.
- PD array matrisi için test edilecek soru: "Discount'taki bullish FVG retest'i, premium'daki bullish FVG retest'inden daha mı iyi sonuç veriyor?" Bu, ICT'nin net ve test edilebilir bir iddiasıdır.
- Breaker için mekanik tanım: "Likidite süpürmesinden sonra MSS ile kırılan OB." Retest sonuçları rastgele geri çekilme girişleriyle kıyaslanır.

## 5.7 Kendini sına

1. Dünün tepesi 100.000, dibi 96.000. Fiyat 97.000'de. Premium mu discount mu, aralığın yüzde kaçında?
2. Breaker block ile mitigation block arasındaki fark nedir?
3. Yükseliş bekliyorsan hangi bölgedeki hangi PD array'lere bakarsın?
4. Verideki premium/discount tablosunda en yüksek ortalama getiri neden "PDH üstü" bölgesinde olabilir?
5. OTE (Modül 4) ile discount arasındaki ilişki nedir?

<details>
<summary>Cevaplar</summary>

1. (97.000 − 96.000) / (100.000 − 96.000) = %25: discount, alt çeyreğin sınırında.
2. Breaker'dan önce bir likidite süpürmesi vardır (yeni tepe/dip yapılıp geri dönülür); mitigation block'ta ise fiyat yeni tepe/dip yapamadan döner (başarısız swing).
3. Discount'taki bullish FVG, bullish OB, bullish breaker ve old low (SSL) bölgelerine.
4. Fiyat dünün tepesinin üstündeyken güçlü trend günleri (momentum) ortalamayı yukarı çeker; yükselme oranı düşük olsa bile kazanç günleri büyük olabilir.
5. OTE (%62–79 geri çekilme) aralığın discount yarısının içindeki daha dar bir bölgedir.

</details>
