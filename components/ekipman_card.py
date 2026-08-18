# ==========================================
# PERİYODİK KONTROL TAKİP
# components/ekipman_card.py
# ==========================================

from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty

from kivymd.uix.card import MDCard

Builder.load_file("components/ekipman_card.kv")


class EkipmanCard(MDCard):
    """Ekipmanların listelerde gösterildiği kart.

    Dashboard'da sadece bilgi gösterir. Ekipman listesinde ise
    düzenle/pasife al aksiyonları açılır.
    """

    ekipman = ObjectProperty(None, allownone=True)
    actions_visible = BooleanProperty(False)
    on_edit = ObjectProperty(None, allownone=True)
    on_delete = ObjectProperty(None, allownone=True)

    def set_data(self, ekipman):
        self.ekipman = ekipman

        self.ids.lbl_ad.text = ekipman.ekipman_adi or "-"
        self.ids.lbl_id.text = f"ID : {ekipman.ekipman_id or '-'}"
        self.ids.lbl_sorumlu.text = f"Sorumlu : {ekipman.sorumlu or '-'}"
        self.ids.lbl_tarih.text = (
            f"Sonraki Kontrol : {ekipman.sonraki_kontrol or '-'}"
        )
        self.ids.lbl_durum.text = ekipman.durum_yazisi

        renkler = {
            "success": (0, 0.7, 0, 1),
            "warning": (1, 0.6, 0, 1),
            "error": (1, 0, 0, 1),
        }
        self.ids.lbl_durum.text_color = renkler.get(
            ekipman.durum_rengi,
            (1, 1, 1, 1),
        )

    def duzenle(self):
        if callable(self.on_edit) and self.ekipman is not None:
            self.on_edit(self.ekipman)

    def pasif_yap(self):
        if callable(self.on_delete) and self.ekipman is not None:
            self.on_delete(self.ekipman)
