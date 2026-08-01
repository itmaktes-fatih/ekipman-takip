from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen

import firebase
import utils


Builder.load_file("kv/dashboard.kv")


class DashboardScreen(MDScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        Clock.schedule_once(
            self.dashboard_yukle,
            0.2
        )

    def dashboard_yukle(self, *args):

        veriler = firebase.get_ekipmanlar()

        ist = utils.dashboard_istatistik(veriler)

        self.ids.lbl_toplam.text = str(ist["toplam"])

        self.ids.lbl_guvenli.text = str(ist["guvenli"])

        self.ids.lbl_yaklasan.text = str(ist["yaklasan"])

        self.ids.lbl_gecmis.text = str(ist["gecmis"])

        self.ids.yaklasan_liste.clear_widgets()

        for item in ist["yaklasan_liste"]:

            self.ids.yaklasan_liste.add_widget(

                self.kart_olustur(item)

            )

    def kart_olustur(self, item):

        from kivymd.uix.card import MDCard

        from kivymd.uix.label import MDLabel

        kart = MDCard(

            orientation="vertical",

            padding=15,

            radius=[15],

            size_hint_y=None,

            height=90,

            ripple_behavior=True,

            style="filled"

        )

        kart.add_widget(

            MDLabel(

                text=item["ekipman"],

                bold=True,

                font_style="TitleMedium"

            )

        )

        kart.add_widget(

            MDLabel(

                text=f'{item["kalan"]} Gün Kaldı',

                theme_text_color="Secondary"

            )

        )

        return kart
