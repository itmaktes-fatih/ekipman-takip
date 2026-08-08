# ==========================================
# PERİYODİK KONTROL TAKİP
# components/ekipman_card.py
# ==========================================

from kivy.lang import Builder

from kivymd.uix.card import MDCard

Builder.load_file("components/ekipman_card.kv")


class EkipmanCard(MDCard):

    ekipman = None

    def set_data(self, ekipman):

        self.ekipman = ekipman

        self.ids.lbl_ad.text = ekipman.ekipman_adi
        self.ids.lbl_id.text = f"ID : {ekipman.ekipman_id}"
        self.ids.lbl_sorumlu.text = ekipman.sorumlu or "-"
        self.ids.lbl_tarih.text = ekipman.sonraki_kontrol
        self.ids.lbl_durum.text = ekipman.durum_yazisi

        renkler = {
            "success": (0, 0.7, 0, 1),
            "warning": (1, 0.6, 0, 1),
            "error": (1, 0, 0, 1),
        }

        self.ids.lbl_durum.text_color = renkler[ekipman.durum_rengi]
