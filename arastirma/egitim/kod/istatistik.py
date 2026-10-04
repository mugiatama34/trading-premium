"""Eğitimdeki bazı popüler SMC/ICT iddialarını Binance 1 saatlik verisiyle basitçe sınar.

Amaç bir strateji kurmak değil; "bu iddia veride görünüyor mu?" sorusuna ilk, kaba bir cevap
vermektir. Sonuçlar sonuclar/istatistik.md dosyasına yazılır.

Maliyet varsayımı (yalnızca R hesaplanan testlerde): giriş ve çıkışta taker komisyon %0,05,
her yönde %0,02 kayma, 8 saat başına %0,01 fonlama (yönden bağımsız maliyet sayılır).
"""

import math
import random
from pathlib import Path

import kavramlar as k
import veri

COINLER = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
BASLANGIC, BITIS = "2023-01", "2026-08"
KOMISYON, KAYMA, FONLAMA_8S = 0.0005, 0.0002, 0.0001
STOP_YUZDE = []  # islem_r çağrılarının stop mesafeleri (fiyata oran)
SONUC = Path(__file__).parent.parent / "sonuclar" / "istatistik.md"


def ort(x):
    return sum(x) / len(x) if x else float("nan")


def medyan(x):
    x = sorted(x)
    return x[len(x) // 2] if x else float("nan")


def ga95(x):
    """Ortalama için kaba %95 güven aralığı (normal yaklaşım)."""
    if len(x) < 2:
        return float("nan"), float("nan")
    o = ort(x)
    s = math.sqrt(sum((v - o) ** 2 for v in x) / (len(x) - 1) / len(x))
    return o - 1.96 * s, o + 1.96 * s


def yuzde(a, b):
    return f"%{100 * a / b:.1f}" if b else "-"


# ---------------------------------------------------------------- 1) Eşit tepe/dipler
def esit_seviye_testi(m, a):
    """Eşit tepeler/dipler (likidite havuzu) tek tepe/diplere göre daha sık mı alınıyor?

    Uzaklık etkisini ayırmak için seviyeler, kesinleştiği andaki fiyata ATR cinsinden
    uzaklıklarına göre gruplanır. Sonuç: 48 saat içinde seviyenin aşılma oranı.
    """
    sonuc = {}
    for yon, noktalar in ((+1, k.swing_tepeler(m)), (-1, k.swing_dipler(m))):
        for idx, i in enumerate(noktalar):
            kes = i + 3
            if kes + 48 >= len(m):
                break
            L = m[i].h if yon > 0 else m[i].l
            esit = False
            for j in reversed(noktalar[:idx]):
                if j < i - 48:
                    break
                Lj = m[j].h if yon > 0 else m[j].l
                if abs(Lj - L) / L > 0.001:
                    continue
                arada = m[j + 1:i]
                ust = max(L, Lj) * 1.001
                alt = min(L, Lj) * 0.999
                if yon > 0 and all(x.h <= ust for x in arada):
                    esit = True
                if yon < 0 and all(x.l >= alt for x in arada):
                    esit = True
                break
            uz = (L - m[kes].c) * yon / a[kes]
            if uz < 0:
                continue  # kesinleşmeden önce zaten aşılmış
            kova = "0-1 ATR" if uz < 1 else "1-2 ATR" if uz < 2 else "2-4 ATR" if uz < 4 else None
            if kova is None:
                continue
            alindi = any((x.h > L) if yon > 0 else (x.l < L) for x in m[kes + 1:kes + 49])
            s = sonuc.setdefault((kova, esit), [0, 0])
            s[0] += alindi
            s[1] += 1
    return sonuc


# ---------------------------------------------------------------- 2) Önceki gün tepe/dip süpürmesi
def islem_r(m, giris_i, giris, stop, yon, sure=12):
    """Kapanışta girilen, stop ya da `sure` mum sonra kapanışta çıkan işlemin net R değeri."""
    risk = abs(giris - stop)
    if risk <= 0:
        return None
    STOP_YUZDE.append(risk / giris)
    cikis = None
    for x in m[giris_i + 1:giris_i + 1 + sure]:
        if (yon < 0 and x.h >= stop) or (yon > 0 and x.l <= stop):
            cikis = stop
            break
    if cikis is None:
        cikis = m[min(giris_i + sure, len(m) - 1)].c
    brut = (cikis - giris) * yon / risk
    maliyet = giris * (2 * KOMISYON + 2 * KAYMA + FONLAMA_8S * sure / 8) / risk
    return brut, brut - maliyet


def supurme_testi(m, pd):
    """PDH/PDL süpürmesi (fitil dışarı, kapanış içeri) sonrası 12 saat.

    Ayrıca iki giriş biçimi kıyaslanır:
    - Hemen ters giriş: süpürme mumunun kapanışında, stop süpürme fitilinin ucunda.
    - Onaylı giriş: 6 mum içinde 1 saatlik yapı bozulması (son swing dibinin/tepesinin
      kapanışla kırılması) olursa o kapanışta, stop süpürme tepesinde/dibinde.
    """
    tepeler, dipler = k.swing_tepeler(m), k.swing_dipler(m)
    r = {"sup_getiri": [], "kirilim_getiri": [], "hemen": [], "onayli": [], "onayli_brut": [],
         "hemen_brut": [], "olay": 0}
    gorulen = set()
    for i in range(30, len(m) - 13):
        if pd[i] is None:
            continue
        PDH, PDL = pd[i]
        gun = m[i].t // 86_400_000
        for yon, seviye in ((-1, PDH), (+1, PDL)):  # yon: beklenen dönüş yönü
            if (gun, yon) in gorulen:
                continue
            asti = m[i].h > seviye if yon < 0 else m[i].l < seviye
            if not asti:
                continue
            gorulen.add((gun, yon))  # günün ilk aşımı
            getiri = (m[i + 12].c / m[i].c - 1) * yon
            icerde = m[i].c < seviye if yon < 0 else m[i].c > seviye
            if not icerde:
                r["kirilim_getiri"].append(getiri)
                continue
            r["olay"] += 1
            r["sup_getiri"].append(getiri)
            uc = m[i].h if yon < 0 else m[i].l
            STOP_YUZDE.clear()
            h = islem_r(m, i, m[i].c, uc, yon)
            r.setdefault("hemen_stop", []).extend(STOP_YUZDE)
            if h:
                r["hemen_brut"].append(h[0])
                r["hemen"].append(h[1])
            # onay: son kesinleşmiş swing noktasının kapanışla kırılması
            liste = dipler if yon < 0 else tepeler
            onceki = [s for s in liste if s + 3 <= i]
            if not onceki:
                continue
            s = onceki[-1]
            yapi = m[s].l if yon < 0 else m[s].h
            for j in range(i + 1, min(i + 7, len(m) - 13)):
                uc = max(uc, m[j].h) if yon < 0 else min(uc, m[j].l)
                if (yon < 0 and m[j].h > max(PDH, m[i].h)) or (yon > 0 and m[j].l < min(PDL, m[i].l)):
                    break  # süpürme ucu aşıldı, kurulum bozuldu
                if (yon < 0 and m[j].c < yapi) or (yon > 0 and m[j].c > yapi):
                    STOP_YUZDE.clear()
                    h = islem_r(m, j, m[j].c, uc, yon)
                    r.setdefault("onayli_stop", []).extend(STOP_YUZDE)
                    if h:
                        r["onayli_brut"].append(h[0])
                        r["onayli"].append(h[1])
                    break
    return r


# ---------------------------------------------------------------- 3) FVG doldurma ve tepki
def fvg_testi(m, a):
    """1 saatlik FVG'ler (en az %0,1 boyutunda): orta noktaya 24 saatte dönüş oranı, aynı
    uzaklıktaki ayna seviyeye dönüş oranıyla kıyaslanır. Orta noktaya dokunulduğunda ise
    simetrik ±mesafe bariyerinden hangisinin önce vurulduğu ölçülür (rastgele ≈ %50)."""
    r = {"n": 0, "orta": 0, "ayna": 0, "tepki_kazan": 0, "tepki_n": 0}
    for i, yon, alt, ust in k.fvg_listesi(m, 0.001):
        bas = i + 2
        if bas + 36 >= len(m):
            break
        orta = (alt + ust) / 2
        ref = m[i + 1].c
        ayna = ref + (ref - orta)
        r["n"] += 1
        pencere = m[bas:bas + 24]
        dokunus = next((t for t, x in enumerate(pencere, bas)
                        if (x.l <= orta if yon > 0 else x.h >= orta)), None)
        r["orta"] += dokunus is not None
        r["ayna"] += any((x.h >= ayna) if yon > 0 else (x.l <= ayna) for x in pencere)
        if dokunus is None:
            continue
        mesafe = max(ust - alt, 0.5 * a[dokunus])
        hedef, stop = orta + yon * mesafe, orta - yon * mesafe
        for x in m[dokunus + 1:dokunus + 13]:
            st = x.l <= stop if yon > 0 else x.h >= stop
            hd = x.h >= hedef if yon > 0 else x.l <= hedef
            if st or hd:
                r["tepki_n"] += 1
                r["tepki_kazan"] += hd and not st  # aynı mumda ikisi: kayıp sayılır
                break
    return r


# ---------------------------------------------------------------- 4) Premium / discount
def pd_bolge_testi(m, pd):
    """Fiyatın önceki gün aralığındaki konumuna göre sonraki 24 saatin getirisi."""
    kovalar = {}
    for i in range(0, len(m) - 24, 4):  # örtüşmeyi azaltmak için 4 saatte bir
        if pd[i] is None:
            continue
        PDH, PDL = pd[i]
        p = (m[i].c - PDL) / (PDH - PDL)
        ad = ("1) PDL altı" if p < 0 else "2) Discount (0-%25)" if p < 0.25 else
              "3) Discount (%25-50)" if p < 0.5 else "4) Premium (%50-75)" if p < 0.75 else
              "5) Premium (%75-100)" if p <= 1 else "6) PDH üstü")
        kovalar.setdefault(ad, []).append(m[i + 24].c / m[i].c - 1)
    return kovalar


def main():
    random.seed(1)
    satirlar = ["# Eğitim İçin Basit Veri Kontrolleri", "",
                f"Veri: Binance USDT-M vadeli, 1 saatlik mumlar, {BASLANGIC} → {BITIS}, "
                f"{', '.join(c[:-4] for c in COINLER)}. Kod: `kod/istatistik.py`.", "",
                "Bunlar strateji testi değil, kavramların veride iz bırakıp bırakmadığına dair ilk "
                "bakıştır. Tek bir mekanik tanım kullanıldı; farklı tanımlar farklı sonuç verebilir.",
                ""]
    toplam_esit, toplam_sup, toplam_fvg, toplam_pd = {}, {}, {}, {}
    for coin in COINLER:
        m = veri.mumlar(coin, BASLANGIC, BITIS)
        a, pd = k.atr(m), k.gunluk_seviyeler(m)
        for anahtar, (x, n) in esit_seviye_testi(m, a).items():
            t = toplam_esit.setdefault(anahtar, [0, 0])
            t[0] += x
            t[1] += n
        s = supurme_testi(m, pd)
        toplam_sup[coin] = s
        f = fvg_testi(m, a)
        for kk, v in f.items():
            toplam_fvg[kk] = toplam_fvg.get(kk, 0) + v
        for kk, v in pd_bolge_testi(m, pd).items():
            toplam_pd.setdefault(kk, []).extend(v)
        print(coin, len(m), "mum")

    satirlar += ["## 1) Eşit tepe/dipler gerçekten \"mıknatıs\" mı? (Modül 2)", "",
                 "Soru: Eşit tepe/dip (iki tepe/dip %0,1 içinde) üzerindeki likidite, tek bir "
                 "swing tepe/dibe göre daha sık mı alınıyor? Ölçüt: seviyenin 48 saat içinde aşılma oranı.",
                 "", "| Uzaklık | Eşit seviye | Tek seviye |", "|---|---|---|"]
    for kova in ("0-1 ATR", "1-2 ATR", "2-4 ATR"):
        e, t = toplam_esit.get((kova, True), [0, 0]), toplam_esit.get((kova, False), [0, 0])
        satirlar.append(f"| {kova} | {yuzde(*e)} (n={e[1]}) | {yuzde(*t)} (n={t[1]}) |")
    satirlar.append("")

    satirlar += ["## 2) Önceki gün tepe/dip süpürmesi ve giriş biçimleri (Modül 2, 5, 6)", "",
                 "Süpürme: mum önceki günün tepesini (PDH) fitille aşıp altında kapatıyor "
                 "(PDL için tersi); günün ilk aşımı sayılır. Kırılım: aşan mum dışarıda kapatıyor.",
                 "Getiriler beklenen dönüş yönünde, 12 saat sonrası, maliyetsiz. "
                 "R değerleri maliyet dahil (net).", "",
                 "| Coin | Süpürme sayısı | 12s dönüş yönü oranı | Ort. 12s getiri (süpürme) | "
                 "Ort. 12s getiri (kırılım, aynı yön) | Hemen ters giriş net R (brüt) | "
                 "Onaylı giriş: işlem / net R (brüt) |", "|---|---|---|---|---|---|---|"]
    tum = {"hemen": [], "onayli": [], "sup_getiri": [], "kirilim_getiri": [],
           "hemen_stop": [], "onayli_stop": []}
    for coin, s in toplam_sup.items():
        for kk in tum:
            tum[kk] += s.get(kk, [])
        pozitif = sum(1 for g in s["sup_getiri"] if g > 0)
        satirlar.append(
            f"| {coin[:-4]} | {s['olay']} | {yuzde(pozitif, len(s['sup_getiri']))} | "
            f"%{100 * ort(s['sup_getiri']):+.3f} | %{100 * ort(s['kirilim_getiri']):+.3f} | "
            f"{ort(s['hemen']):+.3f} ({ort(s['hemen_brut']):+.3f}) | "
            f"{len(s['onayli'])} / {ort(s['onayli']):+.3f} ({ort(s['onayli_brut']):+.3f}) |")
    lo, hi = ga95(tum["hemen"])
    lo2, hi2 = ga95(tum["onayli"])
    satirlar += ["", f"Üç coin birlikte: hemen ters giriş {len(tum['hemen'])} işlem, net "
                 f"{ort(tum['hemen']):+.3f}R (%95 GA {lo:+.3f} … {hi:+.3f}); onaylı giriş "
                 f"{len(tum['onayli'])} işlem, net {ort(tum['onayli']):+.3f}R "
                 f"(%95 GA {lo2:+.3f} … {hi2:+.3f}).", "",
                 f"Medyan stop mesafesi: hemen ters girişte %{100 * medyan(tum['hemen_stop']):.2f}, "
                 f"onaylı girişte %{100 * medyan(tum['onayli_stop']):.2f}. Gidiş-dönüş maliyeti "
                 f"yaklaşık %{100 * (2 * KOMISYON + 2 * KAYMA + FONLAMA_8S * 12 / 8):.3f} olduğundan "
                 "dar stop, maliyetin R cinsinden büyümesine yol açar.", "",
                 "Not: Kırılım sütunu süpürmeyle aynı yönde ölçülür; negatifse kırılımdan sonra "
                 "fiyat kırılım yönünde devam etme eğilimindedir (PO3 çalışmasındaki devam eğilimiyle tutarlı).",
                 ""]

    f = toplam_fvg
    satirlar += ["## 3) FVG'ler doldurulur mu, dokunulunca tepki verir mi? (Modül 3, 4)", "",
                 f"1 saatlik, fiyatın en az %0,1'i büyüklüğünde {f['n']} FVG.", "",
                 "| Ölçüt | Sonuç |", "|---|---|",
                 f"| 24 saatte FVG orta noktasına dönüş | {yuzde(f['orta'], f['n'])} |",
                 f"| 24 saatte aynı uzaklıktaki ayna seviyeye gidiş (kıyas) | {yuzde(f['ayna'], f['n'])} |",
                 f"| Orta noktaya dokunduktan sonra simetrik hedefin stoptan önce gelmesi "
                 f"(rastgele ≈ %50, maliyetsiz) | {yuzde(f['tepki_kazan'], f['tepki_n'])} "
                 f"(n={f['tepki_n']}) |", ""]

    satirlar += ["## 4) Premium / discount: ucuz bölgeden alım daha mı iyi? (Modül 5)", "",
                 "Fiyatın önceki gün aralığındaki konumu ve sonraki 24 saatin ortalama getirisi "
                 "(üç coin, 4 saatte bir örnek, maliyetsiz).", "",
                 "| Bölge | Örnek | Ort. 24s getiri | Yükselme oranı |", "|---|---|---|---|"]
    for ad in sorted(toplam_pd):
        v = toplam_pd[ad]
        satirlar.append(f"| {ad} | {len(v)} | %{100 * ort(v):+.3f} | "
                        f"{yuzde(sum(1 for g in v if g > 0), len(v))} |")
    satirlar.append("")
    SONUC.parent.mkdir(exist_ok=True)
    SONUC.write_text("\n".join(satirlar) + "\n")
    print("\n".join(satirlar))


if __name__ == "__main__":
    main()
