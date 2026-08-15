[app]

title = Ekipman Periyodik Kontrol Takibi

package.name = ekipman_kontrol_takibi
package.domain = org.isg

source.dir = .

source.include_exts = py,png,jpg,kv,atlas,json
source.include_patterns = assets/*, components/*, kv/*, screens/*, services/*

version = 1.0.0

requirements = python3==3.11.9,hostpython3==3.11.9,kivy==2.2.0,kivymd==1.2.0,urllib3,chardet,idna,requests,certifi,openssl

orientation = portrait

fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE

android.api = 33
android.minapi = 21
android.ndk = 25b

android.accept_sdk_license = True

android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 0
