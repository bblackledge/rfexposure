from django.db import models
from django.conf import settings


class RFReportForm(models.Model):
    # Link to the Pro User
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="report_forms"
    )

    # Metadata for the Dashboard
    project_name = models.CharField(max_length=255, default="Untitled Project")
    created_at = models.DateTimeField(auto_now_add=True)

    # The "Bifurcation" Data
    # This stores all the inputs: power, frequency, distance, etc.
    parameters = models.JSONField()

    class Meta:
        verbose_name_plural = "RF Reports"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project_name} ({self.created_at.strftime('%Y-%m-%d')})"