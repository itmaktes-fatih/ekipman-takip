[app]
title = Ekipman Periyodik Kontrol Takibi
package.name = ekipman_kontrol_takibi
package.domain = org.isg
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Bağımlılıklar
requirements = python3,kivy,requests,certifi,urllib3,chardet,idna

orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0

# Android Yetkileri ve Sürümleri
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 0
