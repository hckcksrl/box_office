from django.urls import path
from . import views

urlpatterns = [
    path('daily', views.Daily_Box.as_view()),
    path('search', views.Movie_Search.as_view()),
    path('weekly', views.Weekly_Box.as_view())
]
