# Kurallar ve Sınırlar

Bu dosya projede her zaman dikkate alınması gereken kalıcı kuralları, sınırları ve yasakları içerir.

## Zorunlu kurallar

<!-- Her çalışmada uygulanması gereken proje kuralları. -->

- Backtest ve performans sonuçları her zaman komisyon, kayma (slippage) ve fonlama maliyeti dahil raporlanır.
- Her işlemde toplam sermayenin %1–2'si kadar risk alınır.
- Aksi belirtilmedikçe başlangıç sermayesi 10.000 $ kabul edilir.
- Kaldıraç sabit değildir; her model için risk oranı dikkate alınarak getiriyi en üst düzeye çıkaracak şekilde belirlenir ve gerekçesi yazılır.
- Bir yöntem gerçek parayla kullanılmaya uygun olarak sunulmadan önce paper trading ile denenmiş olmalıdır.
- Backtest ve bot kodları Python ile yazılır.
- Analiz ve backtest çıktıları depodaki `arastirma/` klasörüne kaydedilir.

## Yapılmaması gerekenler

<!-- Kesin yasakları ve kaçınılması gereken davranışları yazın. -->

- Ajan borsada gerçek emir vermez, gerçek hesaba bağlanmaz ve API anahtarı kullanmaz.

## Bütçe, süre ve kaynak sınırları

<!-- Varsa maliyet, zaman, ekip veya araç sınırlamaları. -->

## Hukuki, güvenlik ve gizlilik sınırları

<!-- Kişisel veriler, lisanslar, sözleşmeler veya güvenlik gereklilikleri. -->

## Kullanıcı onayı gerektiren işlemler

<!-- Yayımlama, silme, ödeme, dışarıya mesaj gönderme gibi onay gerektiren işlemler. -->

- Gerçek parayla işlem yapılması yalnızca kullanıcının kararıdır; ajan bu adımı kendisi atmaz.
