from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import TemplateView


@method_decorator(xframe_options_exempt, name="dispatch")
class ComputeHelpView(TemplateView):
    template_name = "compute_help.html"
