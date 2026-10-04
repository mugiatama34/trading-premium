# Modül 4: ICT (Inner Circle Trader) Kavramları

> ICT, Michael J. Huddleston'un geliştirdiği ve büyük kısmı ücretsiz videolarla yayılan bir yöntem bütünüdür. SMC terimlerinin çoğu buradan gelir. ICT'nin SMC'den farkı **zaman** ve **algoritmik teslimat** vurgusudur: "fiyat belirli saatlerde, belirli seviyelere doğru gönderilir."

## 4.1 Temel varsayım: IPDA

ICT, fiyatın bir algoritma tarafından "teslim edildiğini" söyler: **IPDA (Interbank Price Delivery Algorithm)**. Bu algoritmanın iki işi olduğu iddia edilir:

1. Likiditeyi almak (BSL/SSL).
2. Dengesizlikleri (FVG) dengelemek.

ICT ayrıca geçmiş 20, 40 ve 60 işlem gününün tepe/diplerini (IPDA bakış aralıkları) hedef seviyeler olarak kullanır.

> **Dürüst not:** IPDA'nın varlığına dair bağımsız bir kanıt yoktur; bir modelleme metaforu olarak düşün. Bu eğitimde "algoritma şunu yapar" demek yerine "bu kural veride işe yarıyor mu?" diye soruyoruz.

## 4.2 Zaman: killzone'lar ve seanslar

ICT zamanları New York saatine göre verir (kış/yaz saati değişir; UTC'ye çevirirken dikkat).

| Seans / pencere | NY saati | UTC (yaz saati, EDT) | UTC (kış saati, EST) |
|---|---|---|---|
| Asya seansı | 20:00–00:00 | 00:00–04:00 | 01:00–05:00 |
| Londra killzone | 02:00–05:00 | 06:00–09:00 | 07:00–10:00 |
| New York AM killzone | 07:00–10:00 | 11:00–14:00 | 12:00–15:00 |
| Silver Bullet (NY) | 10:00–11:00 | 14:00–15:00 | 15:00–16:00 |
| Londra kapanışı | 10:00–12:00 | 14:00–16:00 | 15:00–17:00 |

- **Killzone:** Hacmin ve oynaklığın arttığı, ICT'ye göre günün yüksek/düşüğünün sık oluştuğu pencere.
- **Macro:** Saatin belli dakikalarındaki kısa pencereler (ör. 09:50–10:10 NY). ICT'ye göre algoritma bu aralıklarda likidite arar.
- **Kripto notu:** Bu saatler forex ve ABD vadeli piyasaları için tasarlandı. Kripto 7/24 işlem görür; yine de ABD ve Avrupa açılışlarında hacim artar, bu yüzden saatlerin etkisi test edilebilir ama varsayılmamalıdır.

## 4.3 Power of 3 (PO3) / AMD

Günlük (veya haftalık) mumun üç evrede oluştuğu iddiası:

1. **Accumulation (birikim):** Açılış etrafında dar aralık (çoğu zaman Asya seansı).
2. **Manipulation (manipülasyon):** Gerçek yönün tersine sahte hareket, **Judas swing**. Asya aralığının bir tarafı süpürülür.
3. **Distribution (dağıtım):** Günün gerçek hareketi.

```text
Yükseliş günü için PO3 (günlük mum)

          │  ← Distribution: günün asıl yükselişi, tepe
         ███
         ███
  açılış ███ ─ ─ ─
          │  ← Manipulation: açılışın altına sahte düşüş (Judas swing)
          │
```

**Bu projede test edildi.** PO3/AMD'nin Asya aralığına dayalı versiyonları (dönüş, MSS+FVG ile giriş, geniş stop, devam modeli; toplam 100'den fazla aday) örneklem dışında güvenilir bir avantaj vermedi. En iyi aday işlem başına −0,019R, PF 0,96 çıktı (PR #3, `arastirma/po3-backtest/sonuclar/devam_rapor.md`). Bu sonuç ICT'nin tamamını çürütmez ama ICT'nin en çok bilinen günlük modelinin kriptoda, kurala bağlandığında, maliyetler sonrası çalışmadığını gösterir.

## 4.4 OTE (Optimal Trade Entry)

Bir hareketin geri çekilmesinde girişin yapılacağı Fibonacci bölgesi: **%62–%79** (ICT özellikle %70,5'i vurgular). Yukarı hareketin dibinden tepesine Fibonacci çekilir, fiyatın %62–79 geri çekildiği bölge "optimal" giriş kabul edilir.

```text
Tepe   100 ───────────────  %0
              \
               \
                \ ─ ─ ─ ─   %50  (equilibrium)
                 \
  OTE bölgesi ── %62 ─ ─ ─
                  \  ← giriş
                ── %79 ─ ─ ─
                   \
Dip     0 ───────────────  %100 (stop bu dibin altında)
```

OTE aslında Modül 5'teki **discount** fikrinin daha dar bir versiyonudur.

## 4.5 SMT Divergence (akıllı para uyumsuzluğu)

Birbiriyle ilişkili iki varlıktan biri yeni tepe/dip yapar, diğeri yapmazsa buna SMT uyumsuzluğu denir. Kriptoda en doğal çift **BTC ve ETH**:

- BTC yeni dip yapar ama ETH önceki dibinin üstünde kalırsa: "satış tarafı zayıf, yükseliş dönüşü olabilir" (bullish SMT).

Kripto için ilginç bir aday, çünkü test edilmesi kolay ve PO3 çalışmasında denenmedi.

## 4.6 Diğer sık duyacağın ICT terimleri

| Terim | Kısaca |
|---|---|
| Displacement | Güçlü, gövdesi büyük, FVG bırakan hareket |
| MSS | Displacement ile gelen yapı kırılımı (SMC'deki CHoCH'un ICT'deki karşılığı) |
| Judas swing | Günün başındaki sahte yön (PO3'teki manipulation) |
| Breaker block | Likidite almış ve kırılmış OB; ters yönde destek/direnç olur (Modül 5) |
| Daily bias | Günün beklenen yönü; genelde üst zaman dilimi PD array'lerine göre |
| NWOG / NDOG | Yeni hafta / yeni gün açılış boşluğu (kripto 7/24 olduğu için boşluk nadiren oluşur) |
| Silver Bullet | Belirli bir saat penceresinde (ör. 10–11 NY) FVG girişi modeli |
| 2022 Mentorship modeli | Likidite süpürmesi → MSS → FVG girişi; bu projede v1 kural setinin temeli |

## 4.7 Sık yapılan hatalar

1. **Saat dilimini karıştırmak.** NY saatiyle verilen kuralı UTC'de uygularken yaz/kış saati farkını atlamak.
2. **Forex kuralını kriptoya aynen taşımak.** Seans yapısı farklıdır, haftasonu da işlem vardır.
3. **Her şeyi aynı anda kullanmak.** Killzone + PO3 + OTE + SMT + OB + FVG birlikte arandığında ya hiç işlem çıkmaz ya da geriye dönük her işlem "kural gereği" görünür.
4. **Öğretmenin canlı işlemlerine güvenmek.** Eğitim videolarında gösterilen işlemler seçilmiş örneklerdir. Önemli olan kuralın yüzlerce işlemdeki ortalamasıdır.

## 4.8 Nasıl test ederiz?

- **Killzone etkisi:** Günün tepe/dibinin saat dağılımını çıkar; killzone'larda rastgele bir dağılımdan anlamlı şekilde fazla mı oluşuyor?
- **SMT:** BTC/ETH 1 saatlik veride "biri yeni dip yaptı, diğeri yapmadı" olaylarını kodla, sonraki 12–24 saat getirisini rastgele olaylarla kıyasla.
- **OTE:** Yapı kırılımından sonra %62–79 geri çekilmede giriş, aynı stop/hedefle %38–50 geri çekilme girişine göre daha mı iyi?

Her testte maliyetler dahil, örneklem içi/dışı ayrımıyla ve parametre seçimini yalnızca örneklem içinde yaparak.

## 4.9 Kendini sına

1. PO3'te "M" hangi evredir ve Asya aralığıyla ilişkisi nedir?
2. OTE bölgesi hangi Fibonacci seviyeleri arasındadır?
3. BTC yeni tepe yaptı, ETH yapmadı. Bu hangi tür SMT'dir ve ne ima eder?
4. Londra killzone'u yaz saatinde UTC kaçtır?
5. Bu projede PO3 testlerinin ana sonucu neydi?

<details>
<summary>Cevaplar</summary>

1. Manipulation: gerçek yönün tersine sahte hareket. ICT'ye göre çoğu zaman Asya aralığının bir tarafı süpürülerek yapılır.
2. %62 ile %79 arası (en çok vurgulanan %70,5).
3. Bearish SMT: alış tarafı güçlü değil, düşüş dönüşü olabilir (test edilmesi gereken bir iddia).
4. 06:00–09:00 UTC.
5. Asya aralığı tabanlı PO3 modellerinin hiçbiri örneklem dışında maliyetler sonrası pozitif çıkmadı; devam eğilimi gerçek ama maliyetten küçük.

</details>
