# ==========================================
# PERİYODİK KONTROL TAKİP
# screens/sorumlular.py
# ==========================================

from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

from models import Sorumlu
from services.sorumlu_service import SorumluService

Builder.load_file("kv/sorumlular.kv")


class SorumlularScreen(MDScreen):

    def on_enter(self):
        Clock.schedule_once(self.yukle)

    def yukle(self, *args):

        from kivymd.uix.card import MDCard
        from kivymd.uix.label import MDLabel

        self.ids.liste.clear_widgets()

        for sorumlu in SorumluService.tumunu_getir():

            card = MDCard(
                orientation="vertical",
                padding=15,
                radius=[18],
                size_hint_y=None,
                height="110dp",
            )

            card.add_widget(
                MDLabel(text=sorumlu.ad, bold=True, font_style="Subtitle1")
            )
            card.add_widget(MDLabel(text=sorumlu.telefon or "-"))
            card.add_widget(MDLabel(text=sorumlu.email or "-"))

            self.ids.liste.add_widget(card)

    def kaydet(self):

        if self.ids.txt_ad.text == "":
            return

        sorumlu = Sorumlu(
            ad=self.ids.txt_ad.text,
            telefon=self.ids.txt_telefon.text,
            email=self.ids.txt_email.text,
        )

        if SorumluService.ekle(sorumlu):

            Snackbar(text="Sorumlu eklendi.").open()

            self.ids.txt_ad.text = ""
            self.ids.txt_telefon.text = ""
            self.ids.txt_email.text = ""

            self.yukle()

        else:

            Snackbar(text="Sorumlu eklenemedi.").open()

    def geri(self):
        self.manager.current = "dashboard"
