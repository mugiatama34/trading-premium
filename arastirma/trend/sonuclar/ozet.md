# Trend Takibi Modeli: Özet ve Yorum

Tarih: 2026-10-05. Kod ve kurallar: [../trend.py](../trend.py). Ayrıntılı tablolar: [rapor.md](rapor.md). Tüm işlemler: `islemler.csv`.

## Kısa sonuç

**Projede ilk kez bir model, örneklem dışı testte tüm devam eşiklerini geçti.** Ancak sonuç sınırda olan noktalar içeriyor ve gerçek parayla kullanmadan önce proje kuralı gereği paper trading şart. Sıradaki adım: yol haritasının Aşama 5'i (paper trading).

## Seçilen model

Seçim yalnızca örneklem içi veriyle (2021-01 → 2024-06), 18 aday arasından yapıldı:

- **Giriş:** Günlük kapanış son 20 günün en yükseğinin üstündeyse ertesi gün açılışta uzun. Yalnızca uzun yön.
- **Stop:** Giriş − 3 × ATR(20). Her gün kapanış − 3 × ATR'ye doğru yukarı çekilen iz süren stop. Hedef yok.
- **Risk:** İşlem başına sermayenin %1'i. Aynı yönde toplam açık risk en fazla %3.

## Örneklem dışı test (2024-06 → 2026-09), maliyetler dahil

| Ölçüt | Eşik | Sonuç | Durum |
|---|---|---|---|
| İşlem sayısı | ≥ 100 | 202 | Geçti |
| Net beklenti (işlem başına) | ≥ +0,15R | +0,272R (temkinli: +0,184R) | Geçti |
| Profit factor | ≥ 1,3 | 1,63 (temkinli: 1,41) | Geçti |
| Maks. düşüş (%1 risk, portföy) | ≤ %20 | %10,3 | Geçti |
| Rastgele kıyastan iyi | p < 0,05 | p = 0,045 | Sınırda geçti |
| Parametre değişikliklerinde sağlam | | 18 adayın 18'i örneklem dışında pozitif | Geçti |

"Temkinli" değer: veri sonunda hâlâ açık olan 16 pozisyonun, son kapanış yerine iz süren stoplarından kapandığı varsayımı.

Karşılaştırma için aynı dönemde al-ve-tut: BTC +%24 (en büyük düşüş %53), ETH −%29, SOL −%29, DOGE −%41. Yani örneklem dışı dönem, altcoinlerin çoğu için kolay bir yükseliş dönemi değildi.

## Dikkat edilmesi gerekenler

1. **Açık pozisyonların payı büyük.** Örneklem dışındaki toplam kazancın yarıdan fazlası henüz kapanmamış 16 pozisyondan geliyor. Bu pozisyonlar stoplarından kapansa bile eşikler geçiliyor (+0,184R, PF 1,41), ama pay yine de yüksek.
2. **Rastgele kıyas sınırda.** Aynı gün, aynı stop kuralıyla rastgele yönde açılan işlemler de ortalama +0,084R kazanıyor. Kazancın bir kısmı yön tahmininden değil, iz süren stopun yapısından (kayıpları kesip kazançları koşturmak) geliyor. Modelin rastgeleden farkı anlamlı ama zayıf (p = 0,045).
3. **Ayı piyasası zayıf nokta.** Model yalnızca uzun pozisyon açıyor. 2022 ayı piyasasında −0,36R/işlem (PF 0,34) kaybetti. Uzun bir düşüş döneminde art arda küçük kayıplar beklenir.
4. **Getiri mutlak olarak küçük.** Stoplar geniş (medyan fiyatın %16'sı) olduğundan %1 risk, sermayenin yalnızca ~0,1 katı büyüklüğünde pozisyon demek. %3 toplam risk sınırı, aynı anda en fazla 3 pozisyona izin veriyor ve sinyallerin ~%73'ünü atlatıyor. Sonuç: örneklem dışında yıllık ~%6, en büyük düşüş ~%10.
5. **Coin seçimi.** Coin listesi bugünden bakılarak seçildi. Listede bugün hâlâ işlem gören coinler var; geçmişte çöken coinler yok. Bu, sonuçları bir miktar iyimser gösterebilir (hayatta kalma yanılgısı).
6. Örneklem içinde en iyi olan kırılım süresi (N = 20) örneklem dışında da iyi. Ama N = 50/100 ve iki yönlü varyantlar da pozitif, yani sonuç tek bir ayara bağlı değil.

## Kaldıraç ve risk yüzdesi

Pozisyon büyüklüğü %1 riskte sermayenin ~0,1 katı, %2 riskte ~0,2 katı (en yüksek 0,5x). **Kaldıraç gerekmiyor.** %2 risk bu modelde getiriyi artırmıyor. %3 toplam sınır nedeniyle aynı anda yalnızca 1 pozisyon açılabiliyor; örneklem dışında 20 işlem alınıyor ve yıllık getiri ~%8 oluyor. Bu nedenle mevcut kurallarla en iyi seçim **%1 risk**. Getiriyi büyütmenin asıl yolu %3 toplam risk sınırını gözden geçirmek. Bu bir proje kararı olduğu için kullanıcıya aittir ve burada değiştirilmedi.

## Sıradaki adım

Proje kuralı: bir yöntem gerçek parayla kullanılmadan önce paper trading ile denenmelidir. Yol haritasına göre en az 8–12 hafta ve en az 50 işlem önerilir. Bu model 17 coinde ayda ortalama ~7 sinyal üretiyor; ancak %3 sınırıyla ayda yalnızca ~2 işlem alınabiliyor. Bu yüzden paper trading'de tüm sinyaller (R cinsinden) izlenmeli; böylece 50 işleme ~7 ayda ulaşılır. Sınır dahil portföy ayrıca izlenir. Kurallar paper trading boyunca değiştirilmemelidir.
