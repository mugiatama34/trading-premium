# Modül 1: Price Action ve Piyasa Yapısı

> Bu modül sonraki bütün modüllerin temelidir. SMC ve ICT'deki her kavram "yapı", "tepe", "dip" ve "kırılım" kelimelerini kullanır; bunlar netleşmeden diğerleri ezber olur.

## 1.1 Price action nedir?

**Price action (fiyat hareketi)**, göstergeler (RSI, MACD vb.) yerine doğrudan fiyatın kendisine, yani mumlara, tepe ve diplere, seviyelere bakarak karar verme yaklaşımıdır. SMC ve ICT, price action'ın kendi terimlerini geliştirmiş iki "okuludur".

Bir makine mühendisi gözüyle: göstergeler fiyat sinyalinin filtrelenmiş türevleridir; price action ise ham sinyale bakmaktır. Ham sinyal daha az gecikmeli ama daha gürültülüdür.

## 1.2 Mum okuma

Her mum dört sayıdan oluşur: açılış (O), en yüksek (H), en düşük (L), kapanış (C).

```text
      │   ← üst fitil: fiyat buraya kadar çıktı ama tutunamadı
     ███  ← gövde: açılış ile kapanış arası (yeşil/█ = kapanış > açılış)
     ███
      │   ← alt fitil: fiyat buraya kadar indi ama geri alındı
```

- **Uzun gövde**, kısa fitil: bir taraf baskın, hareket "kararlı". ICT bunu *displacement* (güçlü yer değiştirme) diye adlandırır.
- **Uzun fitil**: bir seviye denenmiş ve reddedilmiş. SMC'de "likidite alındı" yorumunun ham hali budur.
- **Kapanış fitilden önemlidir.** Bir seviyenin "kırılıp kırılmadığına" karar verirken çoğu kural kapanışa bakar; fitil yalnızca "denendi" demektir.

## 1.3 Swing tepe ve swing dip

**Swing tepe**, solundaki ve sağındaki birkaç mumdan daha yüksek tepesi olan mumdur. **Swing dip** bunun tersidir. Bu eğitimin kodunda "3 mum solda, 3 mum sağda" kuralı kullanıldı (`kod/kavramlar.py`).

```text
            T            ← swing tepe: iki yanındaki mumlardan yüksek
          │ │ │
        │       │
      │           │   │
    │               │     ← D: swing dip
                    D
```

**Önemli tuzak:** Bir swing tepe, sağındaki mumlar kapanmadan *kesinleşmez*. Grafiğe geriye dönük bakınca tepeler apaçık görünür; canlı piyasada ise ancak birkaç mum sonra "evet, o bir tepeymiş" denebilir. Backtest yaparken bu gecikmeyi hesaba katmamak en yaygın hatadır (geleceği görme hatası, *look-ahead bias*).

## 1.4 Piyasa yapısı: HH, HL, LH, LL

Ardışık tepeleri ve dipleri birbiriyle kıyaslarız:

| Kısaltma | Açılım | Anlamı |
|---|---|---|
| HH | Higher High | Önceki tepeden yüksek tepe |
| HL | Higher Low | Önceki dipten yüksek dip |
| LH | Lower High | Önceki tepeden alçak tepe |
| LL | Lower Low | Önceki dipten alçak dip |

- **Yükselen trend:** HH + HL dizisi.
- **Düşen trend:** LH + LL dizisi.
- **Yatay (range):** Tepeler ve dipler kabaca aynı yerde.

```text
Yükselen yapı                      Düşen yapı
                 HH                 LH
          HH    /                  /  \     LH
         /  \  /                  /    \   /  \
   HH   /    HL                         \ /    \
  /  \ /                                 LL     \
     HL                                          LL
```

Gerçek BTC verisiyle etiketlenmiş bir örnek: [`sonuclar/ornekler.md`](sonuclar/ornekler.md) içindeki Örnek 1. O örnekte 11 Şubat 2025'te üst üste HH'ler geldikten sonra fiyatın 94.814'e inerek bir LL yapması, yükselen yapının bozulduğunu gösterir.

## 1.5 Kırılımlar: BOS ve CHoCH (ön bilgi)

- **BOS (Break of Structure, yapı kırılımı):** Trend yönünde son tepenin (yükselişte) veya son dibin (düşüşte) kapanışla aşılması. Trendin devamı demektir.
- **CHoCH (Change of Character, karakter değişimi):** Trendin tersine ilk kırılım. Örneğin yükselen trendde son HL'nin altında kapanış. "Trend dönüyor olabilir" uyarısıdır.

Bunlar Modül 3 ve Modül 6'da ayrıntılı işlenecek.

## 1.6 Zaman dilimleri (timeframe)

Aynı fiyat hareketi farklı zaman dilimlerinde farklı görünür. 1 saatlik grafikteki bir "trend dönüşü", günlük grafikte sıradan bir geri çekilme olabilir. Yaygın yaklaşım:

- **Üst zaman dilimi (HTF: günlük, 4 saatlik):** Yön (bias) ve önemli seviyeler.
- **Orta zaman dilimi (1 saatlik):** Kurulumun oluştuğu yer.
- **Alt zaman dilimi (LTF: 15, 5 dakikalık):** Giriş zamanlaması.

## 1.7 Sık yapılan hatalar

1. **Her küçük çıkıntıyı tepe saymak.** Tanımı sabitle (örneğin 3+3 mum) ve hep aynısını kullan.
2. **Geriye bakıp "ne kadar net" demek.** Kesinleşme gecikmesini unutma; canlıda o netlik yoktur.
3. **Fitili kırılım saymak.** Kapanış kuralını baştan belirle.
4. **Zaman dilimlerini karıştırmak.** "Trend yukarı" derken hangi zaman diliminde olduğunu söyle.

## 1.8 Ne test edildi, ne iddia?

- **Gözlem (tanım gereği doğru):** HH/HL ve LH/LL dizileri trendin tanımıdır; ayrıca test gerektirmez.
- **Topluluk iddiası:** "Yapı kırılımı sonrası fiyat yeni yönde devam eder." Bu bir öngörü iddiasıdır ve test gerektirir. Bu projede yakın bir iddia test edildi: Asya aralığının kırılım yönünde küçük bir devam eğilimi gerçekten var (rastgele yönden iyi, p = 0,004) ama işlem başına ~0,02–0,05R gibi, ~0,05R'lik maliyetin altında kalıyor (PR #3, `arastirma/po3-backtest/sonuclar/devam_rapor.md`).

## 1.9 Nasıl test ederiz?

Swing tepe/dip ve HH/HL tanımı `kod/kavramlar.py` içinde mekanik hale getirildi. Sonraki adım: "1 saatlik grafikte BOS sonrası 12 saatlik getiri, rastgele bir saatteki 12 saatlik getiriden farklı mı?" sorusunu maliyetler dahil ölçmek. Bunu yaparken swing noktasını yalnızca kesinleştiği mumdan itibaren kullanmak şarttır.

## 1.10 Kendini sına

1. Bir swing tepenin "kesinleşmesi" neden gecikmelidir ve bu backtest'i nasıl etkiler?
2. Yükselen trendde ilk LL oluştuğunda bu BOS mu, CHoCH mu?
3. Bir mum önceki tepeyi fitille aşıp altında kapattı. Bu bir kırılım mıdır?
4. 1 saatlik grafikte düşen trend, günlük grafikte yükselen trend varsa hangisi "doğru"dur?

<details>
<summary>Cevaplar</summary>

1. Tepe olduğunu anlamak için sağındaki mumların daha alçak kapanmasını beklemek gerekir. Backtest'te tepeyi oluştuğu mumda kullanmak geleceği görmek demektir ve sonuçları gerçekte olmayacak kadar iyi gösterir.
2. CHoCH (karakter değişimi): trendin tersine ilk kırılım.
3. Kapanış kuralı kullanıyorsan hayır; bu bir "deneme" veya likidite süpürmesidir (Modül 2).
4. İkisi de; farklı ölçeklerde farklı şeyler söylerler. Genelde üst zaman dilimi yönü belirler, 1 saatlik düşüş günlük yükselişin içindeki bir geri çekilme olabilir.

</details>
