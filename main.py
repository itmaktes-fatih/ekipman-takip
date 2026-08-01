from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window

from config import APP_NAME

from screens.dashboard import DashboardScreen


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

        return sm


if __name__ == "__main__":
    PeriyodikKontrolApp().run()
