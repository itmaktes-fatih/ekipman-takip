# ==========================================
# CACHE
# ==========================================

class Cache:

    ekipmanlar = None

    sorumlular = None

    @classmethod
    def temizle(cls):

        cls.ekipmanlar = None

        cls.sorumlular = None
