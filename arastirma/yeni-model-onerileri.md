# Yeni Model Ailesi Önerileri

Tarih: 2026-10-04. Durum: öneri; kullanıcı seçimi bekleniyor.

PO3/AMD ve Asya aralığına dayalı modeller bırakıldı (`context/kararlar.md`, sonuçlar `po3-backtest/sonuclar/ozet.md`). Bu çalışmadan çıkan üç ders sonraki modelin seçimini belirliyor:

1. **Maliyet, gün içi modelleri öldürüyor.** Gün içi stoplarda bir giriş-çıkış 0,05–0,17R tutuyor. Daha seyrek işlem yapan ve daha geniş stop kullanan modellerde maliyetin payı çok daha küçük olur.
2. **Coinler birlikte hareket ediyor.** 17 coin aynı gün aynı yöne sinyal veriyor; %3 toplam risk sınırı işlemlerin yarısını atlıyor. Coinleri birbirine göre değerlendiren modeller bu sorunu yaşamaz.
3. **Altyapı hazır.** 17 coinin 2021-01 → 2026-09 arası 5 dakikalık mumları ve gerçek fonlama oranları indirildi. Backtest motoru, maliyet modeli, örneklem içi/dışı ayrımı, rastgele kıyas ve Monte Carlo yeniden kullanılabilir.

## Öneriler

| | Model ailesi | Fikir | Neden umut verici | Riskler |
|---|---|---|---|---|
| **A (önerim)** | Zaman serisi trendi (trend takibi) | Günlük mumlarda fiyat, son N günün en yükseğini kırınca uzun, en düşüğünü kırınca kısa (ya da hareketli ortalama kesişimi); oynaklığa göre pozisyon boyutu, iz süren stop | Kripto ve diğer piyasalarda trend takibinin uzun dönemde çalıştığı akademik çalışmalarda raporlanmıştır (bizim veride doğrulanmalı). Haftada birkaç işlem, geniş stop, maliyet payı küçük. Kuralları basit ve tamamen mekanik | Uzun yatay dönemlerde art arda küçük kayıplar; kazanma oranı düşük (%30–40), sabır ister; sonuç birkaç büyük trende bağlıdır |
| B | Kesitsel momentum (göreli güç) | Her hafta 17 coini son 1–4 haftalık getiriye göre sırala; en güçlüleri uzun, en zayıfları kısa al | Piyasa yönünden büyük ölçüde bağımsızdır, coinlerin birlikte hareketi sorun olmaz. Haftalık yeniden dengeleme, düşük işlem maliyeti | Kısa bacakta fonlama maliyeti ve sert yukarı sıçramalar; 17 coin küçük bir evren; yeni coinlerin kısa geçmişi |
| C | Fonlama oranı tabanlı | Fonlama aşırı pozitifken (kalabalık uzun) kısa ya da aşırı negatifken uzun pozisyon; ya da fonlamayı toplayan pozisyon | Fonlama verisi elimizde; kalabalık pozisyonlanma ölçülebilir bir veridir | Aşırı fonlama uzun süre aşırı kalabilir; sinyal seyrek; spot-vadeli taşıma (carry) için spot hesabı ve iki bacak gerekir, kural dışına çıkabilir |

## Neden A?

- En az varsayımlı ve en kolay doğrulanabilir aile. Kullanıcının seviyesine (başlangıç-orta) uygun: kurallar birkaç satırdır ve grafikte aynı şekilde görülebilir.
- PO3'teki iki ana sorunu (yüksek maliyet payı, dar stop) yapısı gereği çözer.
- Aynı yöntemle sınanır: kurallar ve aday ızgarası önceden sabitlenir, seçim yalnızca 2024-06 öncesi veride yapılır, sonuç örneklem dışında tek seferde ölçülür ve aynı devam eşikleriyle değerlendirilir.

Not: Örneklem dışı dönem (2024-06 → 2026-09) PO3 çalışmalarında çok kez görüldü, ama trend modeli için hiç kullanılmadı. Yine de ileride paper trading en güvenilir test olacak.
