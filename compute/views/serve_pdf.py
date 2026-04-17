import os

from django.http import FileResponse, Http404
from django.views import View

from django.conf import settings


class ServePDF(View):
    """
    Download Complete - Serve PDF
    re_path('dc', DownloadComplete.as_view(), name="download-complete"),
    State: Unstable
    """

    def __init__(self, **kwargs):
        super(ServePDF, self).__init__(**kwargs)
        self.template = 'serve-pdf.html'
        self.error_message = ""
        self.debug = True

    def get(self, request, filename):
        """
        Download Complete - Serve PDF Template Display
        :param request: Request Object
        :param filename: str
        :returns: Render Download Complete Form
        Status: Stable
        """
        file_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        else:
            raise Http404("PDF file not found")
        # return render(request, self.template)
