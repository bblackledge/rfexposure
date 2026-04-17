from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from compute.models import RFReport


class DashboardViewTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="dashboard-user",
            email="dashboard@example.com",
            password="password123",
        )
        self.other_user = user_model.objects.create_user(
            username="other-user",
            email="other@example.com",
            password="password123",
        )
        self.client.force_login(self.user)

        self.report = RFReport.objects.create(
            user=self.user,
            project_name="Project Alpha",
            parameters={
                "report_description": "Alpha Report",
                "antenna_description": "3-Element Yagi",
                "antenna_gain": 6.5,
                "ground_reflection": True,
                "effective_power": 100.0,
                "duty_factor": ".2",
                "transmit_time": "1.0",
                "receive_time": "2.0",
                "frequency_mode": "0",
                "frequency_position": "2",
                "frequency": 14.25,
                "include_calculations": True,
            },
        )
        RFReport.objects.create(
            user=self.other_user,
            project_name="Other Project",
            parameters={"report_description": "Hidden Report"},
        )

    def test_dashboard_renders_reports_in_vertical_list(self):
        response = self.client.get(reverse("compute:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Calculation Worksheet Report History")
        self.assertContains(response, "Alpha Report")
        self.assertContains(response, "3-Element Yagi")
        self.assertContains(response, "Download Exposure Report")
        self.assertContains(response, "Duplicate Report")
        self.assertContains(response, reverse("instructions"))
        self.assertContains(response, "Delete Report")
        self.assertContains(response, "Signed in as dashboard@example.com")
        self.assertNotContains(response, "Hidden Report")

    def test_delete_report_removes_report_for_current_user_only(self):
        response = self.client.post(reverse("compute:delete_report", args=[self.report.id]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(RFReport.objects.filter(id=self.report.id).exists())
        self.assertTrue(RFReport.objects.filter(project_name="Other Project").exists())
