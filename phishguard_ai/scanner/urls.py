from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("scan/", views.scan, name="scan"),
    path("result/<int:pk>/", views.result, name="result"),
    path("about/", views.about, name="about"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("api-status/", views.api_status, name="api_status"),
]
