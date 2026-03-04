from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Bobbin_app import views

urlpatterns = [
path('admin/', admin.site.urls),


# ⭐ Home page MUST be mapped here
path('', views.home_view, name='home'),

# App urls
path('accounts/', include('django.contrib.auth.urls')),
path('', include('Bobbin_app.urls')),


]

# Media + Static (Render safe)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
