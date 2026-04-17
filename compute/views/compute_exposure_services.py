from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.template.loader import render_to_string
import logging
from icecream import ic
from ..models import ComputeExposureParameters, RFReport

from .computations import compute_report
from .pdf_utilities import PDFUtilities


class ComputeExposureServices:
    """ Compute RF Exposure Services """

    def __init__(self):
        self.report_template = 'exposure_report.html'
        self.cover_template = 'cover_page.html'
        self.computations_template = 'computation_debug.html'
        self.error = None
        self.error_message = ""
        self.logger = logging.getLogger("app.global")

    def compute_exposure_report(self, user=None, save_to_database=True, **kwargs):
        """
        Compute and Create Exposure Report
        :param kwargs: Form Data Passed As Keyword Arguments
        :return Operation Result and PDF output_pdf_filename
        :status Stable
        """

        try:
            pdu = PDFUtilities()
            form_data = kwargs
            record_id = 0

            ic(form_data)

            # === Pass RF Exposure Form Field Values and Complete All Report Computations ===
            param_dict = compute_report(**form_data)

            # === Generate HTML For Each Report Section ===
            rendered_report_html = render_to_string(self.report_template, {'param_dict': param_dict})
            rendered_cover_html = render_to_string(self.cover_template, {'data': param_dict})

            # Free users never receive the computation appendix, even if the form asked for it.
            include_calculations = bool(
                param_dict["include_calculations"] and user is not None and getattr(user, "is_authenticated", False)
            )

            # === User Selected on RF Exposure Form to Include Calculations ===
            if include_calculations:
                rendered_computation_report_html = render_to_string(self.computations_template, {'data': param_dict})
                next_page = '<pdf:nextpage />'
            else:
                rendered_computation_report_html = ''       # === DO NOT Include Calculation Pages ===
                next_page = ''                              # === DO NOT Create NEXT PAGE TAG and Empty Report Page ===

            # ic(param_dict["include_calculations"], rendered_computation_report_html)

            # === Append All Required HTML Report Pages as a Single Document ===
            combined_html_content = (
                rendered_cover_html +
                '<pdf:nextpage />' +
                rendered_report_html +
                next_page +
                rendered_computation_report_html
            )

            result, output_pdf_filename = pdu.create_pdf_report(combined_html_content)

            # === Save RF Exposure Parameters to Database ===
            if result and save_to_database:
                report_data = dict(param_dict)
                report_data['output_pdf_filename'] = output_pdf_filename
                report_data['results_list'] = [
                    {
                        key: value
                        for key, value in result_row.items()
                        if key not in {'c_intermediates', 'u_intermediates'}
                    }
                    for result_row in report_data.get('results_list', [])
                ]
                new_record = ComputeExposureParameters.objects.create(**form_data)
                record_id = new_record.id
                if user is not None and getattr(user, 'is_authenticated', False):
                    RFReport.objects.create(
                        user=user,
                        project_name=form_data.get('report_description') or 'Untitled Project',
                        parameters=report_data,
                    )

            return result, output_pdf_filename, record_id

        except KeyError as e:
            self.error_message = f"Key error: {e}"
            self.logger.exception("compute_exposure_report failed with KeyError")
            return False, None, 0
        except TypeError as e:
            self.error_message = f"Type error: {e}"
            self.logger.exception("compute_exposure_report failed with TypeError")
            return False, None, 0
        except TemplateDoesNotExist as e:
            self.error_message = f"Template does not exist: {e}"
            self.logger.exception("compute_exposure_report failed with missing template")
            return False, None, 0
        except TemplateSyntaxError as e:
            self.error_message = f"Template syntax error: {e}"
            self.logger.exception("compute_exposure_report failed with template syntax error")
            return False, None, 0
        except OSError as e:
            self.error_message = f"OS error: {e}"
            self.logger.exception("compute_exposure_report failed with OSError")
            return False, None, 0
        except ValueError as e:
            self.error_message = f"Value error: {e}"
            self.logger.exception("compute_exposure_report failed with ValueError")
            return False, None, 0
        except Exception as e:
            self.error_message = f"An unexpected error occurred: {e}"
            self.logger.exception("compute_exposure_report failed with unexpected error")
            return False, None, 0
