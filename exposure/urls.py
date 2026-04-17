from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from .views.instructions import Instructions
from .views.workflow_choice import WorkflowChoice

urlpatterns = [
    path('admin/', admin.site.urls),
    path('compute/', include('compute.urls', namespace='compute')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('appauth.urls')),
    path('choose-workflow/', WorkflowChoice.as_view(), name="workflow-choice"),
    re_path('', Instructions.as_view(), name="instructions"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
