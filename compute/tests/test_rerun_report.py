from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from compute.models import RFReport


class RerunReportTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="worksheet-user",
            email="worksheet@example.com",
            password="password123",
        )
        self.client.force_login(self.user)

        self.report = RFReport.objects.create(
            user=self.user,
            project_name="Worksheet Project",
            parameters={
                "report_description": "Test Report",
                "operator_name": "Test Operator",
                "call_sign": "KJ7ABC",
                "email": "test@example.com",
                "antenna_description": "Test Antenna",
                "antenna_gain": 2.0,
                "ground_reflection": True,
                "effective_power": 100.0,
                "duty_factor": ".2",
                "transmit_time": "1.0",
                "receive_time": "1.0",
                "frequency_mode": "0",
                "frequency_position": "2",
                "frequency": 14.0,
                "include_calculations": True,
            },
        )

    @patch("compute.views.dashboard.rerun_report.ComputeExposureServices")
    def test_download_exposure_report_renders_without_saving(self, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.compute_exposure_report.return_value = (True, "report.pdf", 0)

        response = self.client.get(reverse("compute:rerun_report", args=[self.report.id]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "RF Exposure Report Generation Successful!")
        self.assertContains(response, "Download RF Exposure Report PDF")
        mock_service.compute_exposure_report.assert_called_once()
        args, kwargs = mock_service.compute_exposure_report.call_args
        self.assertEqual(kwargs["user"], self.user)
        self.assertFalse(kwargs["save_to_database"])
        self.assertEqual(kwargs["report_description"], "Test Report")
        self.assertEqual(kwargs["antenna_description"], "Test Antenna")
        self.assertEqual(kwargs["antenna_gain"], 2.0)
        self.assertEqual(kwargs["frequency"], 14.0)
