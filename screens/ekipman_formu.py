# ==========================================
# PERİYODİK KONTROL TAKİP
# screens/ekipman_formu.py
# ==========================================

from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.snackbar import MDSnackbarText

import firebase
import utils

from services.sorumlu_service import SorumluService

Builder.load_file("kv/ekipman_formu.kv")


class EkipmanFormuScreen(MDScreen):

    def on_enter(self):
        Clock.schedule_once(self.sorumlulari_yukle)

    def sorumlulari_yukle(self, *args):

        self.ids.cmb_sorumlu.values = []

        data = firebase.get_sorumlular()

        for key, value in data.items():
            if value.get("aktif", True):
                self.ids.cmb_sorumlu.values.append(value["ad"])

    def tarih_degisti(self):

        tarih = self.ids.txt_tarih.text
        periyot = self.ids.txt_periyot.text

        if not tarih or not periyot:
            return

        if not utils.tarih_dogrula(tarih):
            return

        sonraki = utils.sonraki_kontrol_tarihi(tarih, int(periyot))

        self.ids.lbl_sonraki.text = sonraki

    def kaydet(self):

        if self.ids.txt_ad.text == "":
            return

        if self.ids.txt_id.text == "":
            return

        if not utils.tarih_dogrula(self.ids.txt_tarih.text):
            return

        sorumlu_id = SorumluService.id_bul(self.ids.cmb_sorumlu.text)

        veri = utils.ekipman_olustur(
            self.ids.txt_ad.text,
            self.ids.txt_id.text,
            self.ids.txt_tarih.text,
            int(self.ids.txt_periyot.text),
            sorumlu_id,
        )

        if firebase.ekipman_ekle(veri):

            MDSnackbar(
                MDSnackbarText(text="Kayıt başarıyla oluşturuldu.")
            ).open()

            self.temizle()

        else:

            MDSnackbar(
                MDSnackbarText(text="Kayıt oluşturulamadı.")
            ).open()

    def temizle(self):

        self.ids.txt_ad.text = ""
        self.ids.txt_id.text = ""
        self.ids.txt_tarih.text = ""
        self.ids.txt_periyot.text = ""
        self.ids.cmb_sorumlu.text = ""
        self.ids.lbl_sonraki.text = "-"

    def geri(self):
        self.manager.current = "ekipman_listesi"
