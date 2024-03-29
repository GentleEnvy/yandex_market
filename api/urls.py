import mimetypes

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

mimetypes.add_type('application/javascript', '.js')

urlpatterns = []

if settings.USE_BROWSABLE_API:
    urlpatterns += [
        path('__docs__/', SpectacularAPIView.as_view(), name='__docs__'),
        path('', SpectacularSwaggerView.as_view(url_name='__docs__')),
    ]

urlpatterns += [
    path('admin/', admin.site.urls),
    path('base/', include('app.base.urls')),
    path('users/', include('app.users.urls')),
    path('products/', include('app.products.urls')),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
