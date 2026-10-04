# Modül 6: Saatlik Bozulma (1 Saatlik Yapı Kırılımı)

> "Saatlik bozulma", Türkçe SMC/ICT topluluğunda genellikle **1 saatlik grafikte piyasa yapısının kırılması** (1H MSS / CHoCH) için kullanılır: fiyat bir bölgeye veya likiditeye ulaştıktan sonra 1 saatlikte ters yönde yapı kırılımı gelmesi, işleme girmek için "onay" sayılır. Bu modül bu anlamı esas alır. Senin öğrendiğin kaynak terimi farklı kullanıyorsa (ör. saatin belirli dakikalarına bağlı "zaman bazlı" bozulma), modülü ona göre uyarlayabiliriz.

## 6.1 Neden 1 saatlik?

Çoklu zaman dilimi yaklaşımında (Modül 1.6) görev dağılımı şöyledir:

| Zaman dilimi | Görev | Örnek soru |
|---|---|---|
| Günlük / 4 saatlik | Yön (bias) ve PD array'ler | "Fiyat discount'ta mı, hangi FVG'ye geliyor?" |
| **1 saatlik** | **Onay: yön değişti mi?** | "Bölgeye geldi, 1H yapısı bozuldu mu?" |
| 15 / 5 dakikalık | Giriş zamanlaması | "Bozulmanın bıraktığı FVG'ye limit emir" |

1 saatlik, üst zaman diliminin "neden"i ile alt zaman diliminin "nasıl"ı arasında köprüdür. Saatlik bozulma olmadan girmek, düşen bıçağı tutmaya benzetilir; bozulmayı beklemek ise geç kalma maliyeti getirir (Modül 7).

## 6.2 Saatlik bozulmanın anatomisi

Örnek: fiyat yukarıda bir PD array'e (bearish FVG / BSL) ulaşıyor, short düşünüyorsun.

```text
1 saatlik grafik

          S  ← süpürme: PDH/BSL alındı (fitil üstte, kapanış altta)
         │
        ███▒▒▒
     ███    ▒▒▒
  ███  Y      ▒▒▒                ← Y: süpürmeden önceki son swing dip
 ─ ─ ─ ─ ─ ─ ─ ─▒▒▒ ─ ─ ─ ─ ─   ← yapı seviyesi
                 ▒▒▒  ← M: Y'nin ALTINDA KAPANIŞ = saatlik bozulma (MSS)
                 ▒▒▒     arkasında FVG bıraktıysa "displacement'lı" kabul edilir
```

Kontrol listesi:

1. **Bağlam:** Fiyat önemli bir seviyede mi? (HTF PD array, PDH/PDL, eşit tepe/dip)
2. **Süpürme (isteğe bağlı ama tercih edilir):** Seviyenin ötesine fitil atıp içeri kapanış.
3. **Kırılan seviye:** Süpürmeden **önce** kesinleşmiş son swing dip (short için) veya tepe (long için). Süpürmeden sonra oluşan küçük dalgalar değil.
4. **Kapanış:** 1 saatlik mum o seviyenin ötesinde **kapanmalı**; fitil yetmez.
5. **Kalite:** Kırılım güçlü gövdeli mumla ve FVG bırakarak geldiyse (displacement) daha güvenilir kabul edilir.
6. **Süre:** Bozulma süpürmeden sonra makul sürede gelmeli (bu eğitimin kodunda 6 mum). Çok geç gelen bozulma başka bir hikâyedir.
7. **İptal:** Bozulmadan önce fiyat süpürmenin ucunu geçerse kurulum bozulmuştur.

## 6.3 Gerçek veriden iki örnek

[`sonuclar/ornekler.md`](sonuclar/ornekler.md) içinde BTC 1 saatlik verisinden kural ile otomatik seçilmiş iki kurulum var:

- **Örnek 3 (işe yarayan):** 13 Ocak 2025 00:00 UTC mumu PDH'yi (95.444) fitille aştı, içeride kapattı. 06:00 mumu son swing dibin (93.661) altında kapattı: saatlik bozulma. 93.604'ten short, stop 95.934 (süpürme ucu), 2R hedef 88.943 aynı gün 14:00'te geldi.
- **Örnek 4 (stop olan):** 12 Ocak 2025 09:00 PDL süpürüldü, 14:00 mumu son swing tepenin üstünde kapattı: yukarı yönlü saatlik bozulma. 94.766'dan long, ertesi sabah 06:00'da stop oldu.

İki grafik de "kitaba uygun". Fark ancak sonradan bilinir. Aynı kuralla 2025'in ilk altı ayında BTC'de 11 kurulum çıktı: 1 hedef, 2 stop, 8'i 24 saat içinde ikisine de ulaşamadı.

## 6.4 Veride saatlik bozulma onayı

`kod/istatistik.py`, PDH/PDL süpürmesinden sonra 6 mum içinde saatlik bozulma gelirse o mumun kapanışında girer, stopu süpürme ucuna koyar, 12 saat sonra kapanışta çıkar (BTC/ETH/SOL, 2023-01 → 2026-08, maliyetler dahil):

| | İşlem | Net R/işlem | %95 güven aralığı | Medyan stop |
|---|---|---|---|---|
| Saatlik bozulma onaylı giriş | 172 | −0,035 | −0,138 … +0,067 | %2,66 |

**Yorum:** Onaylı giriş, onaysız girişten (Modül 7) çok daha iyi; ama ortalama hâlâ sıfırın biraz altında ve güven aralığı sıfırı içine alıyor: **avantaj kanıtlanmış değil**. Coin bazında da tutarsız (BTC −0,00, ETH −0,20, SOL +0,14 R). İşlem sayısı da az (3,5 yılda 3 coinde 172). Hedef kuralı, süre, giriş biçimi (FVG retest) ve üst zaman dilimi filtresi eklenerek test edilmeye değer, ama bu haliyle bir sistem değil.

## 6.5 "Zaman bazlı" yorum: saat başı ve killzone

Bazı ICT anlatımlarında "saatlik" vurgusu zamanla ilgilidir:

- **Saat başı açılışı:** Her 1 saatlik mumun kendisi küçük bir PO3 gibi okunur: açılış, sahte hareket, asıl hareket.
- **Macro pencereleri:** Saatin belirli dakikalarında (ör. xx:50 – xx:10) likidite arandığı iddiası.
- **Killzone içinde bozulma:** Bozulma yalnızca Londra veya NY killzone'unda gelirse geçerli sayılır.

Bunlar ayrı test edilebilir hipotezlerdir. Önerilen sıra: önce saatlik bozulmayı tek başına netleştir, sonra "killzone içinde mi?" filtresinin sonucu iyileştirip iyileştirmediğine bak.

## 6.6 Sık yapılan hatalar

1. **Yanlış seviyeyi kırılım saymak.** Süpürmeden sonra oluşan minik bir dibin kırılması bozulma değildir; süpürmeden önceki yapı seviyesi esas alınır.
2. **Fitille kırılım.** Kapanışı bekle.
3. **Mum kapanmadan girmek.** 1 saatlik mumun ortasında seviye kırılmış görünür, kapanışta geri alınır. Bu, Modül 7'deki "erken giriş" tuzağının ta kendisidir.
4. **Stopu bozulma mumunun üstüne koymak.** Dar stop R'yi büyütür ama maliyeti ve stop olma sıklığını da artırır. Fikrin yanlış olduğunu gösteren yer süpürmenin ucudur.
5. **Bağlamsız bozulma.** Ortada önemli bir seviye yokken her saatlik CHoCH işlem değildir; 1 saatlikte günde birkaç kez yapı kırılımı olur.

## 6.7 Nasıl test ederiz?

Bu eğitimdeki tanım (`kod/istatistik.py` içinde `supurme_testi`) bir başlangıç. Sonraki adımlar:

1. Giriş: bozulma kapanışı yerine bozulmanın bıraktığı FVG'ye limit emir (maker komisyonu, daha iyi fiyat, ama bazı işlemler kaçar).
2. Hedef: sabit 2R, karşı likidite (PDL/PDH) veya süre bazlı çıkış.
3. Filtreler: üst zaman dilimi yönü, premium/discount, killzone.
4. Parametreleri yalnızca örneklem içi dönemde seç, örneklem dışında bir kez test et; projede kabul edilen eşikler: ≥100 işlem, net ≥ +0,15R, PF ≥ 1,3, maks. düşüş ≤ %20 ve rastgele kıyastan iyi olmak.

## 6.8 Kendini sına

1. Saatlik bozulma için hangi swing seviyesi kullanılır: süpürmeden önceki mi, sonraki mi?
2. Bir 1H mumu seviyenin altına iniyor ama üstünde kapanıyor. Bozulma var mı?
3. Bozulma oluşmadan fiyat süpürmenin tepesini geçerse ne olur?
4. Verideki onaylı giriş sonucu neden "avantaj kanıtlandı" anlamına gelmiyor?
5. Saatlik bozulmayı 15 dakikalık grafikle nasıl birleştirirsin?

<details>
<summary>Cevaplar</summary>

1. Süpürmeden önce kesinleşmiş son swing dip/tepe.
2. Hayır; kapanış kuralı sağlanmadı.
3. Kurulum iptal olur; süpürme aslında kırılıma dönüşmüştür.
4. Ortalama −0,035R, güven aralığı sıfırı içeriyor, coinler arasında tutarsız ve işlem sayısı az.
5. 1H bozulma yönü ve bölgeyi verir; 15 dakikalıkta bozulmanın bıraktığı FVG'ye geri çekilmeyi bekleyip oradan girersin (daha dar ama hâlâ anlamlı bir stopla).

</details>
