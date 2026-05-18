from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from main import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('api/v1/clients/', include('apps.clients.urls', namespace='clients')),
    path('api/v1/policies/', include('apps.policies.urls', namespace='policies')),
    path('api/v1/payments/', include('apps.payments.urls', namespace='payments')),
    path('api/v1/documents/', include('apps.documents.urls', namespace='documents')),
    path('api/v1/notifications/', include('apps.notifications.urls', namespace='notifications')),
    path('api/v1/dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
