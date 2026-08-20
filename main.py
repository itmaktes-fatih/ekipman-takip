from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window

from config import APP_NAME

from screens.splash import SplashScreen
from screens.dashboard import DashboardScreen
from screens.ekipman_listesi import EkipmanListesiScreen
from screens.ekipman_formu import EkipmanFormuScreen
from screens.sorumlular import SorumlularScreen


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

        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(EkipmanListesiScreen(name="ekipman_listesi"))
        sm.add_widget(EkipmanFormuScreen(name="ekipman_formu"))
        sm.add_widget(SorumlularScreen(name="sorumlular"))

        sm.current = "splash"

        return sm


if __name__ == "__main__":
    PeriyodikKontrolApp().run()
