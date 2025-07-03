from django.urls import path
from download import views


urlpatterns = [
    path("", views.index, name="index"),
    path("download/", views.download, name="download"),
    path('index/', views.index)
]