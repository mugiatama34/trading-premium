# PO3 Kural Seti v1 Backtesti: Özet ve Yorum

Tarih: 2026-10-03. Kurallar: [../../po3-kural-seti-v1.md](../../po3-kural-seti-v1.md). Ayrıntılı tablolar: [rapor.md](rapor.md). Tüm işlemler: `islemler.csv`.

## Kısa sonuç

**Kural seti v1, MSS ve FVG onaylarıyla da maliyet sonrası para kaybettiriyor.** Dört varyantın hiçbiri örneklem dışı testte beklenti, profit factor ve düşüş eşiklerini geçmedi. Onaylar ham süpürmeye göre bir miktar seçicilik kazandırıyor ama bu, maliyetleri karşılamaya yetmiyor.

## Örneklem dışı test (2024-06 → 2026-09), maliyetler dahil

| Varyant | İşlem | Net R | PF | Maks. düşüş (%1) | Rastgele kıyas (net R) | Rastgeleden iyi mi? |
|---|---|---|---|---|---|---|
| UTC, hedef Asya karşı tarafı | 367 | −0,099 | 0,89 | %55,7 | −0,183 | Hayır (p = 0,17) |
| UTC, hedef 2R | 323 | −0,060 | 0,92 | %36,6 | −0,175 | Sınırda (p = 0,049) |
| NY, hedef Asya karşı tarafı | 230 | −0,119 | 0,87 | %54,0 | −0,236 | Hayır (p = 0,13) |
| NY, hedef 2R | 211 | −0,176 | 0,78 | %40,0 | −0,170 | Hayır (p = 0,53) |
| **Eşik** | ≥ 100 | ≥ +0,15 | ≥ 1,3 | ≤ %20 | | p < 0,05 |

Tüm dönemde (2021-01 → 2026-09) tablo daha da kötü: net R −0,10 ile −0,22 arası, PF 0,75–0,87. 10.000 $ ile %1 riskte başlayan portföy, varyanta göre 1.400–4.900 $'a iniyor (yıllık −%12 ile −%29).

## Neden çalışmıyor?

1. **Kazanma oranı düşük:** Asya hedefinde işlemlerin yalnızca %21–25'i hedefe ulaşıyor. Ortalama kazanç +2,6–2,9R olsa da bu, %75'lik stop oranını karşılamıyor. 2R hedefinde kazanma oranı %33–35. Maliyetsiz başa baş için ~%33, maliyetlerle ~%38 gerekiyor.
2. **Stoplar dar, maliyet ağır:** Medyan stop mesafesi fiyatın %0,6–0,7'si. Bir giriş-çıkış (komisyon + kayma) işlem başına ortalama **0,13–0,17R** tutuyor. Brüt sonuç sıfıra yakın (−0,07R ile +0,03R arası); farkı maliyet belirliyor. Yol haritasındaki "çok dar stop" uyarısı veride aynen görüldü.
3. **Yön tahmini zayıf:** Aynı anda, aynı stop ve hedefle rastgele yönde açılan işlemler modelden çok geride değil. Model üç varyantta rastgele kıyastan ~0,1R iyi, NY-2R'de fark yok. Bu üstünlük yalnızca UTC-2R varyantında sınırda anlamlı (p = 0,049), diğerlerinde değil. Yani onaylar biraz bilgi taşıyor olabilir ama küçük ve kararsız.
4. **Yıllara göre tutarsız:** Tek tek yıllarda PF 0,5 ile 1,6 arasında dalgalanıyor. Hiçbir varyant iki yıl üst üste eşiği geçmiyor.
5. **Sağlamlık:** Parametreler tek tek değiştirildiğinde (Asya bitişi ±1 saat, N = 2/5, X = 6/24, tampon 0,3 ATR, pivot 3 mum, bias filtresi yok) net R −0,14 ile −0,28 arasında kalıyor. Sonucu pozitife çeviren tek bir ayar yok, yani sonuç tesadüfi bir parametre seçiminden kaynaklanmıyor.

Coin bazında birkaç coin (PENGU, SUI, MMT, bazı varyantlarda ETH) pozitif görünüyor. Ancak örneklemleri 5–50 işlem, güven aralıkları sıfırı içeriyor ve varyanttan varyanta işaret değiştiriyorlar. Geriye dönük seçilirlerse aşırı uyum (overfitting) olur.

## Kaldıraç ve risk yüzdesi

%1 riskte gereken kaldıraç medyan 1,4–1,7x, işlemlerin %90'ında 3,7x'in altında. İzole marjinde tasfiye mesafesi her durumda stopun 3 katından uzak kalıyor (ayrıntı kural seti belgesinde). Beklenti negatif olduğu için %2 risk getiriyi artırmıyor, düşüşü %70–98'e çıkarıyor. Bu model için önerilebilecek bir kaldıraç veya risk yüzdesi yok.

## Sınırlar

- 5 dakikalık veri kullanıldı (yol haritası 1 dakikalık öneriyordu). Mum içi belirsizlikler temkinli çözüldü: aynı mumda stop ve hedef varsa stop sayıldı. Bu, sonuçları biraz kötüleştirmiş olabilir. Ancak brüt sonucun zaten sıfır civarında olması, farkın bundan kaynaklanmadığını düşündürüyor.
- Komisyon oranları (maker %0,02, taker %0,05) doğrulanmadı. Daha düşük bir VIP seviyesi maliyeti azaltır ama brüt sıfıra yakın olduğundan sonucu pozitife çevirmesi beklenmez.
- Kural seti tek bir yorumdur. ICT'nin farklı eğitmenleri MSS, FVG ve giriş için farklı tanımlar kullanır. Bu yorum işe yaramadı; bu, her yorumun yaramayacağının kanıtı değildir.
- Haber günleri (CPI, FOMC) ayrıca ele alınmadı.

## Yol haritasına göre karar önerisi

Aşama 4'ün "bitti" ölçütü sağlandı: örneklem dışı testte net bir **"çalışmıyor"** sonucu var. Yol haritasının Aşama 6 seçeneklerine göre durum **"bırak"** ya da **"düzelt"**:

- **Bırak (önerim):** Hem ham varsayım (Aşama 3) hem onaylı kural seti (Aşama 4) maliyet sonrası negatif. Veri, backtest motoru ve maliyet modeli bir sonraki model için hazır.
- **Düzelt:** Tek umut verici işaret, UTC-2R varyantında rastgeleye karşı küçük bir üstünlük. Daha geniş stoplu (maliyetin R içindeki payını azaltan) bir v2 denenebilir. Ancak bu, sonuçlara bakarak kural uydurma riski taşır ve yeni bir örneklem dışı dönem gerektirir.

Karar kullanıcıya aittir.

## Güncelleme: v2 (geniş stop) denendi, o da geçmedi

Kullanıcının seçimiyle v2 denendi ([../../po3-kural-seti-v2.md](../../po3-kural-seti-v2.md), ayrıntı: [v2_rapor.md](v2_rapor.md)). Asgari stop mesafesi ve hedef seçeneklerinden oluşan 64 aday ayar örneklem içinde tarandı. En iyisi seçildi: NY açılışı, stop en az %1,5 (genişletilerek), hedef 2R.

- Örneklem içinde +0,060R (PF 1,11) olan bu ayar, örneklem dışında **−0,193R (PF 0,71)** verdi. Rastgele yönlü kıyas (−0,105R) bile modelden iyi çıktı.
- Geniş stop maliyeti amaçlandığı gibi düşürdü: işlem başına 0,06R. Ama maliyetsiz sonuç da negatife döndü (−0,14R). Yani sorun yalnızca maliyet değildi; yön tahmininde güvenilir bir avantaj yok.
- 64 adayın yalnızca 4'ü örneklem dışında pozitif. Eşikleri geçen tek aday 30 işlemlik (eşik 100) ve örneklem içinde negatif; tesadüf olarak değerlendirilmeli.
- Örneklem içinde en iyi görünen adaylar (az işlemli "filtre" ayarları) örneklem dışında en kötüler arasında. Bu, aşırı uyumun (overfitting) tipik işaretidir.

**Sonuç:** PO3/AMD bu üç farklı ölçümde (ham varsayım, v1, v2) maliyet sonrası avantaj göstermedi. Yol haritasındaki Aşama 6'ya göre önerim **bırakmak**. Veri, backtest motoru ve maliyet modeli bir sonraki model için hazır.

## Güncelleme: Devam (kırılım) modeli denendi, o da geçmedi

Aşama 3'teki küçük devam eğilimini işlemek için Asya aralığının Londra'da kırıldığı yönde işlem açan ayrı bir model denendi. Kurallar ve seçim yöntemi `devam.py` dosyasının başında; ayrıntılar [devam_rapor.md](devam_rapor.md) dosyasında. 48 aday (piyasa/limit giriş × stop × hedef × bias) yalnızca örneklem içinde tarandı.

- Seçilen aday: NY açılışı, kırılan seviyeye limit (maker) giriş, stop Asya'nın karşı tarafı, hedef yok (gün sonu çıkışı), bias filtreli. Örneklem içinde −0,029R, örneklem dışında **−0,019R, PF 0,96**.
- Devam eğilimi gerçek: model, aynı anda rastgele yönde açılan işlemleri anlamlı şekilde geçiyor (−0,068R'ye karşı −0,019R, p = 0,004). Ama bu üstünlük yalnızca işlem başına ~0,02–0,05R brüt. Limit girişle bile ~0,05R maliyet bunu siliyor.
- 48 adaydan yalnızca 1'i örneklem dışında pozitif (+0,000R), eşikleri geçen yok.
- Stoplar geniş (medyan %2,3–2,7), bu yüzden kaldıraç gerekmiyor. %3 toplam risk sınırı, 17 coinde aynı gün aynı yöne çok sayıda sinyal çıktığı için işlemlerin yaklaşık yarısını atlıyor; coinler birlikte hareket ediyor.

**Sonuç:** Asya aralığı etrafındaki fiyat davranışında ölçülebilir ama ticari olarak kullanılamayacak kadar küçük bir yön bilgisi var. Bu aile (PO3, v1, v2, devam) maliyet sonrası +0,15R eşiğinin çok uzağında kaldı.
