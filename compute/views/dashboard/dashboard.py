from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ...models import RFReport


class DashboardView(LoginRequiredMixin, ListView):
    model = RFReport
    template_name = 'dashboard.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return RFReport.objects.filter(user=self.request.user).order_by('-created_at')
