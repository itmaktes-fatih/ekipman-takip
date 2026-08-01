# ==========================================
# PERİYODİK KONTROL TAKİP
# utils.py
# ==========================================

from datetime import datetime, timedelta
from config import DATE_FORMAT, SAFE_DAYS, WARNING_DAYS


# --------------------------------------------------
# TARİH İŞLEMLERİ
# --------------------------------------------------

def tarih_dogrula(tarih: str) -> bool:
    """
    Girilen tarihin doğru formatta olup olmadığını kontrol eder.
    Format : GG.AA.YYYY
    """

    try:
        datetime.strptime(tarih, DATE_FORMAT)
        return True
    except:
        return False


def str_to_date(tarih: str):
    """
    String tarihi datetime nesnesine çevirir.
    """

    return datetime.strptime(tarih, DATE_FORMAT)


def date_to_str(tarih: datetime):
    """
    Datetime nesnesini string'e çevirir.
    """

    return tarih.strftime(DATE_FORMAT)


# --------------------------------------------------
# KONTROL TARİHLERİ
# --------------------------------------------------

def sonraki_kontrol_tarihi(son_kontrol: str, periyot: int) -> str:
    """
    Son kontrol tarihine göre
    bir sonraki kontrol tarihini hesaplar.
    """

    tarih = str_to_date(son_kontrol)

    sonraki = tarih + timedelta(days=int(periyot))

    return date_to_str(sonraki)


def kalan_gun(sonraki_kontrol: str) -> int:
    """
    Kontrole kaç gün kaldığını hesaplar.
    """

    bugun = datetime.today()

    tarih = str_to_date(sonraki_kontrol)

    return (tarih.date() - bugun.date()).days


# --------------------------------------------------
# DURUM
# --------------------------------------------------

def durum_belirle(kalan: int):
    """
    Durumu döndürür.

    return

    durum

    ikon

    renk
    """

    if kalan < 0:

        return (
            "Süresi Geçmiş",
            "🔴",
            "danger"
        )

    elif kalan <= WARNING_DAYS:

        return (
            "Yaklaşıyor",
            "🟡",
            "warning"
        )

    else:

        return (
            "Geçerli",
            "🟢",
            "success"
        )


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

def dashboard_istatistik(veriler: dict):

    """
    Dashboard sayılarını hesaplar.
    """

    toplam = 0
    guvenli = 0
    yaklasan = 0
    gecmis = 0

    yaklasan_liste = []

    if not veriler:
        return {

            "toplam": 0,
            "guvenli": 0,
            "yaklasan": 0,
            "gecmis": 0,
            "yaklasan_liste": []

        }

    for key, veri in veriler.items():

        try:

            toplam += 1

            sonraki = veri["sonraki_kontrol"]

            kalan = kalan_gun(sonraki)

            durum, ikon, renk = durum_belirle(kalan)

            if renk == "success":

                guvenli += 1

            elif renk == "warning":

                yaklasan += 1

                yaklasan_liste.append({

                    "ekipman": veri["ekipman_adi"],
                    "id": veri["ekipman_id"],
                    "kalan": kalan

                })

            else:

                gecmis += 1

                yaklasan_liste.append({

                    "ekipman": veri["ekipman_adi"],
                    "id": veri["ekipman_id"],
                    "kalan": kalan

                })

        except Exception:

            continue

    yaklasan_liste = sorted(
        yaklasan_liste,
        key=lambda x: x["kalan"]
    )

    return {

        "toplam": toplam,

        "guvenli": guvenli,

        "yaklasan": yaklasan,

        "gecmis": gecmis,

        "yaklasan_liste": yaklasan_liste

    }


# --------------------------------------------------
# EKİPMAN KAYDI
# --------------------------------------------------

def ekipman_olustur(
        ekipman_adi,
        ekipman_id,
        son_kontrol,
        periyot,
        sorumlu):

    """
    Firebase'e gönderilecek sözlüğü oluşturur.
    """

    return {

        "ekipman_adi": ekipman_adi.strip(),

        "ekipman_id": ekipman_id.strip(),

        "son_kontrol": son_kontrol,

        "periyot": int(periyot),

        "sonraki_kontrol":
            sonraki_kontrol_tarihi(
                son_kontrol,
                periyot
            ),

        "sorumlu": sorumlu.strip()

    }
