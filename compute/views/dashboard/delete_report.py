from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from ...models import RFReport


@login_required
@require_POST
def delete_report(request, report_id):
    report = get_object_or_404(RFReport, id=report_id, user=request.user)
    report.delete()
    return redirect("compute:dashboard")
