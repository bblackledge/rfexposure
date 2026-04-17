from django.test import TestCase

from compute.views.pdf_utilities import PDFUtilities


class PDFUtilitiesTests(TestCase):
    def test_link_callback_resolves_static_logo(self):
        resolved_path = PDFUtilities.link_callback("/static/assets/img/logo_maroon.png", None)

        self.assertTrue(resolved_path.endswith("assets/img/logo_maroon.png"))
