# ==========================================
# PERİYODİK KONTROL TAKİP
# screens/ekipman_formu.py
# ==========================================

from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

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

        try:

            # -----------------------------
            # ZORUNLU ALAN KONTROLLERİ
            # -----------------------------

            ad = self.ids.txt_ad.text.strip()
            ekipman_id = self.ids.txt_id.text.strip()
            tarih = self.ids.txt_tarih.text.strip()
            periyot_text = self.ids.txt_periyot.text.strip()
            sorumlu_ad = self.ids.cmb_sorumlu.text.strip()

            if not ad:
                Snackbar(text="Ekipman adı giriniz.").open()
                return

            if not ekipman_id:
                Snackbar(text="Ekipman ID giriniz.").open()
                return

            if not tarih or not utils.tarih_dogrula(tarih):
                Snackbar(text="Geçerli bir tarih giriniz.").open()
                return

            if not periyot_text:
                Snackbar(text="Periyot giriniz.").open()
                return

            try:
                periyot = int(periyot_text)
            except ValueError:
                Snackbar(text="Periyot sayı olmalıdır.").open()
                return

            if periyot <= 0:
                Snackbar(text="Periyot 0'dan büyük olmalıdır.").open()
                return

            # -----------------------------
            # SORUMLU BUL
            # -----------------------------

            sorumlu_id = ""

            if sorumlu_ad and sorumlu_ad != "Seçiniz":
                sorumlu_id = SorumluService.id_bul(sorumlu_ad)

            # -----------------------------
            # VERİ OLUŞTUR
            # -----------------------------

            veri = utils.ekipman_olustur(
                ad,
                ekipman_id,
                tarih,
                periyot,
                sorumlu_id,
            )

            # -----------------------------
            # FIREBASE KAYDI
            # -----------------------------

            firebase_key = firebase.ekipman_ekle(veri)

            if not firebase_key:
                Snackbar(text="Kayıt oluşturulamadı.").open()
                return

            # -----------------------------
            # FORM TEMİZLE
            # -----------------------------

            self.temizle()

            # -----------------------------
            # BAŞARI MESAJI
            # -----------------------------

            Snackbar(
                text="Ekipman başarıyla kaydedildi.",
                duration=2,
            ).open()

        except Exception as e:

            print("===================================")
            print("EKİPMAN KAYIT HATASI")
            print(type(e).__name__)
            print(str(e))
            print("===================================")

            try:
                Snackbar(
                    text=f"Kayıt sırasında hata: {e}",
                    duration=3,
                ).open()
            except Exception:
                pass
                
    def temizle(self):

        self.ids.txt_ad.text = ""
        self.ids.txt_id.text = ""
        self.ids.txt_tarih.text = ""
        self.ids.txt_periyot.text = ""
        self.ids.cmb_sorumlu.text = "Seçiniz"
        self.ids.lbl_sonraki.text = "-"

    def geri(self):
        self.manager.current = "ekipman_listesi"
