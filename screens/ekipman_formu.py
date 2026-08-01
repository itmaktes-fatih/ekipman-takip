from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.snackbar import MDSnackbarText

import firebase
import utils

Builder.load_file("kv/ekipman_formu.kv")


class EkipmanFormuScreen(MDScreen):

    def on_enter(self):
        Clock.schedule_once(self.sorumlulari_yukle)

    def sorumlulari_yukle(self, *args):

        self.ids.cmb_sorumlu.values = []

        data = firebase.get_sorumlular()

        for key, value in data.items():
            self.ids.cmb_sorumlu.values.append(value["ad"])

    def tarih_degisti(self):

        tarih = self.ids.txt_tarih.text
        periyot = self.ids.txt_periyot.text

        if not tarih:
            return

        if not periyot:
            return

        if not utils.tarih_dogrula(tarih):
            return

        sonraki = utils.sonraki_kontrol_tarihi(
            tarih,
            int(periyot)
        )

        self.ids.lbl_sonraki.text = sonraki

    def kaydet(self):

        if self.ids.txt_ad.text == "":
            return

        if self.ids.txt_id.text == "":
            return

        if not utils.tarih_dogrula(
                self.ids.txt_tarih.text):
            return

        veri = utils.ekipman_olustur(

            self.ids.txt_ad.text,

            self.ids.txt_id.text,

            self.ids.txt_tarih.text,

            int(self.ids.txt_periyot.text),

            self.ids.cmb_sorumlu.text

        )

        if firebase.ekipman_ekle(veri):

            MDSnackbar(
                MDSnackbarText(
                    text="Kayıt başarıyla oluşturuldu."
                )
            ).open()

            self.temizle()

        else:

            MDSnackbar(
                MDSnackbarText(
                    text="Kayıt oluşturulamadı."
                )
            ).open()

    def temizle(self):

        self.ids.txt_ad.text = ""
        self.ids.txt_id.text = ""
        self.ids.txt_tarih.text = ""
        self.ids.txt_periyot.text = ""
        self.ids.cmb_sorumlu.text = ""
        self.ids.lbl_sonraki.text = "-"
