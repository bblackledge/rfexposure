from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse

from compute.views.compute_exposure import ComputeExposure


class ComputeExposureViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_anonymous_user_can_open_worksheet(self):
        response = self.client.get(reverse("compute:compute-form"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "RF Exposure Calculation Worksheet")

    @patch("compute.views.compute_exposure.ComputeFormServices")
    @patch("compute.views.compute_exposure.ComputeExposureServices")
    def test_anonymous_user_redirects_to_download_page(self, mock_service_class, mock_form_services_class):
        mock_form_services = mock_form_services_class.return_value
        mock_form_services.normalize_post_data.return_value = {
            "report_description": "Test Report",
            "antenna_description": "Test Antenna",
            "antenna_gain": "2.0",
            "ground_reflection": True,
            "effective_power": "100.0",
            "duty_factor": ".2",
            "transmit_time": "2.0",
            "receive_time": "4.0",
            "frequency_mode": "0",
            "frequency_position": "1",
            "frequency": "14.0",
            "operator_name": "Test Operator",
            "call_sign": "KJ7ABC",
            "email": "test@example.com",
            "include_calculations": True,
        }

        mock_service = mock_service_class.return_value
        mock_service.compute_exposure_report.return_value = (True, "report.pdf", 42)

        request = self.factory.post(reverse("compute:compute-form"), data={})
        request.user = AnonymousUser()
        request.session = {}

        response = ComputeExposure().post(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("compute:success-form-submission"))
        self.assertEqual(request.session["output_pdf_filename"], "report.pdf")
        self.assertEqual(request.session["record_id"], 42)

    @patch("compute.views.compute_exposure.ComputeFormServices")
    @patch("compute.views.compute_exposure.ComputeExposureServices")
    def test_preview_mode_disables_database_write(self, mock_service_class, mock_form_services_class):
        mock_form_services = mock_form_services_class.return_value
        mock_form_services.normalize_post_data.return_value = {
            "report_description": "Test Report",
            "antenna_description": "Test Antenna",
            "antenna_gain": "2.0",
            "ground_reflection": True,
            "effective_power": "100.0",
            "duty_factor": ".2",
            "transmit_time": "2.0",
            "receive_time": "4.0",
            "frequency_mode": "0",
            "frequency_position": "1",
            "frequency": "14.0",
            "operator_name": "Test Operator",
            "call_sign": "KJ7ABC",
            "email": "test@example.com",
            "include_calculations": True,
        }

        mock_service = mock_service_class.return_value
        mock_service.compute_exposure_report.return_value = (True, "report.pdf", 0)

        request = self.factory.post(reverse("compute:compute-form"), data={})
        request.user = AnonymousUser()
        request.session = {"worksheet_preview_mode": True}

        response = ComputeExposure().post(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("compute:success-form-submission"))
        mock_service.compute_exposure_report.assert_called_once_with(
            user=request.user,
            save_to_database=False,
            report_description="Test Report",
            antenna_description="Test Antenna",
            antenna_gain=2.0,
            ground_reflection=True,
            effective_power=100.0,
            duty_factor=".2",
            transmit_time="2.0",
            receive_time="4.0",
            frequency_mode="0",
            frequency_position="1",
            frequency=14.0,
            operator_name="Test Operator",
            call_sign="KJ7ABC",
            email="test@example.com",
            include_calculations=True,
        )
        self.assertNotIn("record_id", request.session)
