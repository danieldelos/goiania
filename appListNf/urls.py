from django.urls import path
from appListNf.views import TableContractView
from .views import run_imprimir
from . import views

urlpatterns = [
    path('table', TableContractView.as_view()),
    path('creat_contract', views.ListNFServiceForm),
    path('upload/', views.upload_planilha, name='upload_planilha'),
    path('criar_pastas/', views.criar_pastas, name='criar_pastas'),
    path('imprimir/', run_imprimir, name='imprimir_notas'),
]
