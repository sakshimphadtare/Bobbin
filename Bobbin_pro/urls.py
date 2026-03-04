from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Bobbin App Routes
    path('', include('Bobbin_app.urls')),

    # Authentication Routes
    path('accounts/', include('django.contrib.auth.urls')),

]

# ✅ Serve media files (works in production with Whitenoise)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)