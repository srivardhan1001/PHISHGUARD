from django.db import models


class ScanResult(models.Model):
    url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    rule_score = models.PositiveIntegerField(default=0)
    api_score = models.PositiveIntegerField(default=0)
    final_score = models.PositiveIntegerField(default=0)
    risk_label = models.CharField(max_length=32, default="Safe")
    issues = models.TextField(blank=True)  # JSON-serialized string of detected issues
    api_verdict = models.CharField(max_length=128, blank=True)
    api_status = models.CharField(max_length=64, blank=True)  # success / unavailable / error

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.url} [{self.risk_label} {self.final_score}]"

