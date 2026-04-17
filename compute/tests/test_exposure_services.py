from django.contrib.auth import get_user_model
from django.test import TestCase
from unittest.mock import patch, MagicMock
from ..views.compute_exposure_services import ComputeExposureServices
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from compute.views.computations import compute_report
from compute.views.pdf_utilities import PDFUtilities
from compute.models import ComputeExposureParameters, RFReport


class ComputeExposureServicesTests(TestCase):

    def setUp(self):
        # Create an instance of the service
        self.service = ComputeExposureServices()

        # Sample kwargs to pass as form data
        self.sample_kwargs = {
            'report_description': 'Test Report',
            'antenna_description': 'Test Antenna',
            'effective_power': 100.0,  # watts
            'antenna_gain': 2.0,  # dBi
            'frequency_mode': 0,
            'frequency_position': 1,
            'frequency': 14.0,  # MHz (in 20 meters band)
            'ground_reflection': True,
            'duty_factor': 0.5,  # 50% duty cycle
            'transmit_time': 2.0,  # minutes
            'receive_time': 4.0,  # minutes,
            'include_calculations': True  # Whether to include calculations in the report
        }

    @patch('compute.views.compute_exposure_services.compute_report')
    @patch('compute.views.compute_exposure_services.render_to_string')
    @patch('compute.views.pdf_utilities.PDFUtilities.create_pdf_report')
    def test_compute_exposure_report_success(self, mock_create_pdf_report, mock_render_to_string, mock_compute_report):
        """Test successful PDF generation with all templates and report data"""

        # Mock the report computation and PDF creation
        mock_compute_report.return_value = {'include_calculations': True, **self.sample_kwargs}
        mock_render_to_string.side_effect = ['<html>Cover</html>', '<html>Report</html>', '<html>Computation</html>']
        mock_create_pdf_report.return_value = (True, 'test_report.pdf')
        mock_user = get_user_model().objects.create_user(
            username="report-user",
            email="report-user@example.com",
            password="password123",
        )

        # Call the method
        result, output_pdf_filename, record_id = self.service.compute_exposure_report(user=mock_user, **self.sample_kwargs)

        # Assert the method returns successful result and PDF filename
        self.assertTrue(result)
        self.assertEqual(output_pdf_filename, 'test_report.pdf')
        self.assertEqual(record_id, 1)

        # Output the actual calls for render_to_string
        print("Actual calls made to render_to_string:", mock_render_to_string.call_args_list)

        # Verify that the correct templates were rendered
        mock_render_to_string.assert_any_call(self.service.report_template, {'param_dict': mock_compute_report.return_value})
        mock_render_to_string.assert_any_call('cover_page.html', {'data': mock_compute_report.return_value})
        mock_render_to_string.assert_any_call(self.service.computations_template, {'data': mock_compute_report.return_value})
        mock_create_pdf_report.assert_called_once()

    @patch('compute.views.compute_exposure_services.compute_report')
    @patch('compute.views.compute_exposure_services.render_to_string')
    @patch('compute.views.pdf_utilities.PDFUtilities.create_pdf_report')
    def test_compute_exposure_report_no_calculations(self, mock_create_pdf_report, mock_render_to_string, mock_compute_report):
        """Test report generation without calculations"""



        # Mock the report computation (with include_calculations=False) and PDF creation
        mock_compute_report.return_value = {**self.sample_kwargs, 'include_calculations': False}
        mock_render_to_string.side_effect = ['<html>Cover</html>', '<html>Report</html>']
        mock_create_pdf_report.return_value = (True, 'test_report.pdf')

        # Call the method
        result, output_pdf_filename, record_id = self.service.compute_exposure_report(**self.sample_kwargs)

        # Assert the method returns successful result and PDF filename
        self.assertTrue(result)
        self.assertEqual(output_pdf_filename, 'test_report.pdf')
        self.assertEqual(record_id, 1)

        # Output the actual calls for render_to_string
        print("Actual calls made to render_to_string:", mock_render_to_string.call_args_list)

        # Verify that the computations template is not rendered
        mock_render_to_string.assert_any_call(self.service.report_template, {'param_dict': mock_compute_report.return_value})
        mock_render_to_string.assert_any_call(self.service.cover_template, {'data': mock_compute_report.return_value})
        self.assertNotIn(
            self.service.computations_template,
            [call[0][0] for call in mock_render_to_string.call_args_list],
        )
        mock_create_pdf_report.assert_called_once()

    @patch('compute.views.compute_exposure_services.compute_report')
    @patch('compute.views.compute_exposure_services.render_to_string')
    @patch('compute.views.pdf_utilities.PDFUtilities.create_pdf_report')
    def test_compute_exposure_report_anonymous_user_skips_calculations(
        self,
        mock_create_pdf_report,
        mock_render_to_string,
        mock_compute_report,
    ):
        """Anonymous users should never get the computation appendix."""

        mock_compute_report.return_value = {'include_calculations': True, **self.sample_kwargs}
        mock_render_to_string.side_effect = ['<html>Cover</html>', '<html>Report</html>']
        mock_create_pdf_report.return_value = (True, 'test_report.pdf')

        result, output_pdf_filename, record_id = self.service.compute_exposure_report(**self.sample_kwargs)

        self.assertTrue(result)
        self.assertEqual(output_pdf_filename, 'test_report.pdf')
        self.assertEqual(record_id, 1)
        self.assertNotIn(
            self.service.computations_template,
            [call[0][0] for call in mock_render_to_string.call_args_list],
        )
        mock_create_pdf_report.assert_called_once()

    @patch('compute.views.compute_exposure_services.compute_report')
    @patch('compute.views.compute_exposure_services.render_to_string')
    @patch('compute.views.pdf_utilities.PDFUtilities.create_pdf_report')
    def test_compute_exposure_report_preview_skips_database_writes(
        self,
        mock_create_pdf_report,
        mock_render_to_string,
        mock_compute_report,
    ):
        """Preview mode should generate the PDF without creating saved report rows."""

        mock_compute_report.return_value = {'include_calculations': True, **self.sample_kwargs}
        mock_render_to_string.side_effect = ['<html>Cover</html>', '<html>Report</html>', '<html>Computation</html>']
        mock_create_pdf_report.return_value = (True, 'preview_report.pdf')
        mock_user = get_user_model().objects.create_user(
            username="preview-user",
            email="preview-user@example.com",
            password="password123",
        )

        result, output_pdf_filename, record_id = self.service.compute_exposure_report(
            user=mock_user,
            save_to_database=False,
            **self.sample_kwargs,
        )

        self.assertTrue(result)
        self.assertEqual(output_pdf_filename, 'preview_report.pdf')
        self.assertEqual(record_id, 0)
        self.assertEqual(mock_create_pdf_report.call_count, 1)
        self.assertEqual(mock_render_to_string.call_count, 3)
        self.assertEqual(ComputeExposureParameters.objects.count(), 0)
        self.assertEqual(RFReport.objects.filter(user=mock_user).count(), 0)

    @patch('compute.views.compute_exposure_services.compute_report')
    @patch('compute.views.compute_exposure_services.render_to_string')
    @patch('compute.views.pdf_utilities.PDFUtilities.create_pdf_report')
    def test_compute_exposure_report_template_does_not_exist(self, mock_create_pdf_report, mock_render_to_string, mock_compute_report):
        """Test handling of TemplateDoesNotExist error"""

        # Mock the report computation and template rendering to raise TemplateDoesNotExist
        mock_compute_report.return_value = {'include_calculations': True, **self.sample_kwargs}
        mock_render_to_string.side_effect = TemplateDoesNotExist('some_template.html')

        # Call the method
        result, output_pdf_filename, record_id = self.service.compute_exposure_report(**self.sample_kwargs)

        # Assert the method returns a failure and no PDF filename
        self.assertFalse(result)
        self.assertIsNone(output_pdf_filename)
        self.assertEqual(record_id, 0)
        self.assertEqual(self.service.error_message, "Template does not exist: some_template.html")

    @patch('compute.views.compute_exposure_services.compute_report')
    @patch('compute.views.compute_exposure_services.render_to_string')
    @patch('compute.views.pdf_utilities.PDFUtilities.create_pdf_report')
    def test_compute_exposure_report_template_syntax_error(self, mock_create_pdf_report, mock_render_to_string, mock_compute_report):
        """Test handling of TemplateSyntaxError"""

        # Mock the report computation and template rendering to raise TemplateSyntaxError
        mock_compute_report.return_value = {'include_calculations': True, **self.sample_kwargs}
        mock_render_to_string.side_effect = TemplateSyntaxError('Syntax error in template')

        # Call the method
        result, output_pdf_filename, record_id = self.service.compute_exposure_report(**self.sample_kwargs)

        # Assert the method returns a failure and no PDF filename
        self.assertFalse(result)
        self.assertIsNone(output_pdf_filename)
        self.assertEqual(record_id, 0)
        self.assertEqual(self.service.error_message, "Template syntax error: Syntax error in template")

    @patch('compute.views.compute_exposure_services.compute_report')
    @patch('compute.views.compute_exposure_services.render_to_string')
    @patch('compute.views.pdf_utilities.PDFUtilities.create_pdf_report')
    def test_compute_exposure_report_os_error(self, mock_create_pdf_report, mock_render_to_string, mock_compute_report):
        """Test handling of OSError"""

        # Mock the report computation and PDF creation to raise OSError
        mock_compute_report.return_value = {'include_calculations': True, **self.sample_kwargs}
        mock_render_to_string.side_effect = ['<html>Cover</html>', '<html>Report</html>', '<html>Computation</html>']
        mock_create_pdf_report.side_effect = OSError('File system error')

        # Call the method
        result, output_pdf_filename, record_id = self.service.compute_exposure_report(**self.sample_kwargs)

        # Assert the method returns a failure and no PDF filename
        self.assertFalse(result)
        self.assertIsNone(output_pdf_filename)
        self.assertEqual(record_id, 0)
        self.assertEqual(self.service.error_message, "OS error: File system error")

    @patch('compute.views.compute_exposure_services.compute_report')
    @patch('compute.views.compute_exposure_services.render_to_string')
    @patch('compute.views.pdf_utilities.PDFUtilities.create_pdf_report')
    def test_compute_exposure_report_value_error(self, mock_create_pdf_report, mock_render_to_string, mock_compute_report):
        """Test handling of ValueError"""

        # Mock the report computation and PDF creation to raise ValueError
        mock_compute_report.return_value = {'include_calculations': True, **self.sample_kwargs}
        mock_render_to_string.side_effect = ['<html>Cover</html>', '<html>Report</html>', '<html>Computation</html>']
        mock_create_pdf_report.side_effect = ValueError('Invalid value passed')

        # Call the method
        result, output_pdf_filename, record_id = self.service.compute_exposure_report(**self.sample_kwargs)

        # Assert the method returns a failure and no PDF filename
        self.assertFalse(result)
        self.assertIsNone(output_pdf_filename)
        self.assertEqual(record_id, 0)
        self.assertEqual(self.service.error_message, "Value error: Invalid value passed")

    @patch('compute.views.compute_exposure_services.compute_report')
    @patch('compute.views.compute_exposure_services.render_to_string')
    @patch('compute.views.pdf_utilities.PDFUtilities.create_pdf_report')
    def test_compute_exposure_report_unexpected_error(self, mock_create_pdf_report, mock_render_to_string, mock_compute_report):
        """Test handling of an unexpected error"""

        # Mock the report computation and PDF creation to raise an unexpected exception
        mock_compute_report.return_value = {'include_calculations': True, **self.sample_kwargs}
        mock_render_to_string.side_effect = ['<html>Cover</html>', '<html>Report</html>', '<html>Computation</html>']
        mock_create_pdf_report.side_effect = Exception('Unexpected error occurred')

        # Call the method
        result, output_pdf_filename, record_id = self.service.compute_exposure_report(**self.sample_kwargs)

        # Assert the method returns a failure and no PDF filename
        self.assertFalse(result)
        self.assertIsNone(output_pdf_filename)
        self.assertEqual(record_id, 0)
        self.assertEqual(self.service.error_message, "An unexpected error occurred: Unexpected error occurred")
