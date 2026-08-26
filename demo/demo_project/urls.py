"""demo_project URL Configuration."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from erp_framework.sites import erp_admin_site

urlpatterns = [
    # ERP Framework Admin Site
    path('erp-system/', erp_admin_site.urls),
    
    # Standard Django Admin
    path('admin/', admin.site.urls),
    
    # ERP Framework reporting URLs (if needed separately)
    # path('reporting/', include('slick_reporting.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
