"""Eğitimdeki kavramların mekanik (kurala bağlanmış) tanımları.

Grafikte göz kararı yapılan işaretlemeleri koda dökmek, kavramı test edilebilir hale getirmenin
ilk adımıdır. Buradaki tanımlar tek bir makul seçimdir; topluluktaki tek doğru tanım değildir.
"""

from collections import defaultdict


def swing_tepeler(m, n=3):
    """Solunda ve sağında n mumdan yüksek tepe yapan mumların indeksleri.

    Dikkat: i'deki tepe ancak i+n mumunun kapanışında "kesinleşir" (geleceği görmeme kuralı).
    """
    return [i for i in range(n, len(m) - n)
            if all(m[i].h > m[j].h for j in range(i - n, i))
            and all(m[i].h >= m[j].h for j in range(i + 1, i + n + 1))]


def swing_dipler(m, n=3):
    return [i for i in range(n, len(m) - n)
            if all(m[i].l < m[j].l for j in range(i - n, i))
            and all(m[i].l <= m[j].l for j in range(i + 1, i + n + 1))]


def fvg_listesi(m, min_oran=0.0):
    """Üç mumlu boşluklar (Fair Value Gap). Dönen öğe: (orta_mum, yon, alt, ust).

    Yükseliş FVG: 1. mumun tepesi < 3. mumun dibi. Düşüş FVG: 1. mumun dibi > 3. mumun tepesi.
    """
    sonuc = []
    for i in range(1, len(m) - 1):
        a, c = m[i - 1], m[i + 1]
        if c.l > a.h and (c.l - a.h) / m[i].c >= min_oran:
            sonuc.append((i, +1, a.h, c.l))
        elif c.h < a.l and (a.l - c.h) / m[i].c >= min_oran:
            sonuc.append((i, -1, c.h, a.l))
    return sonuc


def gunluk_seviyeler(m):
    """Her mum için bir önceki UTC gününün tepesi ve dibi (PDH, PDL). Yoksa None."""
    gunler = defaultdict(lambda: [float("-inf"), float("inf")])
    gun_sirasi = []
    for x in m:
        g = x.t // 86_400_000
        if g not in gunler:
            gun_sirasi.append(g)
        gunler[g][0] = max(gunler[g][0], x.h)
        gunler[g][1] = min(gunler[g][1], x.l)
    onceki = {g: gunler[gun_sirasi[k - 1]] for k, g in enumerate(gun_sirasi) if k > 0
              and gun_sirasi[k - 1] == g - 1}
    return [tuple(onceki[x.t // 86_400_000]) if x.t // 86_400_000 in onceki else None for x in m]


def atr(m, n=24):
    """Basit ortalama gerçek aralık (Average True Range); oynaklık ölçüsü."""
    tr = [m[0].h - m[0].l] + [max(m[i].h, m[i - 1].c) - min(m[i].l, m[i - 1].c)
                              for i in range(1, len(m))]
    sonuc, toplam = [], 0.0
    for i, d in enumerate(tr):
        toplam += d
        if i >= n:
            toplam -= tr[i - n]
        sonuc.append(toplam / min(i + 1, n))
    return sonuc
