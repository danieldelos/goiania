from django import forms
from .models import ListNFService

class ListNFServiceForm(forms.ModelForm):
    class Meta:
        model = ListNFService
        fields = '__all__'
        
        
class PlanilhaForm(forms.Form):
    arquivo = forms.FileField()        