from django.db import models


# Create your models here.
class ListNFService(models.Model):
    empresa = models.CharField(max_length=50, null=True)
    Numero_NF = models.IntegerField(null=True)
    cnpj_cpf = models.CharField(max_length=14, null=True)
    n_cnpj_cpf = models.CharField(max_length=14, null=True)
    nome = models.CharField(max_length=120, null=True)
    endereco = models.CharField(max_length=120, null=True)
    numero = models.CharField(max_length=120, null=True)
    complemento = models.CharField(max_length=120, null=True)
    bairro = models.CharField(max_length=120, null=True)
    cep = models.CharField(max_length=50, null=True)
    cod_mun_prestador = models.CharField(max_length=120, null=True)
    cod_mun_tomador = models.CharField(max_length=120, null=True)
    atividade_economica = models.CharField(max_length=120, default="semTexto")
    discrimicacao = models.CharField(max_length=120, default="semTexto")
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    checkNf = models.BooleanField(default=False)
    pasta = models.CharField(max_length=120)
    link_nfse = models.CharField(max_length=120)
