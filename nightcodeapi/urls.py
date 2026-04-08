"""
URL configuration for nightcodeapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def healthcheck(_request):
    return JsonResponse({'status': 'ok'}, status=200)


urlpatterns = [
    path('health/', healthcheck, name='healthcheck'),
    path('admin/', admin.site.urls),
    path('api/authusers/', include('authusers.urls')),
    path('api/authinventory/', include('authinventory.urls')),
    path('api/order/', include('order.urls')),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
