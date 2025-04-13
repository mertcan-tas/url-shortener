from django.contrib import admin
from django.urls import path,re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView,RedirectView
from django.views.static import serve

from api.views import redirect_to_original

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="API Docs",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    #path(r'', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('testing/', include('testing.urls')),
    path('prometheus/',include('django_prometheus.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='api-docs'),
    path('<str:short_code>/', redirect_to_original, name='redirect'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Url Shortener App'
admin.site.site_title = 'Url Shortener App'
