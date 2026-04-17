from django.shortcuts import render, redirect
from django.views import View


class WorkflowChoice(View):
    """Intermediate page that splits cloud-saved and one-off worksheet flows."""

    template = "workflow_choice.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("compute:dashboard")
        return render(request, self.template)
