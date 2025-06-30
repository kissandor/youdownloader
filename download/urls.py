from django.urls import path
from download import views


urlpatterns = [
    path("", views.index, name="index"),
    path("download/", views.download, name="download"),
    path('test/', views.test_view),
    path('index/', views.index)
]