from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('api/v1/clients/', include('apps.clients.urls', namespace='clients')),
    path('api/v1/policies/', include('apps.policies.urls', namespace='policies')),
]
