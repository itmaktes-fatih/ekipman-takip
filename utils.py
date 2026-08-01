# ==========================================
# PERİYODİK KONTROL TAKİP
# utils.py
# ==========================================

from datetime import datetime, timedelta


DATE_FORMAT = "%d.%m.%Y"


# ==========================================================
# TARİH
# ==========================================================

def bugun():
    """Bugünün tarihini datetime olarak döndürür."""
    return datetime.today()


def bugun_str():
    """Bugünün tarihini string olarak döndürür."""
    return bugun().strftime(DATE_FORMAT)


def tarih_dogrula(tarih: str) -> bool:
    """Girilen tarihin formatını kontrol eder."""

    try:
        datetime.strptime(tarih, DATE_FORMAT)
        return True

    except ValueError:
        return False


def str_to_date(tarih: str):

    return datetime.strptime(
        tarih,
        DATE_FORMAT
    )


def date_to_str(tarih: datetime):

    return tarih.strftime(
        DATE_FORMAT
    )


# ==========================================================
# KONTROL TARİHLERİ
# ==========================================================

def sonraki_kontrol_tarihi(
        son_kontrol: str,
        periyot: int
):

    tarih = str_to_date(
        son_kontrol
    )

    sonraki = tarih + timedelta(
        days=int(periyot)
    )

    return date_to_str(
        sonraki
    )


def kalan_gun(
        sonraki_kontrol: str
):

    tarih = str_to_date(
        sonraki_kontrol
    )

    fark = tarih - bugun()

    return fark.days


# ==========================================================
# DURUM
# ==========================================================

def durum_belirle(kalan: int):

    if kalan < 0:

        return (
            "Süresi Geçmiş",
            "alert-circle",
            "error"
        )

    elif kalan <= 30:

        return (
            "Yaklaşan Kontrol",
            "clock-alert",
            "warning"
        )

    else:

        return (
            "Geçerli",
            "check-circle",
            "success"
        )


# ==========================================================
# FORMATLAMA
# ==========================================================

def kalan_gun_yazisi(kalan: int):

    if kalan < 0:

        return f"{abs(kalan)} gün geçti"

    elif kalan == 0:

        return "Bugün"

    elif kalan == 1:

        return "Yarın"

    return f"{kalan} gün kaldı"


# ==========================================================
# DASHBOARD
# ==========================================================

def dashboard_istatistik(ekipmanlar):

    sonuc = {

        "toplam": len(ekipmanlar),

        "guvenli": 0,

        "yaklasan": 0,

        "gecmis": 0

    }

    for e in ekipmanlar:

        if e.durum_rengi == "success":

            sonuc["guvenli"] += 1

        elif e.durum_rengi == "warning":

            sonuc["yaklasan"] += 1

        else:

            sonuc["gecmis"] += 1

    return sonuc
