from django.contrib import admin
from django.urls import path, include

from . import views

app_name='report'

urlpatterns = [
    path('', views.EntriesView.as_view(), name='entries'),
    path('entrie/<username>/<int:pk>', views.EntriesDetailView.as_view(), name='entries-detail'),
    path('entrie/stats/', views.EntriesStatsView.as_view(), name='entries-stats'),
    path('entrie/create', views.EntriesCreateView.as_view(), name='entries-create'),
    path('entrie/<int:pk>/delete', views.EntriesDeleteView.as_view(), name='entries-delete'),
]
