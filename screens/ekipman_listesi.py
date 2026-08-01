from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen

from services.ekipman_service import EkipmanService

Builder.load_file("kv/ekipman_listesi.kv")


class EkipmanListesiScreen(MDScreen):

    def on_enter(self):
        Clock.schedule_once(self.yukle)

    def yukle(self, *args):

        self.listeyi_doldur(
            EkipmanService.tumunu_getir()
        )

    def ara(self, text):

        if text == "":

            self.listeyi_doldur(
                EkipmanService.tumunu_getir()
            )

        else:

            self.listeyi_doldur(
                EkipmanService.ara(text)
            )

    def listeyi_doldur(self, ekipmanlar):

        self.ids.liste.clear_widgets()

        for ekipman in ekipmanlar:

            kart = self.kart_olustur(ekipman)

            self.ids.liste.add_widget(kart)

    def kart_olustur(self, ekipman):

        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel

        card = MDCard(

            orientation="vertical",

            padding=15,

            radius=[18],

            ripple_behavior=True,

            size_hint_y=None,

            height=130

        )

        card.add_widget(

            MDLabel(

                text=ekipman.ekipman_adi,

                bold=True,

                font_style="TitleMedium"

            )

        )

        card.add_widget(

            MDLabel(

                text=f"ID : {ekipman.ekipman_id}"

            )

        )

        card.add_widget(

            MDLabel(

                text=ekipman.sorumlu

            )

        )

        card.add_widget(

            MDLabel(

                text=f"{ekipman.durum_ikonu} {ekipman.durum_yazisi}"

            )

        )

        return card

    def yeni_ekipman(self):

        self.manager.current = "ekipman_formu"

    def geri(self):

        self.manager.current = "dashboard"
