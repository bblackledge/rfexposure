from django.urls import path, re_path

from .views.compute_exposure import ComputeExposure, TWC, SuccessFormSubmission
from .views.serve_pdf import ServePDF
from .views.dashboard.dashboard import DashboardView
from .views.dashboard.compute_help import ComputeHelpView
from .views.dashboard.delete_report import delete_report
from .views.dashboard.rerun_report import rerun_report, duplicate_report
from .views.dashboard.generate_stored_pdf import generate_stored_pdf

app_name = "compute"

urlpatterns = [
    re_path('compute-form', ComputeExposure.as_view(), name="compute-form"),
    re_path('twc', TWC.as_view(), name="twc"),
    re_path('success', SuccessFormSubmission.as_view(), name="success-form-submission"),
    path('media/pdfs/<str:filename>/', ServePDF.as_view(), name="serve-pdf"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('help/', ComputeHelpView.as_view(), name='compute-help'),
    path('report/<int:report_id>/rerun/', rerun_report, name='rerun_report'),
    path('report/<int:report_id>/duplicate/', duplicate_report, name='duplicate_report'),
    path('report/<int:report_id>/pdf/', generate_stored_pdf, name='generate_pdf'),
    path('report/<int:report_id>/delete/', delete_report, name='delete_report'),
    ]
