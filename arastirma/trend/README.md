# Trend Takibi Modeli

PO3/AMD bırakıldıktan sonra seçilen yeni model ailesi ([../yeni-model-onerileri.md](../yeni-model-onerileri.md)). Günlük mumlarda N günlük kırılımla giriş, ATR'ye dayalı iz süren stopla çıkış.

Sonuç (2026-10-05): seçilen model (N = 20, stop 3 × ATR, yalnızca uzun) örneklem dışında devam eşiklerini geçti. Sıradaki adım paper trading. Özet: [sonuclar/ozet.md](sonuclar/ozet.md).

| Dosya | Görevi |
|---|---|
| `trend.py` | Kurallar ve seçim yöntemi (dosyanın başında), 18 adayın örneklem içi taraması, örneklem dışı test, rastgele kıyas, portföy; `sonuclar/rapor.md` ve `sonuclar/islemler.csv` üretir |
| `sonuclar/ozet.md` | Sonuçların özeti, eşiklerle karşılaştırma ve dikkat edilmesi gerekenler |

Veri ve ortak hesaplar `../po3-backtest/` ve `../po3-istatistik/` klasörlerinden kullanılır (5 dk mumlar `veri_indir.py`, fonlama `fonlama_indir.py` ile indirilir). Kod yalnızca standart Python kullanır.
