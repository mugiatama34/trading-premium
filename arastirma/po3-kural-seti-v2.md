# PO3 Kural Seti v2 (geniş stop)

Tarih: 2026-10-03. Durum: backtest edildi, devam eşiklerini geçmedi. Sonuçlar: [po3-backtest/sonuclar/v2_rapor.md](po3-backtest/sonuclar/v2_rapor.md).

## Neden v2?

v1'de ([po3-kural-seti-v1.md](po3-kural-seti-v1.md)) medyan stop mesafesi fiyatın %0,65'iydi. Bu yüzden komisyon ve kayma işlem başına 0,13–0,17R tutuyordu, maliyetsiz sonuç ise sıfır civarındaydı. v2'nin amacı, stopu genişleterek maliyetin R içindeki payını azaltmak.

## v1'den farkı

Diğer tüm kurallar (bias, Asya aralığı, süpürme, geri kapanış, MSS, FVG girişi, zaman çıkışı, maliyetler, %3 toplam risk sınırı) v1 ile aynıdır. Yalnızca iki şey eklendi:

| Bileşen | v2 kuralı |
|---|---|
| Asgari stop | Yapısal stop (süpürme ucu − 0,1 ATR) girişe fiyatın belirli bir yüzdesinden yakınsa ya **filtre** (işlem atlanır) ya da **genişlet** (stop bu mesafeye uzatılır) uygulanır |
| Hedef | Asya aralığının karşı tarafı ya da sabit 1,5R / 2R / 3R |

## Seçim yöntemi (sonuçlara bakmadan önce sabitlendi)

1. Aday ızgarası: gün açılışı {UTC, NY} × asgari stop {%0,6, %0,8, %1,0, %1,5} × mod {filtre, genişlet} × hedef {Asya, 1,5R, 2R, 3R} = 64 aday.
2. Seçim yalnızca örneklem içi işlemlerle (2021-01 → 2024-06) yapıldı: en az 150 işlemi olan adaylar arasında net R'si en yüksek olan.
3. Seçilen aday örneklem dışında (2024-06 → 2026-09) tek seferde sınandı.

Not: Örneklem dışı dönem v1 testinde zaten görülmüştü, yani tamamen "dokunulmamış" değil. v2 değişikliği bu dönemin sonuçlarından değil, v1'in maliyet analizinden çıkarıldı.

## Seçilen v2

**New York gece yarısı açılışı, asgari stop %1,5 (genişlet), hedef 2R.**

| Dönem | İşlem | Kazanma | Net R | PF |
|---|---|---|---|---|
| Örneklem içi | 331 | %43,5 | +0,060 | 1,11 |
| Örneklem dışı | 248 | %31,9 | −0,193 | 0,71 |

Örneklem içindeki küçük artı, örneklem dışında tersine döndü. Rastgele yönlü kıyas bile modelden iyi çıktı (−0,105R'ye karşı −0,193R).

## Kaldıraç

Stop her işlemde fiyatın %1,5'i olduğundan, %1 riskte pozisyon sermayenin ~0,7 katıdır (kaldıraç gerekmez). %2 riskte ~1,3x kaldıraç gerekir. Beklenti negatif olduğu için önerilebilecek bir risk yüzdesi yok.
