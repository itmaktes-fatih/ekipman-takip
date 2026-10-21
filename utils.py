# ==========================================
# PERİYODİK KONTROL TAKİP
# utils.py
# ==========================================

from datetime import date, datetime, timedelta

from config import DATE_FORMAT, SAFE_DAYS, WARNING_DAYS


# ==========================================================
# TARİH
# ==========================================================

def tarih_dogrula(tarih: str) -> bool:

    try:
        datetime.strptime(tarih, DATE_FORMAT)
        return True

    except (ValueError, TypeError):
        return False


def sonraki_kontrol_tarihi(son_kontrol: str, periyot: int) -> str:

    if not tarih_dogrula(son_kontrol):
        return ""

    tarih = datetime.strptime(son_kontrol, DATE_FORMAT)
    sonraki = tarih + timedelta(days=int(periyot))

    return sonraki.strftime(DATE_FORMAT)


def kalan_gun(sonraki_kontrol: str) -> int:

    if not tarih_dogrula(sonraki_kontrol):
        return 0

    hedef = datetime.strptime(sonraki_kontrol, DATE_FORMAT)
    fark = hedef.date() - datetime.now().date()

    return fark.days


def kalan_gun_yazisi(gun: int) -> str:

    if gun < 0:
        return f"{abs(gun)} gün gecikti"

    if gun == 0:
        return "Bugün"

    return f"{gun} gün kaldı"


# ==========================================================
# DURUM
# ==========================================================

def durum_belirle(gun: int):
    """
    Döndürür: (yazı, ikon, renk_anahtarı)
    renk_anahtarı: "success" | "warning" | "error"
    """

    if gun < 0:
        return ("Süresi Geçmiş", "alert-circle", "error")

    if gun <= WARNING_DAYS:
        return ("Yaklaşıyor", "clock-outline", "warning")

    if gun <= SAFE_DAYS:
        return ("Yaklaşıyor", "clock-outline", "warning")

    return ("Geçerli", "check-circle", "success")


# ==========================================================
# EKİPMAN OLUŞTURMA
# ==========================================================

def ekipman_olustur(
    ad: str,
    ekipman_id: str,
    tarih: str,
    periyot: int,
    sorumlu_id: str,
) -> dict:

    return {
        "ekipman_adi": ad,
        "ekipman_id": ekipman_id,
        "son_kontrol": tarih,
        "periyot": periyot,
        "sorumlu_id": sorumlu_id,
        "aktif": True,
    }


# ==========================================================
# ETİKET (ör. "/10-11-12/20..26" = 3 aylık kontrol etiketi)
# ==========================================================

def _ay_ekle(d: date, n: int) -> date:
    """Ayın 1'i olan bir tarihe n ay ekler."""
    toplam = d.year * 12 + (d.month - 1) + n
    return date(toplam // 12, toplam % 12 + 1, 1)


def etiket_tarihi_hesapla(aylar, yil):
    """
    Etiketteki ay aralığı ve yıldan (başlangıç, periyot) hesaplar.

    Kural: Etiket, yazılı ayların ilkinin 1'inde başlar ve ay sayısı kadar
    geçerlidir. Örn. aylar=[10, 11, 12], yil=2026
        -> ("01.10.2026", 92)   # sonraki kontrol: 01.01.2027

    Okunamayan/geçersiz veride (None, None) döner.
    """
    try:
        aylar = sorted({int(a) for a in (aylar or []) if 1 <= int(a) <= 12})
        yil = int(yil)
    except (ValueError, TypeError):
        return None, None

    if not aylar:
        return None, None

    if yil < 100:
        yil += 2000

    if not 2000 <= yil <= 2100:
        return None, None

    # Aralığın başlangıç ayı: kendinden önceki ay listede olmayan ay
    # (12-1-2 gibi yıl sonunu aşan aralıkları da doğru bulur).
    ilk = next(
        (m for m in aylar if ((m - 2) % 12) + 1 not in aylar),
        aylar[0],
    )

    baslangic = date(yil, ilk, 1)
    bitis = _ay_ekle(baslangic, len(aylar))

    return baslangic.strftime(DATE_FORMAT), (bitis - baslangic).days
