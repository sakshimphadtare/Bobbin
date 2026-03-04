from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # App URLs (Main routing)
    path('', include('Bobbin_app.urls')),

    # Authentication URLs (login/logout/password reset)
    path('accounts/', include('django.contrib.auth.urls')),
]

# Media files (important for production)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Static files (Whitenoise will handle in production)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)