import sys
import traceback
from datetime import datetime
import requests

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window

from config import APP_NAME, FirebaseConfig

from screens.dashboard import DashboardScreen
from screens.ekipman_listesi import EkipmanListesiScreen
from screens.ekipman_formu import EkipmanFormuScreen
from screens.sorumlular import SorumlularScreen


def send_crash_to_firebase(error_trace):
    """Çökme hatasını Firebase veritabanına timestamp ile gönderir."""
    try:
        url = f"{FirebaseConfig.DATABASE_URL}/crash_logs.json"
        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "error": error_trace,
            "platform": "Android"
        }
        requests.post(url, json=data, timeout=5)
    except Exception as e:
        print(f"Firebase loglama hatasi: {e}")


class AppManager(ScreenManager):
    pass


class PeriyodikKontrolApp(MDApp):

    def build(self):
        self.title = APP_NAME

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        Window.minimum_width = 420
        Window.minimum_height = 760

        sm = AppManager(
            transition=FadeTransition(duration=0.20)
        )

        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(EkipmanListesiScreen(name="ekipman_listesi"))
        sm.add_widget(EkipmanFormuScreen(name="ekipman_formu"))
        sm.add_widget(SorumlularScreen(name="sorumlular"))

        return sm


if __name__ == "__main__":
    try:
        PeriyodikKontrolApp().run()
    except Exception:
        error_msg = traceback.format_exc()
        send_crash_to_firebase(error_msg)
        sys.exit(1)
