# ==========================================
# PERİYODİK KONTROL TAKİP
# main.py
# ==========================================

from kivymd.app import MDApp
from kivy.core.window import Window

from config import (
    APP_NAME,
    PRIMARY_COLOR,
    BACKGROUND_COLOR
)

from screens.dashboard import DashboardScreen


class PeriyodikKontrolApp(MDApp):

    def build(self):

        # Uygulama Başlığı
        self.title = APP_NAME

        # Tema
        self.theme_cls.theme_style = "Dark"

        self.theme_cls.primary_palette = "Orange"

        # Pencere Ayarları (Bilgisayarda test için)
        Window.minimum_width = 400
        Window.minimum_height = 700

        # Ana ekran
        return DashboardScreen()

    def on_start(self):
        """
        Uygulama açıldığında çalışır.
        """
        print(f"{APP_NAME} başlatıldı.")

    def on_stop(self):
        """
        Uygulama kapanırken çalışır.
        """
        print("Uygulama kapatıldı.")


if __name__ == "__main__":
    PeriyodikKontrolApp().run()
