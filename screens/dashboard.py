# ==========================================
# PERİYODİK KONTROL TAKİP
# screens/dashboard.py
# ==========================================

from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen

from services.ekipman_service import EkipmanService

Builder.load_file("kv/dashboard.kv")


class DashboardScreen(MDScreen):

    def on_enter(self):
        Clock.schedule_once(self.yukle, 0.1)

    def yukle(self, *args):

        veri = EkipmanService.dashboard_verisi()

        self.ids.toplam_card.value = str(veri["toplam"])
        self.ids.guvenli_card.value = str(veri["guvenli"])
        self.ids.yaklasan_card.value = str(veri["yaklasan"])
        self.ids.gecmis_card.value = str(veri["gecmis"])

        self.yaklasanlari_goster(veri["yaklasan_liste"])

    def yaklasanlari_goster(self, liste):

        from components.ekipman_card import EkipmanCard

        self.ids.yaklasan_liste.clear_widgets()

        if not liste:
            return

        for ekipman in liste:
            kart = EkipmanCard()
            kart.set_data(ekipman)
            self.ids.yaklasan_liste.add_widget(kart)

    def ekipmanlar(self):
        self.manager.current = "ekipman_listesi"

    def sorumlular(self):
        self.manager.current = "sorumlular"
