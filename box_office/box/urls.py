from django.urls import path
from . import views

urlpatterns = [
    path('daily', views.Daily_Box.as_view())
]
