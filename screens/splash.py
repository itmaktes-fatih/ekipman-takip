# ==========================================
# PERİYODİK KONTROL TAKİP
# screens/splash.py
# ==========================================

from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen

Builder.load_file("kv/splash.kv")

SPLASH_SURESI = 1.6  # saniye


class SplashScreen(MDScreen):

    def on_enter(self):
        Clock.schedule_once(self.dashboard_a_gec, SPLASH_SURESI)

    def dashboard_a_gec(self, *args):
        self.manager.current = "dashboard"
