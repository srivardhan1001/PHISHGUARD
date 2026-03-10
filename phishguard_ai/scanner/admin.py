from django.contrib import admin
from .models import ScanResult


@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ("url", "risk_label", "final_score", "created_at", "api_status")
    list_filter = ("risk_label", "api_status", "created_at")
    search_fields = ("url", "api_verdict")
    ordering = ("-created_at",)

