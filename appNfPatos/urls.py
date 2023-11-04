from django.urls import path
from appNfPatos.views import PersonView

urlpatterns = [
    path("persons/", PersonView.as_view()),
]