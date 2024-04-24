from django.apps import AppConfig
# from .controller.firebase_handler import FirebaseAuth


class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance'
    # def ready(self):
    #     firebase = FirebaseAuth()
