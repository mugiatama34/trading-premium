"""PO3 kural seti v1 backtesti (Aşama 4). Yalnızca standart Python kullanır.

Kurallar: ../po3-kural-seti-v1.md, parametreler: kurallar.py
Veri: ../po3-istatistik/veri/ham (5 dk mumlar) ve veri/fonlama (fonlama oranları).

Kullanım:  python backtest.py
Çıktılar:  sonuclar/rapor.md, sonuclar/islemler.csv
"""

import csv
import io
import math
import random
import zipfile
import zlib
from bisect import bisect_left, bisect_right
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from statistics import median
from zoneinfo import ZoneInfo

import kurallar as K
from analiz_saf import coin_oku

CIKTI = K.KLASOR / "sonuclar"
SAAT_MS = 3_600_000
MUM_MS = 300_000
RASTGELE_TOHUM = 20


# ---------------------------------------------------------------- veri

def fonlama_oku(coin: str):
    """(zaman_ms listesi, oran listesi); oran ondalık (0.0001 = %0,01)."""
    satirlar = {}
    for dosya in sorted(K.FONLAMA_KLASORU.glob(f"{coin}USDT-fundingRate-*.zip")):
        with zipfile.ZipFile(dosya) as z:
            for r in csv.reader(io.StringIO(z.read(z.namelist()[0]).decode())):
                if r and r[0].isdigit():
                    # Fonlama anı saatin başına yuvarlanır (kayıt birkaç ms gecikmeli olabilir)
                    satirlar[round(int(r[0]) / SAAT_MS) * SAAT_MS] = float(r[2])
    zaman = sorted(satirlar)
    return zaman, [satirlar[t] for t in zaman]


def atr_hesapla(veri: dict, n: int = 14) -> list[float]:
    h, l, c = veri["high"], veri["low"], veri["close"]
    tr = [h[0] - l[0]] + [max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1]))
                          for i in range(1, len(h))]
    atr, toplam = [], 0.0
    for i, x in enumerate(tr):
        toplam += x - (tr[i - n] if i >= n else 0)
        atr.append(toplam / min(i + 1, n))
    return atr


def ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


def gunler(veri: dict, k: K.Kurallar):
    """Her yerel gün için Asya başlangıcından ertesi gece yarısına kadar dilim ve önceki gün özeti."""
    tz = ZoneInfo(k.saat_dilimi)
    ts = veri["ts"]
    gun = datetime.fromtimestamp(ts[0] / 1000, timezone.utc).astimezone(tz).date()
    son = datetime.fromtimestamp(ts[-1] / 1000, timezone.utc).astimezone(tz).date()
    onceki = None
    while gun <= son:
        gece = datetime(gun.year, gun.month, gun.day)
        acilis = ms(gece.replace(tzinfo=tz))
        bas = ms((gece + timedelta(hours=min(k.asya[0], 0))).replace(tzinfo=tz))
        bitis = ms((gece + timedelta(days=1)).replace(tzinfo=tz))
        i0, i1 = bisect_left(ts, bas), bisect_left(ts, bitis)
        rel = [(t - acilis) / SAAT_MS for t in ts[i0:i1]]
        gun_ici = [i for i, r in enumerate(rel) if r >= 0]
        tam = len(gun_ici) >= 0.9 * (bitis - acilis) / MUM_MS
        ozet = None
        if tam:
            ozet = {
                "yuksek": max(veri["high"][i0 + i] for i in gun_ici),
                "dusuk": min(veri["low"][i0 + i] for i in gun_ici),
                "kapanis": veri["close"][i0 + gun_ici[-1]],
            }
        yield gun, i0, i1, rel, onceki
        onceki = ozet
        gun += timedelta(days=1)


# ---------------------------------------------------------------- işlem mantığı

def pivot_tepe(H, p, n):
    return (p - n >= 0 and p + n < len(H) and H[p] > max(H[p - n:p])
            and H[p] >= max(H[p + 1:p + n + 1]))


def yonlu(veri, i0, i1, yon):
    """Kısa işlemler için fiyatlar ters çevrilir (-fiyat); böylece tek bir uzun işlem mantığı yeter."""
    h, l, c = veri["high"][i0:i1], veri["low"][i0:i1], veri["close"][i0:i1]
    if yon == 1:
        return h, l, c
    return [-x for x in l], [-x for x in h], [-x for x in c]


def ilk_supurme(L, rel, al, k):
    for i, r in enumerate(rel):
        if k.manipulasyon[0] <= r < k.manipulasyon[1] and L[i] < al:
            return i
    return None


def surdur(H, L, C, rel, bas, giris, stop, hedef, cikis):
    """Pozisyon bas mumunda doldu. Dönüş: (çıkış indeksi, çıkış fiyatı, sonuç).

    Aynı mumda stop ve hedef varsa stop sayılır (temkinli). Dolum mumunda yalnızca stop kontrol edilir.
    """
    if L[bas] <= stop:
        return bas, stop, "stop"
    for q in range(bas + 1, len(H)):
        if rel[q] >= cikis:
            return q - 1, C[q - 1], "zaman"
        if L[q] <= stop:
            return q, stop, "stop"
        if H[q] >= hedef:
            return q, hedef, "hedef"
    return len(H) - 1, C[-1], "zaman"


def plan_kur(veri, atr, i0, i1, rel, yon, k: K.Kurallar, sayac):
    """Yönlü (ters çevrilmiş olabilir) fiyatlarda süpürme → geri kapanış → MSS → FVG adımları."""
    H, L, C = yonlu(veri, i0, i1, yon)
    asya = [i for i, r in enumerate(rel) if k.asya[0] <= r < k.asya[1]]
    al, ah = min(L[i] for i in asya), max(H[i] for i in asya)
    t = ilk_supurme(L, rel, al, k)
    if t is None:
        return None
    sayac["supurme"] += 1
    j = next((j for j in range(t, min(t + k.geri_kapanis_mum, len(C))) if C[j] > al), None)
    if j is None:
        return None
    sayac["geri_kapanis"] += 1
    # MSS seviyesi: süpürmeden önce oluşmuş (ve teyit edilmiş) son kısa vadeli tepe
    seviye = next((H[p] for p in range(t - k.pivot, asya[0] - 1, -1)
                   if pivot_tepe(H, p, k.pivot) and H[p] > al), None)
    if seviye is None:
        return None
    m = None
    for q in range(j, len(C)):
        if rel[q] >= k.mss_son:
            break
        if C[q] > seviye:
            m = q
            break
    if m is None:
        return None
    sayac["mss"] += 1
    uc = min(range(t, m + 1), key=lambda i: (L[i], i))
    fvg = next((i for i in range(uc + 2, min(m + 2, len(H))) if L[i] > H[i - 2]), None)
    if fvg is None:
        return None
    sayac["fvg"] += 1
    giris = L[fvg]  # FVG'nin üst kenarı (yükseliş için); fiyat geri çekilince ilk değilen yer
    stop = L[uc] - k.stop_tampon_atr * atr[i0 + m]
    asgari = k.min_stop_yuzde / 100 * abs(giris)  # v2: asgari stop mesafesi (fiyatın yüzdesi)
    if giris - stop < asgari:
        if k.min_stop_modu == "filtre":
            return None
        if k.min_stop_modu == "genislet":
            stop = giris - asgari
    hedef = ah if k.hedef == "asya" else giris + float(k.hedef.rstrip("R")) * (giris - stop)
    if not stop < giris < hedef:
        return None
    k0 = max(fvg, m) + 1
    for q in range(k0, min(k0 + k.fvg_bekleme_mum, len(H))):
        if rel[q] >= k.cikis:
            break
        if L[q] < giris:  # yalnızca değmek yetmez, fiyat limitin altına inmeli
            sayac["dolum"] += 1
            return {"H": H, "L": L, "C": C, "dolum": q, "giris": giris, "stop": stop, "hedef": hedef}
        if H[q] >= hedef:
            return None  # hedefe dolumsuz gidildi, emir iptal
    return None


def maliyet_r(coin, yon, giris, risk, cikis_fiyat, sonuc, t_giris, t_cikis, fon):
    """Komisyon, kayma ve fonlamanın R cinsinden toplamı. Fiyatlar pozitif (gerçek) değerlerdir."""
    komisyon = K.MAKER / 100 * giris
    if sonuc == "hedef":
        komisyon += K.MAKER / 100 * cikis_fiyat
    else:
        komisyon += (K.TAKER + K.kayma(coin)) / 100 * cikis_fiyat
    zaman, oran = fon
    a, b = bisect_right(zaman, t_giris), bisect_left(zaman, t_cikis)
    fonlama = sum(oran[a:b]) * giris * yon  # pozitif oran: uzun öder, kısa alır
    return komisyon / risk, fonlama / risk


def coin_backtest(coin, veri, atr, fon, k: K.Kurallar, rastgele=False):
    islemler, sayac = [], defaultdict(int)
    for gun, i0, i1, rel, onceki in gunler(veri, k):
        if gun.weekday() >= 5 or i1 - i0 == 0:
            continue
        asya_mum = sum(1 for r in rel if k.asya[0] <= r < k.asya[1])
        if asya_mum < 0.9 * (k.asya[1] - k.asya[0]) * 12 or sum(1 for r in rel if 0 <= r < k.cikis) < 0.9 * k.cikis * 12:
            continue
        sayac["gun"] += 1
        if k.bias:
            if onceki is None:
                continue
            yonler = [1 if onceki["kapanis"] > (onceki["yuksek"] + onceki["dusuk"]) / 2 else -1]
        else:
            # Bias yok: önce süpürülen taraf işlenir
            zaman = {}
            for y in (1, -1):
                H, L, C = yonlu(veri, i0, i1, y)
                al = min(L[i] for i, r in enumerate(rel) if k.asya[0] <= r < k.asya[1])
                t = ilk_supurme(L, rel, al, k)
                if t is not None:
                    zaman[y] = t
            if len(zaman) == 2 and zaman[1] == zaman[-1]:
                yonler = []  # iki taraf aynı mumda süpürüldü, sıra bilinemez
            else:
                yonler = sorted(zaman, key=zaman.get)[:1]
        for yon in yonler:
            plan = plan_kur(veri, atr, i0, i1, rel, yon, k, sayac)
            if plan is None:
                continue
            q = plan["dolum"]
            cik, fiyat, sonuc = surdur(plan["H"], plan["L"], plan["C"], rel, q,
                                       plan["giris"], plan["stop"], plan["hedef"], k.cikis)
            risk = plan["giris"] - plan["stop"]
            giris = plan["giris"] * yon
            t_giris, t_cikis = veri["ts"][i0 + q], veri["ts"][i0 + cik] + MUM_MS
            kom, fonl = maliyet_r(coin, yon, giris, risk, fiyat * yon, sonuc, t_giris, t_cikis, fon)
            brut = (fiyat - plan["giris"]) / risk
            islem = {
                "coin": coin, "varyant": k.ad, "gun": gun, "yon": "uzun" if yon == 1 else "kisa",
                "giris_zamani": t_giris, "cikis_zamani": t_cikis, "giris": giris,
                "stop": plan["stop"] * yon, "hedef": plan["hedef"] * yon, "sonuc": sonuc,
                "hedef_turu": k.hedef, "hedef_r": (plan["hedef"] - plan["giris"]) / risk, "stop_yuzde": 100 * risk / giris,
                "brut_r": brut, "komisyon_kayma_r": kom, "fonlama_r": fonl, "net_r": brut - kom - fonl,
            }
            if rastgele:
                islem["rastgele_net_r"] = rastgele_kiyas(coin, veri, i0, i1, rel, q, giris, risk,
                                                         islem["hedef_r"], k, fon)
            islemler.append(islem)
    return islemler, sayac


def rastgele_kiyas(coin, veri, i0, i1, rel, q, giris, risk, hedef_r, k, fon):
    """Aynı anda, aynı fiyattan, aynı stop ve hedef mesafesiyle rastgele yönlü giriş (tohum başına net R)."""
    sonuclar = []
    for s in range(RASTGELE_TOHUM):
        yon = 1 if random.Random(zlib.crc32(f"{coin}{i0}{k.ad}{s}".encode())).random() < 0.5 else -1
        H, L, C = yonlu(veri, i0, i1, yon)
        g = giris * yon
        cik, fiyat, sonuc = surdur(H, L, C, rel, q, g, g - risk, g + hedef_r * risk, k.cikis)
        kom, fonl = maliyet_r(coin, yon, giris, risk, fiyat * yon, sonuc, veri["ts"][i0 + q],
                              veri["ts"][i0 + cik] + MUM_MS, fon)
        sonuclar.append((fiyat - g) / risk - kom - fonl)
    return sonuclar


# ---------------------------------------------------------------- ölçüler

def ozet(islemler):
    if not islemler:
        return None
    net = [x["net_r"] for x in islemler]
    brut = [x["brut_r"] for x in islemler]
    kaz = [r for r in net if r > 0]
    kay = [r for r in net if r <= 0]
    seri = en_uzun = 0
    for x in sorted(islemler, key=lambda x: x["giris_zamani"]):
        seri = seri + 1 if x["net_r"] <= 0 else 0
        en_uzun = max(en_uzun, seri)
    ort = sum(net) / len(net)
    se = math.sqrt(sum((r - ort) ** 2 for r in net) / max(len(net) - 1, 1) / len(net))
    brut_kar = sum(r for r in brut if r > 0)
    maliyet = sum(brut) - sum(net)
    return {
        "n": len(net), "kazanma": 100 * len(kaz) / len(net),
        "ort_kazanc": sum(kaz) / len(kaz) if kaz else 0.0,
        "ort_kayip": sum(kay) / len(kay) if kay else 0.0,
        "brut_r": sum(brut) / len(brut), "net_r": ort, "net_ga": (ort - 1.96 * se, ort + 1.96 * se),
        "pf": sum(kaz) / -sum(kay) if kay and sum(kay) < 0 else math.inf,
        "kayip_serisi": en_uzun,
        "maliyet_orani": 100 * maliyet / brut_kar if brut_kar else math.nan,
        "fonlama_r": sum(x["fonlama_r"] for x in islemler) / len(islemler),
        "stop_medyan": median(x["stop_yuzde"] for x in islemler),
    }


def portfoy(islemler, risk_yuzde, bas=None, bit=None):
    """%risk ile bileşik sermaye; aynı yönde toplam açık risk sınırı uygulanır. Gerçekleşen kâr/zarar üzerinden."""
    sermaye, tepe, dd = K.SERMAYE, K.SERMAYE, 0.0
    acik, alinan, atlanan = [], 0, 0

    def kapat(sinir):
        nonlocal sermaye, tepe, dd
        acik.sort(key=lambda a: a[0])
        while acik and acik[0][0] <= sinir:
            _, _, tutar, r = acik.pop(0)
            sermaye += tutar * r
            tepe = max(tepe, sermaye)
            dd = max(dd, 1 - sermaye / tepe)

    for x in sorted(islemler, key=lambda x: x["giris_zamani"]):
        kapat(x["giris_zamani"])
        ayni = sum(1 for a in acik if a[1] == x["yon"])
        if (ayni + 1) * risk_yuzde > K.TOPLAM_RISK_SINIRI + 1e-9:
            atlanan += 1
            continue
        acik.append((x["cikis_zamani"], x["yon"], sermaye * risk_yuzde / 100, x["net_r"]))
        alinan += 1
    kapat(math.inf)
    if bas is None:
        bas = min(x["giris_zamani"] for x in islemler)
        bit = max(x["cikis_zamani"] for x in islemler)
    yil = (bit - bas) / (365.25 * 24 * SAAT_MS)
    yillik = 100 * ((sermaye / K.SERMAYE) ** (1 / yil) - 1) if sermaye > 0 and yil > 0 else -100.0
    return {"son": sermaye, "dd": 100 * dd, "yillik": yillik, "alinan": alinan, "atlanan": atlanan}


def monte_carlo(islemler, risk_yuzde=1.0, tekrar=1000):
    """İşlem sırası karıştırılarak %95'lik en kötü maksimum düşüş (sıralı, örtüşmesiz bileşik)."""
    net = [x["net_r"] for x in islemler]
    rng = random.Random(42)
    dds = []
    for _ in range(tekrar):
        rng.shuffle(net)
        s, tepe, dd = 1.0, 1.0, 0.0
        for r in net:
            s *= 1 + risk_yuzde / 100 * r
            tepe = max(tepe, s)
            dd = max(dd, 1 - s / tepe)
        dds.append(dd)
    dds.sort()
    return 100 * dds[len(dds) // 2], 100 * dds[int(0.95 * len(dds))]


# ---------------------------------------------------------------- rapor

def bicim(o):
    if o is None:
        return "| – | – | – | – | – | – | – | – |"
    return (f"| {o['n']} | %{o['kazanma']:.1f} | {o['brut_r']:+.3f} | {o['net_r']:+.3f} | "
            f"{o['net_ga'][0]:+.3f} – {o['net_ga'][1]:+.3f} | {o['pf']:.2f} | %{o['stop_medyan']:.2f} | "
            f"{o['kayip_serisi']} |")


BASLIK = ("| Grup | İşlem | Kazanma | Brüt R | Net R | Net R %95 GA | PF | Medyan stop | En uzun kayıp serisi |\n"
          "|---|---|---|---|---|---|---|---|---|")


def esik_tablosu(o, p, rastgele_p):
    def d(kosul):
        return "Geçti" if kosul else "Geçmedi"
    return "\n".join([
        "| Ölçüt | Eşik | Sonuç | Durum |", "|---|---|---|---|",
        f"| İşlem sayısı | ≥ 100 | {o['n']} | {d(o['n'] >= 100)} |",
        f"| Net beklenti | ≥ +0,15R | {o['net_r']:+.3f}R | {d(o['net_r'] >= 0.15)} |",
        f"| Profit factor | ≥ 1,3 | {o['pf']:.2f} | {d(o['pf'] >= 1.3)} |",
        f"| Maks. düşüş (%1 risk) | ≤ %20 | %{p['dd']:.1f} | {d(p['dd'] <= 20)} |",
        f"| Rastgele kıyastan iyi | p < 0,05 | p = {rastgele_p:.3f} | {d(rastgele_p < 0.05)} |",
    ])


def rastgele_ozet(islemler):
    """Modelin net R'si, aynı işlemin rastgele yönlü kopyalarının ortalamasıyla eşleştirilerek kıyaslanır.

    p: "model rastgeleden iyi değil" varsayımı için tek yönlü p değeri (eşleştirilmiş farkların z testi).
    """
    tohum_ort = [sum(x["rastgele_net_r"][s] for x in islemler) / len(islemler) for s in range(RASTGELE_TOHUM)]
    fark = [x["net_r"] - sum(x["rastgele_net_r"]) / RASTGELE_TOHUM for x in islemler]
    n = len(fark)
    ort = sum(fark) / n
    se = math.sqrt(sum((d - ort) ** 2 for d in fark) / max(n - 1, 1) / n)
    p = 0.5 * math.erfc(ort / se / math.sqrt(2)) if se > 0 else 0.5
    return sum(tohum_ort) / len(tohum_ort), min(tohum_ort), max(tohum_ort), p


def yil_tablosu(islemler):
    s = ["| Yıl | İşlem | Kazanma | Net R | PF |", "|---|---|---|---|---|"]
    yillar = defaultdict(list)
    for x in islemler:
        yillar[x["gun"].year].append(x)
    for y in sorted(yillar):
        o = ozet(yillar[y])
        s.append(f"| {y} | {o['n']} | %{o['kazanma']:.1f} | {o['net_r']:+.3f} | {o['pf']:.2f} |")
    return "\n".join(s)


def kaldirac_satiri(islemler, risk):
    lev = sorted(risk / x["stop_yuzde"] for x in islemler)
    return (f"medyan {median(lev):.1f}x, %90'lık {lev[int(0.9 * len(lev))]:.1f}x, "
            f"en yüksek {lev[-1]:.1f}x")


def veri_yukle():
    veriler = {}
    for coin in K.COINLER:
        v = coin_oku(coin)
        if v["ts"]:
            veriler[coin] = (v, atr_hesapla(v), fonlama_oku(coin))
    return veriler


def main():
    veriler = veri_yukle()
    bas_ts = min(v["ts"][0] for v, _, _ in veriler.values())
    bit_ts = max(v["ts"][-1] for v, _, _ in veriler.values())
    oos = ms(datetime.fromisoformat(K.ORNEKLEM_DISI_BASLANGIC).replace(tzinfo=timezone.utc))

    def calistir(k, rastgele=False):
        tum, sayac = [], defaultdict(int)
        for coin, (v, atr, fon) in veriler.items():
            isl, say = coin_backtest(coin, v, atr, fon, k, rastgele)
            tum += isl
            for a, b in say.items():
                sayac[a] += b
        return tum, sayac

    s = ["# PO3 Kural Seti v1 Backtesti: Sonuçlar\n",
         "Kurallar: [../../po3-kural-seti-v1.md](../../po3-kural-seti-v1.md). Kod: `backtest.py`, parametreler: `kurallar.py`.\n",
         f"Veri: Binance USDT-M vadeli 5 dk mumlar ve geçmiş fonlama oranları, {len(veriler)} coin, "
         f"{datetime.fromtimestamp(bas_ts / 1000, timezone.utc):%Y-%m-%d} → "
         f"{datetime.fromtimestamp(bit_ts / 1000, timezone.utc):%Y-%m-%d}. Örneklem dışı (test) dönemi: "
         f"{K.ORNEKLEM_DISI_BASLANGIC} sonrası.\n",
         f"Maliyetler: giriş ve hedef limit emir (maker %{K.MAKER}), stop ve zaman çıkışı piyasa emri "
         f"(taker %{K.TAKER} + coin bazında kayma %0,01–0,05), gerçek geçmiş fonlama oranları. "
         "Tüm R değerleri **net R** sütunlarında maliyetler düşülmüş haldedir.\n"]
    tum_islemler = []
    for ad, k in K.TEMEL.items():
        for hedef in ("asya", "2R"):
            kk = K.degistir(k, hedef=hedef)
            isl, sayac = calistir(kk, rastgele=True)
            tum_islemler += isl
            baslik = "00:00 UTC açılışı" if ad == "utc" else "New York gece yarısı açılışı"
            s.append(f"\n## {baslik}, hedef: {'Asya aralığının karşı tarafı' if hedef == 'asya' else 'sabit 2R'}\n")
            s.append(f"Huni: {sayac['gun']} hafta içi gün → {sayac['supurme']} bias yönünde süpürme → "
                     f"{sayac['geri_kapanis']} geri kapanış → {sayac['mss']} MSS → {sayac['fvg']} FVG → "
                     f"{sayac['dolum']} dolan limit emir.\n")
            if not isl:
                s.append("İşlem yok.\n")
                continue
            ic = [x for x in isl if x["giris_zamani"] < oos]
            dis = [x for x in isl if x["giris_zamani"] >= oos]
            s.append(BASLIK)
            for etiket, grup in (("Tümü", isl), ("Örneklem içi", ic), ("Örneklem dışı", dis),
                                 ("Uzun", [x for x in isl if x["yon"] == "uzun"]),
                                 ("Kısa", [x for x in isl if x["yon"] == "kisa"])):
                s.append(f"| {etiket} " + bicim(ozet(grup)))
            o_dis = ozet(dis)
            if o_dis:
                p1 = portfoy(dis, 1.0, oos, bit_ts)
                r_ort, r_min, r_max, r_p = rastgele_ozet(dis)
                s.append("\n**Örneklem dışı, devam eşikleri:**\n")
                s.append(esik_tablosu(o_dis, p1, r_p))
                s.append(f"\nRastgele yönlü kıyas (aynı giriş anı, stop ve hedef, {RASTGELE_TOHUM} tohum): "
                         f"ortalama net R {r_ort:+.3f} (tohumlar {r_min:+.3f} … {r_max:+.3f}); model {o_dis['net_r']:+.3f}.\n")
            o = ozet(isl)
            dagilim = ", ".join(f"{a} %{100 * sum(1 for x in isl if x['sonuc'] == a) / len(isl):.1f}"
                                for a in ("hedef", "stop", "zaman"))
            s.append(f"\nSonuç dağılımı: {dagilim}. Ortalama kazanç {o['ort_kazanc']:+.2f}R, ortalama kayıp {o['ort_kayip']:+.2f}R. "
                     f"Maliyetlerin brüt kâra oranı %{o['maliyet_orani']:.0f}; fonlamanın payı işlem başına {o['fonlama_r']:+.4f}R.\n")
            s.append("\n**Portföy (tüm dönem, 10.000 $ başlangıç, aynı yönde en fazla %3 açık risk):**\n")
            s.append("| Risk/işlem | Alınan işlem | Sınır yüzünden atlanan | Son sermaye | Yıllık getiri | Maks. düşüş |\n|---|---|---|---|---|---|")
            for r in (1.0, 2.0):
                p = portfoy(isl, r, bas_ts, bit_ts)
                s.append(f"| %{r:.0f} | {p['alinan']} | {p['atlanan']} | {p['son']:,.0f} $ | %{p['yillik']:.1f} | %{p['dd']:.1f} |")
            mc50, mc95 = monte_carlo(isl)
            s.append(f"\nMonte Carlo (işlem sırası 1000 kez karıştırıldı, %1 risk): medyan maks. düşüş %{mc50:.1f}, "
                     f"%95 kötü durumda %{mc95:.1f}.\n")
            s.append(f"\nGereken kaldıraç (pozisyon / sermaye): %1 riskte {kaldirac_satiri(isl, 1)}; "
                     f"%2 riskte {kaldirac_satiri(isl, 2)}.\n")
            s.append("\n**Yıllara göre:**\n")
            s.append(yil_tablosu(isl))
            s.append("\n**Coinlere göre:**\n")
            s.append(BASLIK)
            for c in sorted({x["coin"] for x in isl}):
                s.append(f"| {c} " + bicim(ozet([x for x in isl if x["coin"] == c])))

    s.append("\n## Sağlamlık: parametreler tek tek değiştirildiğinde (tüm dönem, net R)\n")
    s.append("| Değişiklik | UTC işlem | UTC net R | UTC PF | NY işlem | NY net R | NY PF |\n|---|---|---|---|---|---|---|")
    degisiklikler = [
        ("Temel (hedef Asya)", {}),
        ("Asya bitişi 1 saat erken", {"asya": "-1"}),
        ("Asya bitişi 1 saat geç", {"asya": "+1"}),
        ("Geri kapanış N = 2", {"geri_kapanis_mum": 2}),
        ("Geri kapanış N = 5", {"geri_kapanis_mum": 5}),
        ("FVG bekleme X = 6", {"fvg_bekleme_mum": 6}),
        ("FVG bekleme X = 24", {"fvg_bekleme_mum": 24}),
        ("Stop tamponu 0,3 ATR", {"stop_tampon_atr": 0.3}),
        ("Pivot 3 mum", {"pivot": 3}),
        ("Bias filtresi yok", {"bias": False}),
    ]
    for etiket, deg in degisiklikler:
        satir = f"| {etiket} "
        for k in K.TEMEL.values():
            d = dict(deg)
            if d.get("asya") in ("-1", "+1"):
                fark = int(d.pop("asya"))
                d["asya"] = (k.asya[0], k.asya[1] + fark)
                d["manipulasyon"] = (k.manipulasyon[0] + fark, k.manipulasyon[1])
            isl, _ = calistir(K.degistir(k, **d))
            o = ozet(isl)
            satir += f"| {o['n']} | {o['net_r']:+.3f} | {o['pf']:.2f} " if o else "| 0 | – | – "
        s.append(satir + "|")

    CIKTI.mkdir(parents=True, exist_ok=True)
    (CIKTI / "rapor.md").write_text("\n".join(s) + "\n", encoding="utf-8")
    alanlar = [a for a in tum_islemler[0] if a != "rastgele_net_r"]
    with open(CIKTI / "islemler.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=alanlar, extrasaction="ignore")
        w.writeheader()
        for x in tum_islemler:
            satir = dict(x)
            satir["giris_zamani"] = datetime.fromtimestamp(x["giris_zamani"] / 1000, timezone.utc).isoformat()
            satir["cikis_zamani"] = datetime.fromtimestamp(x["cikis_zamani"] / 1000, timezone.utc).isoformat()
            w.writerow(satir)
    print(f"Rapor: {CIKTI / 'rapor.md'}")


if __name__ == "__main__":
    main()
