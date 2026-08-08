# ==========================================
# PERİYODİK KONTROL TAKİP
# screens/ekipman_listesi.py
# ==========================================

from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen

from services.ekipman_service import EkipmanService

Builder.load_file("kv/ekipman_listesi.kv")


class EkipmanListesiScreen(MDScreen):

    def on_enter(self):
        Clock.schedule_once(self.yukle)

    def yukle(self, *args):
        self.listeyi_doldur(EkipmanService.tumunu_getir())

    def ara(self, text):

        if text == "":
            self.listeyi_doldur(EkipmanService.tumunu_getir())
        else:
            self.listeyi_doldur(EkipmanService.ara(text))

    def listeyi_doldur(self, ekipmanlar):

        from components.ekipman_card import EkipmanCard

        self.ids.liste.clear_widgets()

        for ekipman in ekipmanlar:

            kart = EkipmanCard()
            kart.set_data(ekipman)

            self.ids.liste.add_widget(kart)

    def yeni_ekipman(self):
        self.manager.current = "ekipman_formu"

    def geri(self):
        self.manager.current = "dashboard"
