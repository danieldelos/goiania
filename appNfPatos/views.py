# from django.shortcuts import render
from cmath import e
import subprocess
from rest_framework.views import APIView, Response


# Create your views here.
def executar_teste():
    try:
        subprocess.run(['pytest', 'index.py'])
        return 'Comando executado com sucesso!'
    except Exception as e:
        return 'Erro ao executar o comando: ' + str(e)


class PersonView(APIView):
    def get(self, request):
        resultado = executar_teste()
        return Response({"resultado": resultado})