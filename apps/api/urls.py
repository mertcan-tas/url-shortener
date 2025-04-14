# api/urls.py

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('urls/create/', views.CreateShortURLView.as_view(), name='url-create'),
    path('urls/', views.ListShortURLsView.as_view(), name='url-list'),
    path('urls/my/', views.MyShortURLsView.as_view(), name='my-urls'),
    path('urls/<int:id>/', views.ShortURLDetailView.as_view(), name='url-detail'),
    path('urls/<int:id>/update/', views.UpdateShortURLView.as_view(), name='url-update'),
    path('urls/<int:id>/delete/', views.DeleteShortURLView.as_view(), name='url-delete'),
    path('urls/stats/', views.URLStatsView.as_view(), name='url-stats'),
    path('urls/<int:id>/stats/', views.URLDetailStatsView.as_view(), name='url-detail-stats'),
    
    
    # Dashboard Endpoint'leri
    path('dashboard/', views.dashboard_stats, name='dashboard-stats'),
    
    # Sağlık Kontrolü Endpoint'i
    path('health/', views.health_check, name='health-check'),
    
    # Ana URL Kısaltma Endpoint'i (redirector)
    # Bu ana urls.py'a eklenmelidir, çünkü kök URL'de olmalıdır
]
