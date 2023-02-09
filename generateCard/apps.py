from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class GeneratecardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "generateCard"

class NewAdminConfig(AdminConfig):
    default_site='generateCard.admin.NewAdminSite'
