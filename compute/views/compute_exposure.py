import time
import logging

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .compute_exposure_services import ComputeExposureServices
from .compute_form_services import ComputeFormServices
from ..forms.form import ComputeExposureParametersForm
from django.conf import settings
from icecream import ic


class ComputeExposure(View):
    """
    Display Exposure Compute Data Entry Form and Process POST Valid Form Results
    re_path('compute-form', ComputeExposure.as_view(), name="compute-form"),
    State: Unstable
    """

    def __init__(self, **kwargs):
        super(ComputeExposure, self).__init__(**kwargs)
        self.template = 'compute_form_new.html'
        self.form = ComputeExposureParametersForm
        self.form_services = ComputeFormServices()
        self.error_message = ""
        self.debug = True
        self.logger = logging.getLogger("app.global")

    def get(self, request):
        """
        Render Compute Exposure Form
        :param request: Request Object
        :returns: Render Compute Exposure Form
        Status: Stable
        """

        # == Check for Existing Record ID in Session ===
        # record_id = request.session.get('record_id')
        #
        # # === Record ID Found ===
        # if record_id:
        #     record = get_object_or_404(ComputeExposureParameters, id=record_id)
        # else:
        #     record = None

        # === Load Existing Record Data or Create Blank Form ===
        # if record:
        #     form = self.form(instance=record)
        #     # print(form)
        # else:
        #     form = self.form()

        initial_data = request.session.pop("worksheet_data", None)
        if not initial_data:
            request.session.pop("worksheet_preview_mode", None)
            request.session.pop("worksheet_report_id", None)
        form = self.form(initial=initial_data) if initial_data else self.form()
        return render(request, self.template, {'form': form})

    def post(self, request):
        """ Process Compute Exposure Form Post """

        # === Normalize custom HTML field names into the legacy service payload ===
        normalized_post = self.form_services.normalize_post_data(request.POST)
        form = self.form(normalized_post)
        if form.is_valid():
            compute_services = ComputeExposureServices()
            preview_mode = bool(request.session.get("worksheet_preview_mode"))
            result, output_pdf_filename, record_id = compute_services.compute_exposure_report(
                user=request.user,
                save_to_database=not preview_mode,
                **form.cleaned_data
            )

            if result:
                ic('compute:dashboard', result, output_pdf_filename, record_id)

                request.session['output_pdf_filename'] = output_pdf_filename
                request.session['MEDIA_URL'] = settings.MEDIA_URL
                if record_id:
                    request.session['record_id'] = record_id
                else:
                    request.session.pop('record_id', None)
                if preview_mode:
                    request.session.pop("worksheet_preview_mode", None)
                    request.session.pop("worksheet_report_id", None)

                return redirect('compute:success-form-submission')
            else:
                ic(result, output_pdf_filename, compute_services.error_message)
                self.logger.error(
                    "Generate report failed: %s",
                    compute_services.error_message or "no error message returned",
                )
                return JsonResponse({
                    "error": "Failed to generate report",
                    "details": compute_services.error_message,
                }, status=500)

        # === Invalid Form - Return Original Post Data ===
        self.logger.error("Compute form validation failed: %s", form.errors.as_json())
        return render(request, self.template, {'form': form})


class TWC(View):

    def __init__(self, **kwargs):
        super(TWC, self).__init__(**kwargs)
        self.template = 'twc.html'

    def get(self, request):
        from redis import Redis
        from rq import Queue

        q = Queue(connection=Redis())

        from .twc_services import count_words_at_url

        job = q.enqueue(count_words_at_url)
        while True:
            job.refresh()  # Refresh job status
            if job.is_finished:
                print("Job completed successfully!")
                break
            elif job.is_failed:
                print("Job failed!")
                break
            else:
                print("Job still running...")

            time.sleep(1)

        return render(request, self.template, {'count': job})


class SuccessFormSubmission(View):
    """ Success Page Displayed After Successful Computation and PDF Report Generation """

    def __init__(self, **kwargs):
        super(SuccessFormSubmission, self).__init__(**kwargs)
        self.template = 'success-form-submission.html'

    def get(self, request):

        # === Extract Previously Stored Session Data ===
        output_pdf_filename = request.session.get('output_pdf_filename')
        media_url = request.session.get('MEDIA_URL')
        record_id = request.session.get('record_id')

        # === Clear the Session Data After Retrieving It ===
        request.session.pop('output_pdf_filename', None)
        request.session.pop('MEDIA_URL', None)
        # request.session.pop('record_id', None)

        # === If We Loaded Data, Pass as JSON Context ===
        if output_pdf_filename and media_url:
            context = {
                'pdf_filename': output_pdf_filename,
                'media_url': media_url,
                'record_id': record_id,
                'DEBUG': settings.DEBUG,
            }
            return render(request, self.template, context)
        else:
            # === Invalid Data Passed, Report Error On Page ===
            return render(request, self.template, {"error": "Missing Session Data"})
