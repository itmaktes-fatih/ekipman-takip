import os
from datetime import datetime
import threading
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock

# 🚨 CANLI FİREBASE BAĞLANTISI (Kayıtlar bu adreste toplanır)
FIREBASE_URL = "https://kacis-seti-takip-default-rtdb.europe-west1.firebasedatabase.app/"

# Evrensel İSG Renk Paleti
ARKA_PLAN = get_color_from_hex("#1E2022")       
TEMA_RENGI = get_color_from_hex("#E67E22")      
FORM_RENGI = get_color_from_hex("#2C3E50")      
YAZI_RENGI = get_color_from_hex("#ECF0F1")      
BUTON_YESIL = get_color_from_hex("#27AE60")     
BUTON_KIRMIZI = get_color_from_hex("#C0392B")    

class RenkliKutu(BoxLayout):
    def __init__(self, bg_color, radius=[10], **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=radius)
        self.bind(pos=self.guncelle, size=self.guncelle)
    def guncelle(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class EkipmanTakipEkrani(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=8, **kwargs)
        self.secili_kayit_id = None
        self.tum_bulut_verisi = {}

        # Üst Başlık
        self.lbl_durum = Label(text="EKİPMAN PERİYODİK KONTROL TAKİBİ", size_hint_y=0.06, color=TEMA_RENGI, bold=True, font_size='16sp')
        self.add_widget(self.lbl_durum)

        # Form Alanı
        form_karti = RenkliKutu(bg_color=FORM_RENGI, orientation='vertical', padding=8, spacing=6, size_hint_y=0.40)
        self.input_id = TextInput(hint_text="Ekipman ID / Barkod / Plaka (*)", multiline=False, font_size='14sp', write_tab=False)
        self.input_adi = TextInput(hint_text="Ekipman Adı / Tanımı (*)", multiline=False, font_size='14sp', write_tab=False)
        self.input_tarih = TextInput(hint_text="Son Kontrol Tarihi (GG.AA.YYYY) (*)", multiline=False, font_size='14sp', write_tab=False)
        self.input_periyot = TextInput(hint_text="Kontrol Periyodu (Gün - Örn: 90, 180) (*)", multiline=False, font_size='14sp', input_filter='int', write_tab=False)
        self.input_sorumlu = TextInput(hint_text="Sorumlu Kişi / Firma", multiline=False, font_size='14sp', write_tab=False)
        self.input_mail = TextInput(hint_text="İletişim E-Posta Adresi", multiline=False, font_size='14sp', write_tab=False)

        form_karti.add_widget(self.input_id)
        form_karti.add_widget(self.input_adi)
        form_karti.add_widget(self.input_tarih)
        form_karti.add_widget(self.input_periyot)
        form_karti.add_widget(self.input_sorumlu)
        form_karti.add_widget(self.input_mail)
        self.add_widget(form_karti)

        # İşlem Butonları
        islem_butonlari = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=6)
        btn_ekle = Button(text="BULUTA KAYDET / GÜNCELLE", background_normal='', background_color=BUTON_YESIL, font_size='14sp', bold=True)
        btn_ekle.bind(on_press=lambda inst: threading.Thread(target=self.ekipman_kaydet_click).start())
        btn_sil = Button(text="SİL", background_normal='', background_color=BUTON_KIRMIZI, font_size='14sp', bold=True, size_hint_x=0.3)
        btn_sil.bind(on_press=lambda inst: threading.Thread(target=self.ekipman_sil_click).start())
        islem_butonlari.add_widget(btn_ekle)
        islem_butonlari.add_widget(btn_sil)
        self.add_widget(islem_butonlari)

        # Arama ve Yenileme
        liste_buton_duzeni = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=6)
        btn_yenile = Button(text="🔄 Yenile", background_normal='', background_color=get_color_from_hex("#7F8C8D"), font_size='13sp', bold=True, size_hint_x=0.3)
        btn_yenile.bind(on_press=self.verileri_yenile_thread)
        self.input_arama = TextInput(hint_text="ID veya İsim ile canlı ara...", multiline=False, font_size='14sp')
        self.input_arama.bind(text=self.arama_yap)
        liste_buton_duzeni.add_widget(btn_yenile)
        liste_buton_duzeni.add_widget(self.input_arama)
        self.add_widget(liste_buton_duzeni)

        # Liste Ekranı
        liste_karti = RenkliKutu(bg_color=get_color_from_hex("#2C3E50"), orientation='vertical', padding=8, size_hint_y=0.38)
        scroll = ScrollView(bar_width=8)
        self.lbl_liste = Label(text="Kayıtlar yükleniyor...", size_hint_y=None, halign="left", valign="top", font_size='13sp', color=YAZI_RENGI)
        self.lbl_liste.bind(texture_size=self.lbl_liste.setter('size'))
        scroll.add_widget(self.lbl_liste)
        liste_karti.add_widget(scroll)
        self.add_widget(liste_karti)

        self.verileri_yenile_thread(None)

    def DurumGuncelle(self, metin, renk):
        self.lbl_durum.text = metin
        self.lbl_durum.color = renk

    def formu_temizle(self):
        self.input_id.text = ""
        self.input_adi.text = ""
        self.input_tarih.text = ""
        self.input_periyot.text = ""
        self.input_sorumlu.text = ""
        self.input_mail.text = ""
        self.secili_kayit_id = None

    def verileri_yenile_thread(self, instance):
        threading.Thread(target=self.verileri_cek).start()

    def verileri_cek(self):
        try:
            res = requests.get(f"{FIREBASE_URL}ekipmanlar.json", timeout=10)
            Clock.schedule_once(lambda dt: self.listeleme_yap(res.json()))
        except:
            Clock.schedule_once(lambda dt: self.DurumGuncelle("Bağlantı Hatası!", BUTON_KIRMIZI))

    def listeleme_yap(self, result):
        if not result:
            self.lbl_liste.text = "Firebase üzerinde henüz kayıtlı ekipman yok."
            self.tum_bulut_verisi = {}
            return
        self.tum_bulut_verisi = result
        self.rapor_olustur(result)

    def rapor_olustur(self, veri_havuzu):
        bugun = datetime.now()
        rapor = ""
        for k_id, v in veri_havuzu.items():
            try:
                kontrol_tarihi = datetime.strptime(v.get('son_kontrol_tarihi'), "%d.%m.%Y")
                periyot_gun = int(v.get('kontrol_periyodu', 0))
                
                import datetime as dt_mod
                gecerlilik_tarihi = kontrol_tarihi + dt_mod.timedelta(days=periyot_gun)
                kalan_gun = (gecerlilik_tarihi - bugun).days + 1
                
                if kalan_gun <= 0:
                    durum = f"🔴 SÜRESİ GEÇMİŞ! ({abs(kalan_gun)} gün)"
                elif kalan_gun <= 15:
                    durum = f"🟡 KRİTİK ({kalan_gun} gün)"
                else:
                    durum = f"🟢 GÜVENLİ ({kalan_gun} gün)"

                rapor += f"📦 ID: {v.get('ekipman_id')} | {v.get('ekipman_adi')}\n"
                rapor += f"⏳ Vade: {gecerlilik_tarihi.strftime('%d.%m.%Y')} -> {durum}\n"
                rapor += f"👤 Sorumlu: {v.get('sorumlu_kisi','-')}\n\n"
            except:
                continue
        self.lbl_liste.text = rapor

    def arama_yap(self, instance, text):
        kriter = text.strip().lower()
        if not kriter:
            self.rapor_olustur(self.tum_bulut_verisi)
            return
        filtrelenmis = {k: v for k, v in self.tum_bulut_verisi.items() if kriter in v.get('ekipman_id','').lower() or kriter in v.get('ekipman_adi','').lower()}
        if len(filtrelenmis) == 1:
            for k_id, v in filtrelenmis.items():
                self.secili_kayit_id = k_id
                self.input_id.text = v.get('ekipman_id','')
                self.input_adi.text = v.get('ekipman_adi','')
                self.input_tarih.text = v.get('son_kontrol_tarihi','')
                self.input_periyot.text = str(v.get('kontrol_periyodu',''))
                self.input_sorumlu.text = v.get('sorumlu_kisi','')
                self.input_mail.text = v.get('sorumlu_mail','')
        self.rapor_olustur(filtrelenmis)

    def ekipman_kaydet_click(self):
        e_id = self.input_id.text.strip()
        e_adi = self.input_adi.text.strip()
        e_tarih = self.input_tarih.text.strip()
        e_periyot = self.input_periyot.text.strip()
        
        if not e_id or not e_adi or not e_tarih or not e_periyot: return
        try: datetime.strptime(e_tarih, "%d.%m.%Y")
        except: return

        yeni = {
            "ekipman_id": e_id, "ekipman_adi": e_adi, "son_kontrol_tarihi": e_tarih,
            "kontrol_periyodu": int(e_periyot), "sorumlu_kisi": self.input_sorumlu.text.strip(), "sorumlu_mail": self.input_mail.text.strip()
        }
        if self.secili_kayit_id:
            requests.patch(f"{FIREBASE_URL}ekipmanlar/{self.secili_kayit_id}.json", json=yeni)
        else:
            requests.post(f"{FIREBASE_URL}ekipmanlar.json", json=yeni)
        
        Clock.schedule_once(lambda dt: self.formu_temizle())
        self.verileri_yenile_thread(None)

    def ekipman_sil_click(self):
        if not self.secili_kayit_id: return
        requests.delete(f"{FIREBASE_URL}ekipmanlar/{self.secili_kayit_id}.json")
        self.formu_temizle()
        self.verileri_yenile_thread(None)

class EkipmanPeriyodikKontrolTakibiApp(App):
    def build(self):
        self.title = "Ekipman Periyodik Kontrol Takibi"
        return EkipmanTakipEkrani()

if __name__ == "__main__":
    EkipmanPeriyodikKontrolTakibiApp().run()
