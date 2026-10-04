# Modül 3: SMC (Smart Money Concepts)

> SMC, ICT'nin (Modül 4) öğretilerinden türeyip sosyal medyada sadeleşerek yayılmış bir terimler kümesidir. Bu modül SMC'nin "alet çantasını" anlatır: BOS/CHoCH, order block, FVG, inducement, mitigation.

## 3.1 SMC'nin temel hikâyesi

1. "Akıllı para" (büyük kurumlar) fiyatı likiditeye götürür (Modül 2).
2. Likiditeyi aldıktan sonra güçlü bir hareketle yön değiştirir (**displacement**).
3. Bu hareket arkasında **izler** bırakır: order block ve FVG.
4. Fiyat bu izlere geri döner (**mitigation / retest**); trader orada girer.

Bu hikâye sezgisel olarak çekicidir. Ancak her adımı ölçülebilir hale getirmeden "işe yarıyor" demek mümkün değil. Aşağıda her aracın tanımını ve bilinen zayıflığını birlikte veriyoruz.

## 3.2 BOS ve CHoCH

- **BOS (Break of Structure):** Trend yönünde yapı kırılımı. Yükselişte son HH'nin kapanışla aşılması.
- **CHoCH (Change of Character):** Ters yöndeki ilk kırılım. Yükselişte son HL'nin altında kapanış.
- ICT'deki karşılığı **MSS (Market Structure Shift)**; MSS'te kırılımın güçlü bir displacement ile, genelde FVG bırakarak olması beklenir.

```text
Yükselen trendde CHoCH

        HH
       /  \        
  HH  /    \       
 /  \/      \      
    HL ─ ─ ─ \─ ─ ─ ← son HL
              \
               ▼ kapanış HL'nin altında = CHoCH (yapı karakter değiştirdi)
```

**İç yapı / dış yapı:** SMC trader'ları büyük swing'leri (dış yapı) ve onların içindeki küçük dalgaları (iç yapı) ayırır. Hangi seviyenin "geçerli" olduğu konusunda topluluk içinde bile görüş ayrılığı vardır; bu da yöntemi öznel hale getiren başlıca noktalardan biridir.

## 3.3 Order Block (OB)

**Tanım:** Yapıyı kıran güçlü hareketten (displacement) **hemen önceki son ters renkli mum**.

- **Yükseliş OB'si (bullish OB):** Güçlü yükselişten önceki son düşüş mumu.
- **Düşüş OB'si (bearish OB):** Güçlü düşüşten önceki son yükseliş mumu.

```text
Bullish OB
                    ███
                ███ ███
            ███ ███        ← displacement: yapıyı yukarı kırar
    ▒▒▒ ███
    ▒▒▒      ← son düşüş mumu = Order Block
    ▒▒▒        (fiyat buraya dönerse alım bölgesi kabul edilir)
```

**İddia:** Kurumlar bu mumda emirlerinin bir kısmını doldurdu; fiyat geri dönünce kalan emirleri doldururlar ve fiyat tepki verir.

**Kullanım:** OB'nin gövdesi veya %50'si (ICT'de *mean threshold*) giriş bölgesi; OB'nin diğer ucu stop yeri.

**Zayıflık:** Hemen her hareketten önce bir "ters renkli mum" vardır. OB'yi geçerli kılan şartlar (likidite almış olmalı, FVG bırakmış olmalı, yapıyı kırmış olmalı vb.) eklendikçe tanım iyileşir ama sübjektiflik de artar.

## 3.4 Fair Value Gap (FVG) / Imbalance

**Tanım:** Üç mumlu bir dizide, 1. mumun fitili ile 3. mumun fitili arasında kalan, 2. mumun gövdesiyle "tek taraflı" geçilmiş boşluk.

```text
Bullish FVG
                 │
                ███   ← 3. mum: dibi = FVG üst sınırı
           ███  ███
           ███
           ███        ← 2. mum: büyük displacement mumu
    ███ ·········  ← FVG: 1. mumun tepesi ile 3. mumun dibi arası boşluk
    ███   │
           ← 1. mum: tepesi = FVG alt sınırı
```

- Kod tanımı (`kod/kavramlar.py`): yükseliş FVG'si için `3. mumun dibi > 1. mumun tepesi`.
- **Consequent Encroachment (CE):** FVG'nin orta noktası (%50). ICT'de hassas giriş yeri.
- **Inversion FVG (IFVG):** Kapanışla tamamen geçilen FVG artık ters yönde çalışır kabul edilir (bullish FVG kırılınca direnç olur).
- **BPR (Balanced Price Range):** Zıt yönlü iki FVG'nin üst üste bindiği bölge.

**İddia:** FVG, piyasanın "verimsiz" geçtiği yerdir; fiyat bu boşluğu doldurmak (rebalance) için geri gelir ve orada tepki verir.

## 3.5 Veride FVG

BTC, ETH, SOL 1 saatlik verisinde (2023-01 → 2026-08) fiyatın en az %0,1'i büyüklüğünde 11.820 FVG incelendi ([`sonuclar/istatistik.md`](sonuclar/istatistik.md)):

| Ölçüt | Sonuç |
|---|---|
| 24 saatte FVG orta noktasına dönüş | %77,6 |
| Aynı uzaklıktaki **ayna** seviyeye (diğer yönde) gidiş | %77,9 |
| Orta noktaya dokununca, eşit uzaklıktaki hedefin stoptan önce gelmesi | %50,5 (rastgele ≈ %50) |

**Yorum:** "FVG'ler çoğunlukla doldurulur" doğrudur, ama aynı uzaklıktaki rastgele bir seviyeye de aynı sıklıkla gidiliyor. Yani doldurulma FVG'ye özgü bir "mıknatıs" etkisi değil, fiyatın doğal salınımı. Dokunulduktan sonraki tepki de yazı tura düzeyinde. **FVG tek başına bir avantaj göstermiyor.** Bu, FVG'nin hiçbir bağlamda işe yaramadığını kanıtlamaz (ör. üst zaman dilimi yönüyle birlikte); ama "FVG'yi gör, gir" yaklaşımını açıkça zayıflatır.

## 3.6 Inducement ve mitigation

- **Inducement (tuzak/yem):** Asıl giriş bölgesinden (OB/FVG) hemen önce oluşan küçük bir tepe/dip. Erken giren trader'ların stopları oraya birikir; fiyat önce onları alır, sonra asıl bölgeye ulaşır. SMC anlatısında "inducement alınmadan girme" denir.
- **Mitigation (telafi):** Fiyatın OB'ye geri dönmesi. "OB mitigate edildi" = fiyat bölgeye dokundu, bölge kullanıldı. Bir kez dokunulan bölge çoğu SMC kuralında artık zayıf sayılır.

## 3.7 Tipik SMC işlem akışı

1. Üst zaman diliminde yön (ör. 4 saatlik yükselen yapı).
2. Fiyat discount bölgesine (Modül 5) geri çekilir ve bir SSL'yi süpürür.
3. Alt zaman diliminde CHoCH/MSS oluşur, arkasında FVG ve OB kalır.
4. Fiyat FVG/OB'ye döner, limit emirle giriş.
5. Stop: süpürmenin dibinin altı. Hedef: karşı taraftaki BSL.

Bu akış Modül 8'de risk yönetimiyle birlikte birleştiriliyor.

## 3.8 Sık yapılan hatalar

1. **Geriye bakarak OB seçmek.** Tepkinin geldiği mumu "OB buydu" diye işaretlemek kolaydır; önceden hangi mumun OB olacağını söylemek zordur. Grafik çalışırken sağ tarafı kapatıp adım adım ilerle.
2. **Her boşluğu FVG saymak.** Büyüklük eşiği koy (ör. fiyatın %0,1'i veya ATR'nin bir kesri).
3. **Çok dar stop.** OB/FVG girişleri dar stop sunar; bu R oranını güzel gösterir ama maliyetler R cinsinden büyür. Projedeki v1 backtest'te ~%0,65 medyan stop ile işlem başına maliyet 0,13–0,17R olmuştu (PR #3, `arastirma/po3-backtest/sonuclar/ozet.md`).
4. **Terim çorbası.** OB + FVG + breaker + inducement + CHoCH aynı anda aranınca her grafikte bir "kurulum" bulunur. Az sayıda, net tanımlı araçla çalış.

## 3.9 Nasıl test ederiz?

- FVG ve swing yapı tanımı kodda hazır (`kod/kavramlar.py`). OB için de mekanik tanım yazılabilir: "BOS yapan displacement'tan önceki son ters mum, displacement en az 1,5 ATR."
- Test edilecek soru: "Üst zaman dilimi yönündeki FVG/OB retest'leri, aynı yöndeki rastgele geri çekilme girişlerinden daha iyi mi?" Maliyetler, örneklem içi/dışı ayrımı ve rastgele kıyas dahil.

## 3.10 Kendini sına

1. CHoCH ile BOS arasındaki fark nedir?
2. Bullish OB hangi mumdur?
3. FVG'nin "CE" seviyesi nedir?
4. Verideki "FVG'lerin %78'i doldurulur" bilgisi neden tek başına avantaj göstermez?
5. Inducement'ın amacı (anlatıya göre) nedir?

<details>
<summary>Cevaplar</summary>

1. BOS trend yönünde kırılımdır (devam), CHoCH ters yöndeki ilk kırılımdır (olası dönüş).
2. Yukarı yönlü displacement'tan hemen önceki son düşüş mumu.
3. FVG'nin orta noktası (%50).
4. Aynı uzaklıktaki rastgele seviyeye de aynı oranda (%78) gidiliyor; doldurulma FVG'ye özgü değil. Dokunulduktan sonraki tepki de %50 civarında.
5. Erken giren trader'ların stoplarını asıl bölgeden önce bir yerde toplamak; fiyat önce bu stopları alıp sonra asıl bölgeye ulaşır.

</details>
