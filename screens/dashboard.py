from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

import firebase
import utils


Builder.load_file("kv/dashboard.kv")


class DashboardScreen(MDScreen):

    def on_enter(self):

        Clock.schedule_once(
            self.verileri_yukle,
            0.2
        )

    def verileri_yukle(self, *args):

        veriler = firebase.get_ekipmanlar()

        ist = utils.dashboard_istatistik(veriler)

        self.ids.lbl_toplam.text = str(ist["toplam"])
        self.ids.lbl_guvenli.text = str(ist["guvenli"])
        self.ids.lbl_yaklasan.text = str(ist["yaklasan"])
        self.ids.lbl_gecmis.text = str(ist["gecmis"])

        self.listeyi_doldur(
            ist["yaklasan_liste"]
        )

    def listeyi_doldur(self, liste):

        self.ids.yaklasan_liste.clear_widgets()

        if len(liste) == 0:

            self.ids.yaklasan_liste.add_widget(

                MDLabel(

                    text="Yaklaşan kontrol bulunmuyor.",

                    halign="center"

                )

            )

            return

        for item in liste:

            card = MDCard(

                orientation="vertical",

                radius=[15],

                padding=15,

                size_hint_y=None,

                height=85,

                ripple_behavior=True

            )

            card.add_widget(

                MDLabel(

                    text=item["ekipman"],

                    bold=True

                )

            )

            card.add_widget(

                MDLabel(

                    text=f'{item["kalan"]} gün kaldı'

                )

            )

            self.ids.yaklasan_liste.add_widget(card)

    def yeni_ekipman(self):
        self.manager.current = "ekipman_formu"

    def ekipmanlar(self):
        self.manager.current = "ekipman_listesi"

    def sorumlular(self):
        self.manager.current = "sorumlular"
