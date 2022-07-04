"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('ObjectA.urls'), name="obj-a"),
    path('obj-a/', include('ObjectA.urls')),
    path('obj-b/', include('ObjectB.urls')),
    path('obj-c/', include('ObjectC.urls')),
    path('obj-abc/', include('ObjectABC.urls')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('image/favicon.ico')))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
