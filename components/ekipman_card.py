# ==========================================
# components/ekipman_card.py
# ==========================================

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.card import MDCard

Builder.load_file("components/ekipman_card.kv")


class EkipmanCard(MDCard):

    ekipman = ObjectProperty(None)

    def on_kv_post(self, base_widget):

        self.verileri_guncelle()

    def on_ekipman(self, instance, value):

        self.verileri_guncelle()

    def verileri_guncelle(self):

        if not self.ekipman:
            return

        self.ids.lbl_ad.text = self.ekipman.ekipman_adi

        self.ids.lbl_id.text = f"ID : {self.ekipman.ekipman_id}"

        self.ids.lbl_sorumlu.text = f"👤 {self.ekipman.sorumlu}"

        self.ids.lbl_tarih.text = f"📅 {self.ekipman.sonraki_kontrol}"

        self.ids.lbl_durum.text = (
            f"{self.ekipman.durum_ikonu} "
            f"{self.ekipman.durum_yazisi}"
        )

        renkler = {
            "success": (0.18, 0.80, 0.44, 1),
            "warning": (1.00, 0.65, 0.00, 1),
            "error":   (0.91, 0.30, 0.24, 1),
        }

        self.ids.lbl_durum.text_color = renkler.get(
            self.ekipman.durum_rengi,
            (1, 1, 1, 1)
        )

    def tiklandi(self):

        """
        İleride detay ekranını açacak.
        """
        print(self.ekipman.ekipman_adi)
