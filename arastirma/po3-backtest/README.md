# PO3 Kural Seti v1 Backtesti (Aşama 4)

Yol haritasının ([../yol-haritasi-po3-amd.md](../yol-haritasi-po3-amd.md)) 4. aşaması: [kural seti v1](../po3-kural-seti-v1.md) MSS ve FVG onaylarıyla, maliyetler dahil, örneklem içi/dışı ayrımıyla test edilir.

Sonuç (2026-10-03): v1 de [v2](../po3-kural-seti-v2.md) de eşikleri geçmedi. Özet: [sonuclar/ozet.md](sonuclar/ozet.md).

## Dosyalar

| Dosya | Görevi |
|---|---|
| `kurallar.py` | Kural parametreleri (iki gün açılışı varyantı), maliyetler, sermaye ve risk sınırları |
| `backtest.py` | Sinyal, işlem simülasyonu, portföy (%3 toplam risk sınırı), rastgele kıyas, Monte Carlo, sağlamlık; `sonuclar/rapor.md` ve `sonuclar/islemler.csv` üretir |
| `v2_secim.py` | Kural seti v2 (geniş stop): 64 adayı örneklem içinde tarar, en iyisini seçer, örneklem dışında sınar; `sonuclar/v2_rapor.md` ve `sonuclar/v2_islemler.csv` üretir |
| `fonlama_indir.py` | Binance herkese açık arşivinden geçmiş fonlama oranlarını indirir (API anahtarı gerekmez) |
| `sonuclar/ozet.md` | Sonuçların özeti, eşiklerle karşılaştırma ve yorum |

Kod yalnızca standart Python kullanır. Mum verisi `../po3-istatistik/veri_indir.py` ile, fonlama verisi `fonlama_indir.py` ile `../po3-istatistik/veri/` altına indirilir ve depoya eklenmez.

## Yöntem notları

- **Geleceğe bakma yok:** Her adım yalnızca o ana kadar kapanmış mumları kullanır. MSS seviyesi süpürmeden önce teyit edilmiş tepedir; limit emir FVG ve MSS tamamlandıktan sonra verilir.
- **Temkinli dolum:** Limit emir, fiyat seviyenin altına inmedikçe dolmuş sayılmaz. Aynı mumda stop ve hedef varsa stop sayılır.
- **Rastgele kıyas:** Her işlem için aynı anda, aynı fiyattan, aynı stop ve hedef mesafesiyle rastgele yönde 20 kopya işlem simüle edilir.
- **Örneklem ayrımı:** 2024-06-01 öncesi geliştirme, sonrası test. Parametreler önceden sabitlendi; sonuçlara göre ayar yapılmadı.
