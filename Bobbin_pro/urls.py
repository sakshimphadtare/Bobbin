from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Bobbin_app.views import test_base_template




urlpatterns = [
    # 🔐 Admin Panel
    path('admin/', admin.site.urls),
    path('test/', test_base_template),  # ✅ this line

    # 🧵 Bobbin App URLs
    path('', include('Bobbin_app.urls')),

    # 🔐 Django Auth URLs (login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]

# 📂 Media & Static Files (Only in Development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
