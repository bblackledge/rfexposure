import os

from django.http import FileResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from ...models import RFReport


@login_required
def generate_stored_pdf(request, report_id):
    # Security: Ensure users can only download their own reports
    report = get_object_or_404(RFReport, id=report_id, user=request.user)

    output_pdf_filename = report.parameters.get('output_pdf_filename')
    if not output_pdf_filename:
        raise Http404("Saved PDF file not found for this report")

    file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', output_pdf_filename)
    if not os.path.exists(file_path):
        raise Http404("PDF file not found")

    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
