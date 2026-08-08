# ==========================================
# PERİYODİK KONTROL TAKİP
# utils.py
# ==========================================

from datetime import datetime, timedelta

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
