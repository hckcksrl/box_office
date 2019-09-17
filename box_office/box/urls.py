from django.urls import path
from . import views

urlpatterns = [
    path('daily', views.DailyBox.as_view()),
    path('search', views.MovieSearch.as_view()),
    path('weekly', views.WeeklyBox.as_view())
]
