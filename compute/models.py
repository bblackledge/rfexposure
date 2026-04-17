from django.db import models
from django.conf import settings


class RFReport(models.Model):
    # Link to the Pro User
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="final_reports"
    )

    # Metadata for the Dashboard
    project_name = models.CharField(max_length=255, default="Untitled Project")
    created_at = models.DateTimeField(auto_now_add=True)

    # The "Bifurcation" Data
    # This stores all the inputs: power, frequency, distance, etc.
    parameters = models.JSONField()

    class Meta:
        verbose_name_plural = "RFReports"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project_name} ({self.created_at.strftime('%Y-%m-%d')})"





class ComputeExposureParameters(models.Model):
    """ Compute Exposure Parameters """

    report_description = models.CharField(max_length=255, null=True)
    antenna_description = models.CharField(max_length=255, null=True, blank=True)
    antenna_gain = models.FloatField(null=True, blank=True)
    ground_reflection = models.BooleanField(default=False)
    effective_power = models.FloatField(null=True, blank=True)
    duty_factor = models.FloatField(null=True, blank=True)
    transmit_time = models.FloatField(null=True, blank=True)
    receive_time = models.FloatField(null=True, blank=True)
    frequency_mode = models.IntegerField(null=True, blank=True)
    frequency_position = models.IntegerField(null=True, blank=True)
    frequency = models.FloatField(null=True, blank=True)
    operator_name = models.CharField(max_length=128, null=True)
    call_sign = models.CharField(max_length=128, null=True)
    email = models.EmailField(max_length=128, null=True)
    include_calculations = models.BooleanField(default=True)
    mode_factor = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.report_description

    class Meta:
        db_table = 'compute-exposure-parameter'
        verbose_name = 'Compute Exposure Parameter'
        verbose_name_plural = 'Compute Exposure Parameters'
        ordering = ['created_at']



class DutyFactor(models.Model):
    """ Mode Duty Factor """

    id = models.IntegerField(primary_key=True)
    duty_factor_description = models.CharField(max_length=128, null=True)
    duty_factor = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.duty_factor

    class Meta:
        db_table = 'duty-factor'
        verbose_name = 'Duty Factor'
        verbose_name_plural = 'Mode Duty Factor'
        ordering = ['id']


class TransmitReceiveTime(models.Model):
    """ Transmit / Receive Times """

    id = models.IntegerField(primary_key=True)  # Record ID
    time_period = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'transmit-receive-time'
        verbose_name = 'Transmit Receive Time'
        verbose_name_plural = 'Transmit Receive Times'
        ordering = ['id']
