from django.contrib import admin
from .models import License

@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('key', 'domain', 'is_active', 'created_at', 'updated_at')
