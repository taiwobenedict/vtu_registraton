from django.contrib import admin
from .models import License

@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('activation_key', 'domain', 'key_sent', 'created_at', 'updated_at')
