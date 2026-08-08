# Ekipman Periyodik Kontrol Takibi

## Bu pakette yapılanlar

1. **Dosya isim/içerik karışıklığı düzeltildi.** Yüklediğiniz dosyaların her
   birinin içeriği, dosya adıyla uyuşmuyordu (ör. `models.py` diye
   adlandırılan dosyanın içeriği aslında `config.py`'ye aitti). Her dosya
   gerçek içeriğine göre doğru isim ve klasöre (`screens/`, `services/`,
   `components/`, `kv/`) taşındı.

2. **`firebase.py` yeniden yazıldı.** Orijinalde `firebase_admin` (sunucu
   SDK'sı) kullanılıyordu; bu, Android'de çalışmaz ve bir servis hesabı JSON
   anahtarını telefona gömmeyi gerektirirdi. Bunun yerine `buildozer.spec`
   içinde zaten yer alan `requests` kütüphanesiyle Firebase Realtime
   Database REST API'sine bağlanıyor.

3. **Eksik dosyalar tamamlandı** (hiç yüklenmemişlerdi):
   - `utils.py` (tarih/durum hesaplama fonksiyonları)
   - `services/ekipman_service.py`, `services/sorumlu_service.py`
   - `screens/sorumlular.py`, `kv/sorumlular.kv`, `kv/ekipman_formu.kv`
   - `components/istatistik_card.kv`

4. **Küçük hatalar düzeltildi:** `kart.ekipman = ekipman` yerine
   `kart.set_data(ekipman)`; form ekranında sorumlu adı yerine
   `sorumlu_id` kaydediliyor; `firebase.get_sorumlular` için takma ad
   eklendi.

## Firebase Realtime Database kuralları

Şu an `config.py` içindeki `FIREBASE_AUTH_TOKEN` boş. Database kurallarınız
herkese açık okuma/yazmaya izin vermiyorsa (test modu değilse), buraya bir
kimlik doğrulama tokenı eklemeniz gerekir; aksi halde istekler 401/403
döner.

## GitHub üzerinden APK almak için adımlar

1. Bu klasörün **tüm içeriğini** (gizli `.github` klasörü dahil) yeni bir
   GitHub reposuna push edin.
2. Repo → **Actions** sekmesine gidin. `main`/`master` dalına push
   yaptığınızda `Otomatik APK Derleyici` workflow'u otomatik başlar
   (istersen "Run workflow" ile elle de tetikleyebilirsiniz).
3. Build bitince (~20-40 dk, ilk seferde daha uzun sürebilir) Actions
   çalıştırmasının altındaki **Artifacts** bölümünden
   `Ekipman_Periyodik_Kontrol_Takibi_APK` dosyasını indirin — içinde
   `.apk` dosyanız olacak.
4. Hata alırsanız aynı bölümdeki `Build_Loglari` artifact'ini incelemeniz
   yeterli.
