from django.contrib.admin.apps import AdminConfig

class CustomAdminConfig(AdminConfig):
    default_site = "src.config.admin_dashboard.CustomAdminSite"
