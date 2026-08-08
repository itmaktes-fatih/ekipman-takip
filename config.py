# ==========================================
# PERİYODİK KONTROL TAKİP
# config.py
# ==========================================

from kivy.utils import get_color_from_hex

# --------------------------------------------------
# UYGULAMA
# --------------------------------------------------

APP_NAME = "Periyodik Kontrol Takip"
APP_VERSION = "2.0.0"

# --------------------------------------------------
# FIREBASE
# --------------------------------------------------
# Realtime Database REST API kullanılıyor (mobil/Android uyumlu).
# firebase_admin SDK Android'de ÇALIŞMAZ ve servis hesabı anahtarı
# telefona gömülemeyeceği için kullanılmamalıdır.

FIREBASE_URL = "https://kacis-seti-takip-default-rtdb.europe-west1.firebasedatabase.app/"

# Realtime Database kurallarınız "auth != null" gerektiriyorsa buraya
# bir Database Secret / ID token yazabilirsiniz. Test modundaysa boş bırakın.
FIREBASE_AUTH_TOKEN = ""

# Firebase Node'ları
NODE_EKIPMANLAR = "ekipmanlar"
NODE_SORUMLULAR = "sorumlular"

# --------------------------------------------------
# TEMA
# --------------------------------------------------

PRIMARY_COLOR = "#E67E22"      # Turuncu
SECONDARY_COLOR = "#34495E"    # Lacivert
BACKGROUND_COLOR = "#1E1E1E"   # Koyu Gri
CARD_COLOR = "#2C3E50"
TEXT_COLOR = "#FFFFFF"

SUCCESS_COLOR = "#2ECC71"
WARNING_COLOR = "#F1C40F"
DANGER_COLOR = "#E74C3C"

PRIMARY = get_color_from_hex(PRIMARY_COLOR)
SECONDARY = get_color_from_hex(SECONDARY_COLOR)
BACKGROUND = get_color_from_hex(BACKGROUND_COLOR)
CARD = get_color_from_hex(CARD_COLOR)
TEXT = get_color_from_hex(TEXT_COLOR)

SUCCESS = get_color_from_hex(SUCCESS_COLOR)
WARNING = get_color_from_hex(WARNING_COLOR)
DANGER = get_color_from_hex(DANGER_COLOR)

# --------------------------------------------------
# KONTROL DURUMLARI
# --------------------------------------------------

SAFE_DAYS = 30
WARNING_DAYS = 15

# --------------------------------------------------
# TARİH
# --------------------------------------------------

DATE_FORMAT = "%d.%m.%Y"

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

MAX_WARNING_LIST = 10

# --------------------------------------------------
# FONT
# --------------------------------------------------

TITLE_FONT = "22sp"
SUBTITLE_FONT = "18sp"
NORMAL_FONT = "15sp"
SMALL_FONT = "13sp"

# --------------------------------------------------
# BUTON
# --------------------------------------------------

BUTTON_HEIGHT = 55
CARD_RADIUS = 15

# --------------------------------------------------
# LOG
# --------------------------------------------------

DEBUG = True
