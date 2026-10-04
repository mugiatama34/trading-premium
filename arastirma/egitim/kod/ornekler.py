"""Eğitim modülleri için BTCUSDT 1 saatlik gerçek grafik örneklerini metin (ASCII) olarak çizer.

Örnekler kurallarla otomatik seçilir (elle seçilmiş "güzel" grafikler değildir) ve hem işe yarayan
hem de bozulan kurulumlar gösterilir. Çıktı: sonuclar/ornekler.md
"""

from pathlib import Path

import kavramlar as k
import veri

SONUC = Path(__file__).parent.parent / "sonuclar" / "ornekler.md"
YUKSEKLIK = 22


def ciz(m, bas, bit, seviyeler=(), isaretler=None, kutular=()):
    """m[bas:bit] mumlarını çizer.

    seviyeler: [(fiyat, etiket)] yatay çizgiler. isaretler: {indeks: harf} alt satırda.
    kutular: [(ilk_indeks, alt, ust, karakter)] FVG gibi bölgeleri boş alanda gösterir.
    """
    isaretler = isaretler or {}
    parca = m[bas:bit]
    ust = max(x.h for x in parca)
    alt = min(x.l for x in parca)
    for f, _ in seviyeler:
        ust, alt = max(ust, f), min(alt, f)
    adim = (ust - alt) / (YUKSEKLIK - 1)

    def satir(f):
        return round((ust - f) / adim)

    izgara = [[" "] * (2 * len(parca)) for _ in range(YUKSEKLIK)]
    for ilk, a, u, ch in kutular:
        for kol in range(2 * (ilk - bas), 2 * len(parca)):
            for r in range(satir(u), satir(a) + 1):
                izgara[r][kol] = ch
    etiketler = {}
    for f, ad in seviyeler:
        r = satir(f)
        for kol in range(2 * len(parca)):
            if izgara[r][kol] == " ":
                izgara[r][kol] = "-"
        etiketler[r] = (etiketler[r] + " / " if r in etiketler else "") + ad
    for n, x in enumerate(parca):
        govde_ust, govde_alt = satir(max(x.o, x.c)), satir(min(x.o, x.c))
        for r in range(satir(x.h), satir(x.l) + 1):
            izgara[r][2 * n] = ("█" if x.c >= x.o else "▒") if govde_ust <= r <= govde_alt else "│"
    cikti = []
    for r, sat in enumerate(izgara):
        fiyat = ust - r * adim
        cikti.append(f"{fiyat:>9,.0f} ┤{''.join(sat)}" + (f"  ← {etiketler[r]}" if r in etiketler else ""))
    alt_satir = [" "] * (2 * len(parca))
    zaman = [" "] * (2 * len(parca))
    for i, h in isaretler.items():
        if bas <= i < bit:
            alt_satir[2 * (i - bas)] = h
    for n, x in enumerate(parca):
        if x.zaman.hour % 6 == 0 and 2 * n + 5 <= len(zaman):
            zaman[2 * n:2 * n + 5] = list(x.zaman.strftime("%H:00"))
    cikti.append(" " * 10 + "└" + "─" * (2 * len(parca)))
    cikti.append(" " * 11 + "".join(alt_satir))
    cikti.append(" " * 11 + "".join(zaman))
    return "\n".join(cikti)


def yapi_ornegi(m):
    """Piyasa yapısı: swing tepe/dipleri ve HH/HL/LH/LL etiketleri."""
    bas, bit = 24 * 40, 24 * 40 + 48  # 2025 başından sabit bir pencere
    tepeler = [i for i in k.swing_tepeler(m) if bas <= i < bit]
    dipler = [i for i in k.swing_dipler(m) if bas <= i < bit]
    isaret, notlar = {}, []
    for liste, ad, fn in ((tepeler, "T", lambda i: m[i].h), (dipler, "D", lambda i: m[i].l)):
        onceki = None
        for i in liste:
            if onceki is None:
                etiket = ad
            elif ad == "T":
                etiket = "HH" if fn(i) > fn(onceki) else "LH"
            else:
                etiket = "HL" if fn(i) > fn(onceki) else "LL"
            isaret[i] = ad
            notlar.append((i, f"{m[i].zaman:%d.%m %H:00} {'tepe' if ad == 'T' else 'dip'} "
                              f"{fn(i):,.0f} → {etiket}"))
            onceki = i
    notlar.sort()
    return bas, bit, ciz(m, bas, bit, isaretler=isaret), [n for _, n in notlar]


def supurme_kurulumlari(m):
    """PDH/PDL süpürmesi + 6 mum içinde 1 saatlik yapı bozulması (MSS) + FVG olan kurulumlar."""
    pd = k.gunluk_seviyeler(m)
    tepeler, dipler = k.swing_tepeler(m), k.swing_dipler(m)
    fvgler = {i: (y, a, u) for i, y, a, u in k.fvg_listesi(m, 0.0005)}
    sonuc, gorulen = [], set()
    for i in range(30, len(m) - 30):
        if pd[i] is None:
            continue
        PDH, PDL = pd[i]
        gun = m[i].t // 86_400_000
        for yon, seviye in ((-1, PDH), (+1, PDL)):
            if (gun, yon) in gorulen:
                continue
            if not (m[i].h > seviye if yon < 0 else m[i].l < seviye):
                continue
            gorulen.add((gun, yon))
            if not (m[i].c < seviye if yon < 0 else m[i].c > seviye):
                continue
            liste = dipler if yon < 0 else tepeler
            onceki = [s for s in liste if s + 3 <= i]
            if not onceki:
                continue
            s = onceki[-1]
            yapi = m[s].l if yon < 0 else m[s].h
            uc = m[i].h if yon < 0 else m[i].l
            for j in range(i + 1, i + 7):
                uc = max(uc, m[j].h) if yon < 0 else min(uc, m[j].l)
                if (yon < 0 and m[j].c < yapi) or (yon > 0 and m[j].c > yapi):
                    fvg = next(((f, fvgler[f]) for f in range(i, j + 1)
                                if f in fvgler and fvgler[f][0] == yon), None)
                    if fvg:
                        risk = abs(m[j].c - uc)
                        hedef = m[j].c + yon * 2 * risk
                        sonuc_ = "süre doldu"
                        for t in range(j + 1, j + 25):
                            if (yon < 0 and m[t].h >= uc) or (yon > 0 and m[t].l <= uc):
                                sonuc_ = "stop"
                                break
                            if (yon < 0 and m[t].l <= hedef) or (yon > 0 and m[t].h >= hedef):
                                sonuc_ = "hedef"
                                break
                        sonuc.append(dict(sup=i, yon=yon, seviye=seviye, yapi_i=s, yapi=yapi,
                                          mss=j, fvg=fvg, stop=uc, hedef=hedef, sonuc=sonuc_, son=t))
                    break
    return sonuc


def kurulum_ciz(m, ks, baslik):
    i, j, yon = ks["sup"], ks["mss"], ks["yon"]
    bas, bit = max(0, i - 18), min(len(m), ks["son"] + 4)
    bit = min(bit, bas + 48)
    f_i, (_, f_alt, f_ust) = ks["fvg"]
    isaret = {i: "S", ks["yapi_i"]: "Y", j: "M"}
    seviye_ad = "PDH (önceki gün tepesi)" if yon < 0 else "PDL (önceki gün dibi)"
    seviyeler = [(ks["seviye"], seviye_ad), (ks["yapi"], "kırılan yapı seviyesi"),
                 (ks["stop"], "stop"), (ks["hedef"], "2R hedef")]
    grafik = ciz(m, bas, bit, seviyeler, isaret, [(f_i + 2, f_alt, f_ust, "·")])
    x = m[i]
    acik = (f"{x.zaman:%Y-%m-%d %H:00} UTC mumu {seviye_ad}'yi ({ks['seviye']:,.0f}) "
            f"{'yukarı' if yon < 0 else 'aşağı'} fitille aştı ama içeride kapattı (S). "
            f"{m[j].zaman:%H:00} mumu son swing {'dibinin' if yon < 0 else 'tepesinin'} (Y, "
            f"{ks['yapi']:,.0f}) {'altında' if yon < 0 else 'üstünde'} kapattı: 1 saatlik yapı bozulması (M). "
            f"Noktalı alan bu hareketin bıraktığı FVG ({f_alt:,.0f}–{f_ust:,.0f}). "
            f"Örnek giriş M kapanışı ({m[j].c:,.0f}), stop süpürme ucu ({ks['stop']:,.0f}), "
            f"hedef 2R ({ks['hedef']:,.0f}). Sonuç: **{ks['sonuc']}** "
            f"({m[ks['son']].zaman:%Y-%m-%d %H:00}).")
    return f"### {baslik}\n\n```text\n{grafik}\n```\n\n{acik}\n"


def esit_dip_ornegi(m):
    """Eşit dipler (sellside likidite havuzu) ve sonradan süpürülmesi."""
    dipler = k.swing_dipler(m)
    for a_, b_ in zip(dipler, dipler[1:]):
        if a_ < 24 * 30 or b_ - a_ < 6 or b_ - a_ > 30:
            continue
        if abs(m[a_].l - m[b_].l) / m[a_].l > 0.0008:
            continue
        L = min(m[a_].l, m[b_].l)
        sup = next((t for t in range(b_ + 4, b_ + 30) if m[t].l < L), None)
        if sup is None or m[sup].c < L:  # fitille alıp içeride kapatan
            continue
        bas = a_ - 4
        bit = min(bas + 48, sup + 12)
        grafik = ciz(m, bas, bit, [(L, "eşit dipler = sellside likidite (SSL)")],
                     {a_: "1", b_: "2", sup: "S"})
        sonra = m[min(sup + 12, len(m) - 1)].c
        acik = (f"{m[a_].zaman:%Y-%m-%d %H:00} ve {m[b_].zaman:%d.%m %H:00} dipleri neredeyse aynı "
                f"seviyede ({m[a_].l:,.0f} / {m[b_].l:,.0f}). Bu diplerin altında stop emirleri birikir. "
                f"{m[sup].zaman:%d.%m %H:00} mumu (S) seviyenin altına fitil attı ve üstünde kapattı. "
                f"12 saat sonra fiyat {sonra:,.0f} ({100 * (sonra / m[sup].c - 1):+.2f}%).")
        return f"### Örnek 2: Eşit dipler ve sellside likidite süpürmesi\n\n```text\n{grafik}\n```\n\n{acik}\n"


def main():
    m = veri.mumlar("BTCUSDT", "2025-01", "2025-06")
    parcalar = ["# Gerçek Grafik Örnekleri (BTCUSDT, 1 saatlik, Binance vadeli)", "",
                "Kod: `kod/ornekler.py`. Örnekler kurallarla otomatik seçildi. Okuma anahtarı: "
                "`█` yükselen mum gövdesi, `▒` düşen mum gövdesi, `│` fitil, `-` yatay seviye, "
                "`·` FVG bölgesi. Alt satırdaki harfler olayları, en alttaki saatler UTC saatini gösterir.", ""]
    bas, bit, grafik, notlar = yapi_ornegi(m)
    parcalar += ["### Örnek 1: Piyasa yapısı (swing tepe ve dipleri)", "", "```text", grafik, "```", "",
                 f"{m[bas].zaman:%Y-%m-%d} → {m[bit - 1].zaman:%Y-%m-%d}. T = swing tepe, D = swing dip "
                 "(solundaki ve sağındaki 3 mumdan daha uç). Her tepe/dip bir öncekiyle kıyaslanır:", ""]
    parcalar += [f"- {n}" for n in notlar] + [""]
    parcalar.append(esit_dip_ornegi(m))
    kurulumlar = supurme_kurulumlari(m)
    hedef = next(x for x in kurulumlar if x["sonuc"] == "hedef")
    stop = next(x for x in kurulumlar if x["sonuc"] == "stop")
    parcalar.append(kurulum_ciz(m, hedef, "Örnek 3: Süpürme + saatlik bozulma + FVG, işe yarayan"))
    parcalar.append(kurulum_ciz(m, stop, "Örnek 4: Aynı kurulum, stop olan"))
    say = {s: sum(1 for x in kurulumlar if x["sonuc"] == s) for s in ("hedef", "stop", "süre doldu")}
    parcalar += ["### Bu altı ayda aynı kurulumun dökümü", "",
                 f"2025-01 → 2025-06 arasında BTC'de bu kurala uyan {len(kurulumlar)} kurulum oluştu: "
                 f"{say['hedef']} hedef, {say['stop']} stop, {say['süre doldu']} süre doldu (24 saat). "
                 "Bu sayı tek coin ve kısa dönem olduğu için sonuç çıkarmaya yetmez; yalnızca "
                 "\"her güzel görünen kurulum çalışmaz\" gerçeğini göstermek için verildi.", ""]
    SONUC.parent.mkdir(exist_ok=True)
    SONUC.write_text("\n".join(parcalar))
    print("\n".join(parcalar))


if __name__ == "__main__":
    main()
