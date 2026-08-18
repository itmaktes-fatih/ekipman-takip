# ==========================================
# PERİYODİK KONTROL TAKİP
# screens/ekipman_listesi.py
# ==========================================

from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from services.ekipman_service import EkipmanService

Builder.load_file("kv/ekipman_listesi.kv")


class EkipmanListesiScreen(MDScreen):

    _pasif_dialog = None
    _pasif_ekipman = None

    def on_enter(self):
        Clock.schedule_once(self.yukle, 0.05)

    def yukle(self, *args):
        self.listeyi_doldur(EkipmanService.tumunu_getir())

    def ara(self, text):
        metin = (text or "").strip()

        if not metin:
            self.listeyi_doldur(EkipmanService.tumunu_getir())
        else:
            self.listeyi_doldur(EkipmanService.ara(metin))

    def listeyi_doldur(self, ekipmanlar):
        from components.ekipman_card import EkipmanCard

        self.ids.liste.clear_widgets()

        for ekipman in ekipmanlar:
            kart = EkipmanCard()
            kart.actions_visible = True
            kart.on_edit = self.duzenle_ekipman
            kart.on_delete = self.pasif_ekipman
            kart.set_data(ekipman)
            self.ids.liste.add_widget(kart)

    def yeni_ekipman(self):
        form = self.manager.get_screen("ekipman_formu")
        form.yeni_kayit_modu()
        self.manager.current = "ekipman_formu"

    def duzenle_ekipman(self, ekipman):
        if not ekipman or not ekipman.firebase_key:
            return

        form = self.manager.get_screen("ekipman_formu")
        form.duzenle(ekipman)
        self.manager.current = "ekipman_formu"

    def pasif_ekipman(self, ekipman):
        if not ekipman or not ekipman.firebase_key:
            return

        self._pasif_ekipman = ekipman

        cancel = MDFlatButton(text="VAZGEÇ")
        confirm = MDFlatButton(text="PASİFE AL")

        dialog = MDDialog(
            title="Ekipmanı pasife al",
            text=(
                f"{ekipman.ekipman_adi} ({ekipman.ekipman_id}) pasife alınacak.\n\n"
                "Ekipman silinmeyecek; kayıt Firebase'de korunacaktır."
            ),
            buttons=[cancel, confirm],
        )

        cancel.bind(on_release=lambda *_: dialog.dismiss())
        confirm.bind(
            on_release=lambda *_: self._pasif_onayla(dialog)
        )

        self._pasif_dialog = dialog
        dialog.open()

    def _pasif_onayla(self, dialog):
        ekipman = self._pasif_ekipman
        dialog.dismiss()
        self._pasif_dialog = None
        self._pasif_ekipman = None

        if not ekipman or not ekipman.firebase_key:
            return

        basarili = EkipmanService.sil(ekipman.firebase_key)

        if basarili:
            self.yukle()
        else:
            # Listeyi bozmadan kullanıcıya hata bilgisini ekranda göster.
            self._bilgi_dialog(
                "İşlem başarısız",
                "Ekipman pasife alınamadı. İnternet bağlantısını ve Firebase kurallarını kontrol edin.",
            )

    def _bilgi_dialog(self, baslik, metin):
        kapat = MDFlatButton(text="TAMAM")
        dialog = MDDialog(title=baslik, text=metin, buttons=[kapat])
        kapat.bind(on_release=lambda *_: dialog.dismiss())
        dialog.open()

    def geri(self):
        self.manager.current = "dashboard"
