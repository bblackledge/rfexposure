from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

from ..compute_exposure_services import ComputeExposureServices
from ...models import RFReport


def _worksheet_data_from_report(report):
    return {
        key: value
        for key, value in report.parameters.items()
        if key in {
            "report_description",
            "antenna_description",
            "antenna_gain",
            "ground_reflection",
            "effective_power",
            "duty_factor",
            "transmit_time",
            "receive_time",
            "frequency_mode",
            "frequency_position",
            "frequency",
            "operator_name",
            "call_sign",
            "email",
            "include_calculations",
        }
    }


@login_required
def rerun_report(request, report_id):
    report = get_object_or_404(RFReport, id=report_id, user=request.user)
    worksheet_data = _worksheet_data_from_report(report)
    compute_services = ComputeExposureServices()
    result, output_pdf_filename, record_id = compute_services.compute_exposure_report(
        user=request.user,
        save_to_database=False,
        **worksheet_data,
    )

    if result:
        request.session["output_pdf_filename"] = output_pdf_filename
        request.session["MEDIA_URL"] = settings.MEDIA_URL
        request.session.pop("record_id", None)
        request.session.pop("worksheet_preview_mode", None)
        request.session.pop("worksheet_report_id", None)
        request.session.pop("worksheet_data", None)
        return redirect("compute:success-form-submission")

    return JsonResponse(
        {
            "error": "Failed to generate report",
            "details": compute_services.error_message,
        },
        status=500,
    )


@login_required
def duplicate_report(request, report_id):
    report = get_object_or_404(RFReport, id=report_id, user=request.user)
    request.session["worksheet_data"] = _worksheet_data_from_report(report)
    request.session.pop("worksheet_preview_mode", None)
    request.session["worksheet_report_id"] = report.id
    return redirect('compute:compute-form')
