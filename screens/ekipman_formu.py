# ==========================================
# PERİYODİK KONTROL TAKİP
# screens/ekipman_formu.py
# ==========================================

import os
import threading

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform

from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar

import firebase
import utils

from services import etiket_service

from services.sorumlu_service import SorumluService
from services.ekipman_service import EkipmanService

Builder.load_file("kv/ekipman_formu.kv")


class EkipmanFormuScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.duzenleme_modu = False
        self.duzenlenen_key = None

    def on_enter(self):
        Clock.schedule_once(self.sorumlulari_yukle, 0.05)

    def sorumlulari_yukle(self, *args):
        self.ids.cmb_sorumlu.values = []

        data = firebase.get_sorumlular()

        if not isinstance(data, dict):
            return

        for value in data.values():
            if value.get("aktif", True):
                ad = value.get("ad", "").strip()
                if ad:
                    self.ids.cmb_sorumlu.values.append(ad)

        # Düzenleme sırasında sorumlu seçimini, liste yüklendikten sonra geri yükle.
        if self.duzenleme_modu and self.duzenlenen_key:
            ekipman = getattr(self, "_duzenlenen_ekipman", None)
            if ekipman:
                self.ids.cmb_sorumlu.text = SorumluService.ad_bul(
                    ekipman.sorumlu_id
                )

    def tarih_degisti(self, *args):
        tarih = self.ids.txt_tarih.text.strip()
        periyot = self.ids.txt_periyot.text.strip()

        if not tarih or not periyot:
            self.ids.lbl_sonraki.text = "-"
            return

        if not utils.tarih_dogrula(tarih):
            self.ids.lbl_sonraki.text = "-"
            return

        try:
            periyot_int = int(periyot)
        except (ValueError, TypeError):
            self.ids.lbl_sonraki.text = "-"
            return

        if periyot_int <= 0:
            self.ids.lbl_sonraki.text = "-"
            return

        self.ids.lbl_sonraki.text = utils.sonraki_kontrol_tarihi(
            tarih,
            periyot_int,
        )

    # --------------------------------------------------
    # MODLAR
    # --------------------------------------------------

    def yeni_kayit_modu(self):
        self.duzenleme_modu = False
        self.duzenlenen_key = None
        self._duzenlenen_ekipman = None
        self.temizle()

    def duzenle(self, ekipman):
        """Mevcut ekipmanı aynı form üzerinde düzenleme modunda açar."""
        self.duzenleme_modu = True
        self.duzenlenen_key = ekipman.firebase_key
        self._duzenlenen_ekipman = ekipman

        self.ids.txt_ad.text = ekipman.ekipman_adi or ""
        self.ids.txt_id.text = ekipman.ekipman_id or ""
        self.ids.txt_tarih.text = ekipman.son_kontrol or ""
        self.ids.txt_periyot.text = str(ekipman.periyot or 365)

        sorumlu_ad = SorumluService.ad_bul(ekipman.sorumlu_id)
        self.ids.cmb_sorumlu.text = sorumlu_ad if sorumlu_ad != "-" else "Seçiniz"

        self.tarih_degisti()

    # --------------------------------------------------
    # ETİKET TARAMA
    # --------------------------------------------------

    def _izin_iste(self, *izinler):
        if platform != "android":
            return
        try:
            from android.permissions import request_permissions
            request_permissions(list(izinler))
        except Exception as e:
            print("İzin isteği hatası:", e)

    def etiket_cek(self):
        """Kamerayla etiket fotoğrafı çeker."""
        self._izin_iste("android.permission.CAMERA")

        try:
            from kivy.app import App
            from plyer import camera

            yol = os.path.join(App.get_running_app().user_data_dir, "etiket.jpg")
            if os.path.exists(yol):
                os.remove(yol)

            camera.take_picture(
                filename=yol,
                on_complete=lambda f: Clock.schedule_once(
                    lambda dt: self._foto_hazir(f), 0
                ),
            )
        except Exception as e:
            self._mesaj(f"Kamera açılamadı: {e}")

    def etiket_sec(self):
        """Galeriden etiket fotoğrafı seçer."""
        self._izin_iste(
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.READ_MEDIA_IMAGES",
        )

        try:
            from plyer import filechooser

            filechooser.open_file(
                on_selection=lambda sec: Clock.schedule_once(
                    lambda dt: self._foto_hazir(sec[0] if sec else None), 0
                ),
                filters=[["Resim", "*.jpg", "*.jpeg", "*.png"]],
            )
        except Exception as e:
            self._mesaj(f"Dosya seçilemedi: {e}")

    def _foto_hazir(self, yol):
        if not yol or not os.path.exists(yol):
            self._mesaj("Fotoğraf alınamadı.")
            return

        self._tarama_durumu("Etiket okunuyor...", mesgul=True)
        threading.Thread(target=self._etiket_isle, args=(yol,), daemon=True).start()

    def _etiket_isle(self, yol):
        """Arka planda: etiketi oku ve sistemde kayıtlı mı diye bak."""
        try:
            sonuc = etiket_service.etiket_oku(yol)
            sonuc["mevcut"] = (
                EkipmanService.id_ile_bul(sonuc["ekipman_id"])
                if sonuc["ekipman_id"]
                else None
            )
            Clock.schedule_once(lambda dt: self._etiket_sonucu(sonuc), 0)

        except etiket_service.EtiketHatasi as e:
            hata = str(e)
            Clock.schedule_once(lambda dt: self._etiket_hatasi(hata), 0)

        except Exception as e:
            hata = f"Beklenmeyen hata: {e}"
            Clock.schedule_once(lambda dt: self._etiket_hatasi(hata), 0)

    def _etiket_hatasi(self, hata):
        self._tarama_durumu("", mesgul=False)
        self._mesaj(hata)

    def _etiket_sonucu(self, sonuc):
        mevcut = sonuc["mevcut"]

        if mevcut:
            # Kayıtlı ekipman: mevcut kaydı düzenleme modunda aç,
            # yalnızca kontrol tarihi ve periyodu etiketten güncelle.
            self.duzenle(mevcut)
            bilgi = f"Kayıtlı ekipman bulundu ({mevcut.ekipman_adi}). Tarih güncellenecek."
        else:
            self.yeni_kayit_modu()
            self.ids.txt_ad.text = sonuc["ekipman_adi"]
            self.ids.txt_id.text = sonuc["ekipman_id"]
            bilgi = "Yeni ekipman. Bilgileri kontrol edip Kaydet'e basın."

        if sonuc["son_kontrol"]:
            self.ids.txt_tarih.text = sonuc["son_kontrol"]
            self.ids.txt_periyot.text = str(sonuc["periyot"])

        self.tarih_degisti()

        uyari = " ".join(sonuc["uyarilar"])
        self._tarama_durumu((bilgi + " " + uyari).strip(), mesgul=False)

    def _tarama_durumu(self, metin, mesgul):
        self.ids.lbl_etiket_durum.text = metin
        self.ids.btn_etiket_cek.disabled = mesgul
        self.ids.btn_etiket_sec.disabled = mesgul

    # --------------------------------------------------
    # KAYDET / GÜNCELLE
    # --------------------------------------------------

    def kaydet(self):
        try:
            ad = self.ids.txt_ad.text.strip()
            ekipman_id = self.ids.txt_id.text.strip()
            tarih = self.ids.txt_tarih.text.strip()
            periyot_text = self.ids.txt_periyot.text.strip()
            sorumlu_ad = self.ids.cmb_sorumlu.text.strip()

            if not ad:
                self._mesaj("Ekipman adı giriniz.")
                return

            if not ekipman_id:
                self._mesaj("Ekipman ID giriniz.")
                return

            if not tarih or not utils.tarih_dogrula(tarih):
                self._mesaj("Son kontrol tarihini GG.AA.YYYY formatında giriniz.")
                return

            if not periyot_text:
                self._mesaj("Periyot giriniz.")
                return

            try:
                periyot = int(periyot_text)
            except ValueError:
                self._mesaj("Periyot sayı olmalıdır.")
                return

            if periyot <= 0:
                self._mesaj("Periyot 0'dan büyük olmalıdır.")
                return

            # Aynı ekipman ID'sinin ikinci kez kullanılmasını engelle.
            if EkipmanService.ekipman_id_kullaniliyor(
                ekipman_id,
                haric_key=self.duzenlenen_key if self.duzenleme_modu else None,
            ):
                self._mesaj(f"'{ekipman_id}' ID'li ekipman zaten kayıtlı.")
                return

            sorumlu_id = ""
            if sorumlu_ad and sorumlu_ad != "Seçiniz":
                sorumlu_id = SorumluService.id_bul(sorumlu_ad)

            veri = utils.ekipman_olustur(
                ad,
                ekipman_id,
                tarih,
                periyot,
                sorumlu_id,
            )

            if self.duzenleme_modu:
                basarili = EkipmanService.guncelle(
                    self.duzenlenen_key,
                    veri,
                )
                mesaj = "Ekipman başarıyla güncellendi."
            else:
                basarili = EkipmanService.ekle(veri)
                mesaj = "Ekipman başarıyla kaydedildi."

            if not basarili:
                self._mesaj("İşlem tamamlanamadı. Firebase bağlantısını kontrol edin.")
                return

            self.temizle()
            self.duzenleme_modu = False
            self.duzenlenen_key = None
            self._duzenlenen_ekipman = None

            self._mesaj(mesaj)

            # Listeyi güncelle ve ekipmanlar ekranına dön.
            liste = self.manager.get_screen("ekipman_listesi")
            liste.yukle()
            self.manager.current = "ekipman_listesi"

        except Exception as e:
            print("===================================")
            print("EKİPMAN KAYIT/GÜNCELLEME HATASI")
            print(type(e).__name__)
            print(str(e))
            print("===================================")
            self._mesaj(f"İşlem sırasında hata oluştu: {e}")

    def temizle(self):
        self.ids.txt_ad.text = ""
        self.ids.txt_id.text = ""
        self.ids.txt_tarih.text = ""
        self.ids.txt_periyot.text = ""
        self.ids.cmb_sorumlu.text = "Seçiniz"
        self.ids.lbl_sonraki.text = "-"
        self.ids.lbl_etiket_durum.text = ""

    def _mesaj(self, metin):
        """Snackbar hatası uygulamayı düşürmesin diye güvenli bildirim."""
        try:
            Snackbar(text=metin, duration=2.5).open()
        except Exception:
            print("BİLDİRİM:", metin)

    def geri(self):
        self.yeni_kayit_modu()
        self.manager.current = "ekipman_listesi"
