from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from unittest.mock import ANY, patch


class ComputeFormSubmissionTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
        )
        self.client.force_login(self.user)

    @patch("compute.views.compute_exposure.ComputeExposureServices")
    def test_generate_report_posts_normalized_payload_to_service(self, mock_service_class):
        mock_service = mock_service_class.return_value
        mock_service.compute_exposure_report.return_value = (True, "report.pdf", 42)

        response = self.client.post(
            reverse("compute:compute-form"),
            data={
                "report_description": "Test Report",
                "name": "Test Operator",
                "call_sign": "KJ7ABC",
                "email": "test@example.com",
                "band_group": "MF/HF (1.8 MHz - 54.0 MHz)",
                "freq_pos": "Highest Frequency in Band",
                "antenna_description": "Test Antenna",
                "antenna_gain": "2.0",
                "ground_reflection": "on",
                "transmitter_power": "100",
                "duty_factor": "SSB (Conversational, No Speech Processing)  [20%]",
                "tx_time": "2",
                "rx_time": "4",
                "single_freq": "14.0",
                "include_calculations": "on",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("compute:success-form-submission"))
        mock_service.compute_exposure_report.assert_called_once_with(
            user=ANY,
            save_to_database=True,
            report_description="Test Report",
            antenna_description="Test Antenna",
            antenna_gain=2.0,
            ground_reflection=True,
            effective_power=100.0,
            duty_factor=".2",
            transmit_time="2.0",
            receive_time="4.0",
            frequency_mode="0",
            frequency_position="2",
            frequency=14.0,
            operator_name="Test Operator",
            call_sign="KJ7ABC",
            email="test@example.com",
            include_calculations=True,
        )
