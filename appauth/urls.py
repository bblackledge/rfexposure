from django.urls import include, path

app_name = 'appauth'

urlpatterns = [
    path('', include('allauth.urls')),
]
