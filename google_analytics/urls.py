from django.urls import path

from . import views

app_name = "analytics"
urlpatterns = [
    path("", views.home, name="home"),
    path("analyze/", views.analyze, name="analyze"),
    path(
        "download/<str:filename>/<str:start>/<str:end>", views.download, name="download"
    ),
]
