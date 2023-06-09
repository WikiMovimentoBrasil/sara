from django.urls import path

from . import views

app_name = 'metrics'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('activities_plan', views.show_activities_plan, name='show_activities'),
    path('metrics', views.show_metrics, name='metrics'),
    path('metrics_per_project', views.show_metrics_per_project, name='per_project'),
]
