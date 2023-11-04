"""
URL configuration for automation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from appListNf import views
from django.conf.urls.static import static
# from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.mainRender, name='main.html'),
    path('api/', include('appNfPatos.urls')),
    path('api/', include('appListNf.urls')),
    # path('executar-script/', views.executar_script, name='executar_script'),
    # path('calcular/', views.calcular, name='calcular'),
    path('run_test_view/', views.run_test_view, name='run_test_view'),
    path('api/test', TemplateView.as_view(template_name='teste.html')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Adicionar Isto
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Adicionar Isto