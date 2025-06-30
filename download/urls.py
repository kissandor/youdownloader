from django.urls import path
from download import views


urlpatterns = [
    path("", views.home, name="home"),
    path('test/', views.test_view),
    path('index/', views.index)
]