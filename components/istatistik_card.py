# ==========================================
# components/istatistik_card.py
# ==========================================

from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

Builder.load_file("components/istatistik_card.kv")


class IstatistikCard(MDCard):

    icon = StringProperty("information")

    title = StringProperty("Başlık")

    value = StringProperty("0")

    icon_color = StringProperty("#FFFFFF")
