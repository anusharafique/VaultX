from django.contrib import admin
from .models import VaultItem


@admin.register(VaultItem)
class VaultItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')