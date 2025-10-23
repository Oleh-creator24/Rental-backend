from django.apps import AppConfig
from django.contrib import admin

class ConfigConfig(AppConfig):
    name = "config"

    def ready(self):
        admin.site.site_header = "Система аренды жилья"
        admin.site.site_title = "Панель управления"
        admin.site.index_title = "Добро пожаловать в админ-панель"
