# ==========================================
# PERİYODİK KONTROL TAKİP
# services/base_service.py
# ==========================================

class BaseService:

    @staticmethod
    def normalize(text):

        if text is None:
            return ""

        return str(text).strip().lower()

    @staticmethod
    def contains(value, search):

        return BaseService.normalize(search) in BaseService.normalize(value)
