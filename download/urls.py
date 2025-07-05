from django.urls import path
from download import views


urlpatterns = [
    path("", views.index, name="index"),
    path("download/", views.download, name="download"),
    path('check-status/<str:filename>/', views.check_status, name='check_status'),
    path('index/', views.index)
]