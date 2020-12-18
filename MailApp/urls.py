from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.main),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('subscription/', include('subscription.urls')),
    path('print-edition/', include('print_edition.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
