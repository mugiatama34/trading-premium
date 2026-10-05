"""PO3 kural seti v2: geniş stop. Seçim örneklem içinde yapılır, örneklem dışı tek seferde sınanır.

v1'in ana sorunu dar stoplardı (medyan %0,65): komisyon ve kayma işlem başına 0,13–0,17R tutuyordu.
v2, v1'e yalnızca asgari stop mesafesi ve hedef seçeneği ekler. Diğer tüm kurallar v1 ile aynıdır.

Önceden sabitlenen seçim kuralı:
  1. Aday ızgarası: gün açılışı {UTC, NY} × asgari stop {%0,6, %0,8, %1,0, %1,5}
     × mod {filtre, genişlet} × hedef {Asya karşı tarafı, 1,5R, 2R, 3R} = 64 aday.
  2. Yalnızca örneklem içi işlemler (2024-06-01 öncesi) kullanılır.
  3. Örneklem içinde en az 150 işlemi olan adaylar arasından net R ortalaması en yüksek olan seçilir.
  4. Seçilen aday örneklem dışında devam eşikleriyle sınanır. Tüm adayların örneklem dışı sonuçları da
     raporlanır ki seçimin şansa bağlı olup olmadığı görülsün.

Kullanım:  python v2_secim.py      Çıktı: sonuclar/v2_rapor.md, sonuclar/v2_islemler.csv
"""

import csv
from datetime import datetime, timezone
from itertools import product

import backtest as B
import kurallar as K

ASGARI = (0.6, 0.8, 1.0, 1.5)
MODLAR = ("filtre", "genislet")
HEDEFLER = ("asya", "1.5R", "2R", "3R")
EN_AZ_ICINDE = 150


def etiket(k: K.Kurallar) -> str:
    acilis = "UTC" if k.ad == "utc" else "NY"
    hedef = "Asya" if k.hedef == "asya" else k.hedef
    if k.min_stop_modu == "yok":
        return f"{acilis}, v1, hedef {hedef}"
    return f"{acilis}, stop ≥ %{k.min_stop_yuzde:g} ({k.min_stop_modu}), hedef {hedef}"


def main():
    veriler = B.veri_yukle()
    bit_ts = max(v["ts"][-1] for v, _, _ in veriler.values())
    oos = B.ms(datetime.fromisoformat(K.ORNEKLEM_DISI_BASLANGIC).replace(tzinfo=timezone.utc))

    def calistir(k, rastgele=False):
        tum = []
        for coin, (v, atr, fon) in veriler.items():
            tum += B.coin_backtest(coin, v, atr, fon, k, rastgele)[0]
        return [x for x in tum if x["giris_zamani"] < oos], [x for x in tum if x["giris_zamani"] >= oos]

    adaylar = []
    for ad, asgari, mod, hedef in product(K.TEMEL, ASGARI, MODLAR, HEDEFLER):
        k = K.degistir(K.TEMEL[ad], min_stop_yuzde=asgari, min_stop_modu=mod, hedef=hedef)
        ic, dis = calistir(k)
        adaylar.append((k, B.ozet(ic), B.ozet(dis)))
        print(etiket(k), len(ic), len(dis), flush=True)
    v1 = []
    for ad, hedef in product(K.TEMEL, ("asya", "2R")):
        k = K.degistir(K.TEMEL[ad], hedef=hedef)
        ic, dis = calistir(k)
        v1.append((k, B.ozet(ic), B.ozet(dis)))

    uygun = [a for a in adaylar if a[1] and a[1]["n"] >= EN_AZ_ICINDE]
    secilen = max(uygun, key=lambda a: a[1]["net_r"])[0]
    ic, dis = calistir(secilen, rastgele=True)
    o_ic, o_dis = B.ozet(ic), B.ozet(dis)

    s = ["# PO3 Kural Seti v2 (geniş stop): Sonuçlar\n",
         "Kod: `v2_secim.py` (seçim kuralı dosyanın başında), motor: `backtest.py`. Kurallar: "
         "[../../po3-kural-seti-v2.md](../../po3-kural-seti-v2.md). Maliyetler v1 ile aynı: maker %0,02 "
         "giriş ve hedef, taker %0,05 + kayma stop ve zaman çıkışı, gerçek fonlama.\n",
         f"Örneklem içi: 2021-01 → {K.ORNEKLEM_DISI_BASLANGIC}. Örneklem dışı: sonrası → 2026-09.\n",
         f"\n## Seçilen v2: {etiket(secilen)}\n",
         f"Seçim yalnızca örneklem içi sonuçlara göre yapıldı ({len(uygun)} uygun aday arasında en yüksek net R).\n",
         B.BASLIK,
         f"| Örneklem içi " + B.bicim(o_ic),
         f"| Örneklem dışı " + B.bicim(o_dis)]
    if o_dis:
        p1 = B.portfoy(dis, 1.0, oos, bit_ts)
        r_ort, r_min, r_max, r_p = B.rastgele_ozet(dis)
        s.append("\n**Örneklem dışı, devam eşikleri:**\n")
        s.append(B.esik_tablosu(o_dis, p1, r_p))
        s.append(f"\nRastgele yönlü kıyas ({B.RASTGELE_TOHUM} tohum): ortalama net R {r_ort:+.3f} "
                 f"(tohumlar {r_min:+.3f} … {r_max:+.3f}); model {o_dis['net_r']:+.3f}.\n")
        dagilim = ", ".join(f"{a} %{100 * sum(1 for x in dis if x['sonuc'] == a) / len(dis):.1f}"
                            for a in ("hedef", "stop", "zaman"))
        s.append(f"\nÖrneklem dışı sonuç dağılımı: {dagilim}. Ortalama kazanç {o_dis['ort_kazanc']:+.2f}R, "
                 f"ortalama kayıp {o_dis['ort_kayip']:+.2f}R. İşlem başına maliyet "
                 f"{o_dis['brut_r'] - o_dis['net_r']:.3f}R.\n")
        s.append("\n**Örneklem dışı portföy (10.000 $, aynı yönde en fazla %3 açık risk):**\n")
        s.append("| Risk/işlem | Alınan işlem | Atlanan | Son sermaye | Yıllık getiri | Maks. düşüş |\n|---|---|---|---|---|---|")
        for r in (1.0, 2.0):
            p = B.portfoy(dis, r, oos, bit_ts)
            s.append(f"| %{r:.0f} | {p['alinan']} | {p['atlanan']} | {p['son']:,.0f} $ | %{p['yillik']:.1f} | %{p['dd']:.1f} |")
        mc50, mc95 = B.monte_carlo(dis)
        s.append(f"\nMonte Carlo (örneklem dışı, %1 risk): medyan maks. düşüş %{mc50:.1f}, %95 kötü durumda %{mc95:.1f}.\n")
        s.append(f"\nGereken kaldıraç: %1 riskte {B.kaldirac_satiri(ic + dis, 1)}; %2 riskte {B.kaldirac_satiri(ic + dis, 2)}.\n")
        s.append("\n**Yıllara göre (tüm dönem):**\n")
        s.append(B.yil_tablosu(ic + dis))
        s.append("\n**Coinlere göre (örneklem dışı):**\n")
        s.append(B.BASLIK)
        for c in sorted({x["coin"] for x in dis}):
            s.append(f"| {c} " + B.bicim(B.ozet([x for x in dis if x["coin"] == c])))

    s.append("\n## Tüm adaylar (örneklem içi sıralı)\n")
    s.append("Örneklem dışı sütunları seçimde kullanılmadı; seçimin şansa bağlı olup olmadığını görmek için verilir.\n")
    s.append("| Aday | İçi işlem | İçi net R | İçi PF | Dışı işlem | Dışı net R | Dışı PF |\n|---|---|---|---|---|---|---|")

    def satir(k, a, b):
        f = lambda o: f"{o['n']} | {o['net_r']:+.3f} | {o['pf']:.2f}" if o else "0 | – | –"
        isaret = " **(seçilen)**" if k == secilen else ""
        return f"| {etiket(k)}{isaret} | {f(a)} | {f(b)} |"

    for k, a, b in v1:
        s.append(satir(k, a, b))
    for k, a, b in sorted(adaylar, key=lambda x: -(x[1]["net_r"] if x[1] else -9)):
        s.append(satir(k, a, b))
    gecen = sum(1 for _, _, b in adaylar if b and b["net_r"] >= 0.15 and b["pf"] >= 1.3)
    pozitif = sum(1 for _, _, b in adaylar if b and b["net_r"] > 0)
    s.append(f"\n64 adaydan örneklem dışında net R'si pozitif olan: {pozitif}; beklenti ve PF eşiğini "
             f"birlikte geçen: {gecen}.\n")

    (B.CIKTI / "v2_rapor.md").write_text("\n".join(s) + "\n", encoding="utf-8")
    with open(B.CIKTI / "v2_islemler.csv", "w", newline="", encoding="utf-8") as f:
        alanlar = [a for a in (ic + dis)[0] if a != "rastgele_net_r"]
        w = csv.DictWriter(f, fieldnames=alanlar, extrasaction="ignore")
        w.writeheader()
        for x in ic + dis:
            satir_ = dict(x)
            for a in ("giris_zamani", "cikis_zamani"):
                satir_[a] = datetime.fromtimestamp(x[a] / 1000, timezone.utc).isoformat()
            w.writerow(satir_)
    print("Seçilen:", etiket(secilen))


if __name__ == "__main__":
    main()
