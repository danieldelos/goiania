from gettext import translation
from lib2to3.pgen2 import driver
import traceback
from django.shortcuts import redirect, render
from django.urls import reverse
from django.apps import apps
from django.contrib import messages
from django.test import RequestFactory
from rest_framework.views import APIView, Response
import subprocess
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from appListNf.forms import ListNFServiceForm, PlanilhaForm
from appListNf.models import ListNFService
from django.db import transaction
import ipdb
import pytest
import time
import json
import os
import requests
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from weasyprint import HTML
from time import sleep
import pandas as pd
from selenium.webdriver import ActionChains

def mainRender(request):
    clients = ListNFService.objects.all()
    Model = apps.get_model("appListNf", "ListNFService")
    column_names = [field.name for field in Model._meta.get_fields()]
    selected_data = ListNFService.objects.values_list(
        "id",
        "empresa",
        "Numero_NF",
        "cnpj_cpf",
        "n_cnpj_cpf",
        "nome",
        "endereco",
        "numero",
        "complemento",
        "bairro",
        "cep",
        "cod_mun_prestador",
        "cod_mun_tomador",
        "atividade_economica",
        "discrimicacao",
        "valor",
        "checkNf",
        "pasta",
        "link_nfse",
    )

    return render(
        request,
        "dashboard.html",
        {
            "column": column_names,
            "selected_data": selected_data,
        },
    )

def criar_listnf(request):
    if request.method == "POST":
        form = ListNFServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("nome_da_rota")
    else:
        form = ListNFServiceForm()

    return render(request, "dashboard.html", {"form": form})


# Create your views here.
class TableContractView(APIView):
    def get(self, request):
        return Response({"msg": "rota get"})


def upload_planilha(request):
    if request.method == "POST":
        form = PlanilhaForm(request.POST, request.FILES)
        if form.is_valid():
            planilha = form.cleaned_data["arquivo"]
            df = pd.read_excel(planilha)
            max_numero_nf = request.POST.get("input_value", "")
            sequencia = int(max_numero_nf)
            if sequencia is None:
                sequencia = 0
            ListNFService.objects.all().delete()  # Remove registros existentes
            nf_services = []
            for _, row in df.iterrows():
                sequencia += 1  # Incrementar o valor para o próximo número NF
                nf_service = ListNFService(
                    empresa=row["empresa"],
                    Numero_NF=sequencia,  # Inserir o novo valor na coluna Numero_NF
                    cnpj_cpf=row["cnpj_cpf"],
                    n_cnpj_cpf=row["n_cnpj_cpf"],
                    nome=row["nome"],
                    endereco=row["endereco"],
                    numero=row["numero"],
                    complemento=row["complemento"],
                    bairro=row["bairro"],
                    cep=row["cep"],
                    cod_mun_prestador=row["cod_mun_prestador"],
                    cod_mun_tomador=row["cod_mun_tomador"],
                    atividade_economica=row["atividade_economica"],
                    discrimicacao=row["discrimicacao"],
                    valor=row["valor"],
                    checkNf=row["checkNf"],
                    pasta=row["pasta"],
                    link_nfse=row["link_nfse"],
                )
                nf_services.append(nf_service)
            ListNFService.objects.bulk_create(nf_services)
            criar_pastas(request)
            return render(request, "upload_sucesso.html")
    else:
        form = PlanilhaForm()
    return render(request, "upload_planilha.html", {"form": form})


def criar_pastas(request):
    # Obtenha todos os objetos ListNFService
    servicos = ListNFService.objects.all()

    # Diretório principal no seu desktop
    dir_principal = os.path.join(os.path.expanduser("~"), "Desktop", "notas")

    # Crie o diretório principal se ele ainda não existir
    if not os.path.exists(dir_principal):
        os.makedirs(dir_principal)

    # Para cada serviço em servicos
    for servico in servicos:
        # Obtenha o nome da pasta do serviço atual
        nome_pasta = servico.pasta

        # Crie um novo diretório para este serviço no diretório principal
        novo_dir = os.path.join(dir_principal, nome_pasta)

        # Crie o diretório se ele ainda não existir
        if not os.path.exists(novo_dir):
            os.makedirs(novo_dir)
    return HttpResponse("Pastas criadas com sucesso!")


def run_test_view(request):
    # Cria uma instância da classe de teste
    test_class_instance = Create_document()
    # Selecion o browser
    # chrome_options = Options()
    # chrome_options.add_experimental_option(
    #     "prefs",
    #     {
    #         "download.default_directory": os.path.expanduser(
    #             "~/Desktop/notas_faturamento"
    #         ),
    #         "download.prompt_for_download": False,
    #         "download.directory_upgrade": True,
    #         "safebrowsing.enabled": True,
    #     },
    # )
    # test_class_instance.driver = webdriver.Chrome(options=chrome_options)
    
    firefox_options = FirefoxOptions()
    test_class_instance.driver = webdriver.Firefox(options=firefox_options)
    firefox_options = FirefoxOptions()
    firefox_options.set_preference(
        "browser.download.dir",
        os.path.expanduser("~/Desktop/notas_faturamento"),
    )
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
    firefox_options.set_preference("pdfjs.disabled", True)
    firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    
    # edge_options = webdriver.EdgeOptions()
    # Use a linha abaixo se estiver usando a versão baseada em Chromium do Edge
    # edge_options.use_chromium = True  
    
    # Definir o diretório de download (isso pode ser um pouco diferente do Firefox e Chrome)
    # Você pode precisar testar e ajustar de acordo com sua necessidade específica e a versão do Edge
    prefs = {
        "download.default_directory": os.path.expanduser("~/Desktop/notas_faturamento"),
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True,
    }
    # edge_options.add_experimental_option("prefs", prefs)

    # test_class_instance.driver = webdriver.Edge(options=edge_options)
    
    test_class_instance.test_emitirnfse()
    # Encerra a instância do driver
    test_class_instance.driver.quit()
    # Retorna uma resposta HTTP para indicar que o teste foi concluído
    return HttpResponse("Notas emitidas com sucesso!")


class Create_document(TestCase):
    def setUp(self):
        self.vars = {}

    def wait_for_window(self, timeout=2):
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def test_emitirnfse(self):
        empresa_list = ListNFService.objects.values_list("empresa", flat=True)
        cnpj_cpf_list = ListNFService.objects.values_list("cnpj_cpf", flat=True)
        n_cnpj_cpf_list = ListNFService.objects.values_list("n_cnpj_cpf", flat=True)
        nome_list = ListNFService.objects.values_list("nome", flat=True)
        endereco_list = ListNFService.objects.values_list("endereco", flat=True)
        numero_list = ListNFService.objects.values_list("numero", flat=True)
        complemento_list = ListNFService.objects.values_list("complemento", flat=True)
        bairro_list = ListNFService.objects.values_list("bairro", flat=True)
        cep_list = ListNFService.objects.values_list("cep", flat=True)
        cod_mun_prestador_list = ListNFService.objects.values_list("cod_mun_prestador", flat=True)
        cod_mun_tomador_list = ListNFService.objects.values_list("cod_mun_tomador", flat=True)
        atividade_economica_list = ListNFService.objects.values_list("atividade_economica", flat=True)
        discrimicacao_list = ListNFService.objects.values_list("discrimicacao", flat=True)
        valor_list = ListNFService.objects.values_list("valor", flat=True)
        check_list = ListNFService.objects.values_list("checkNf", flat=True)
        pasta_list = ListNFService.objects.values_list("pasta", flat=True)
        link_nfse_list = ListNFService.objects.values_list("link_nfse", flat=True)
        wait = WebDriverWait(self.driver, 15)
        self.driver.get("https://www10.goiania.go.gov.br/Internet/Login.aspx?OriginalURL=https%3a%2f%2fwww10.goiania.go.gov.br%2fsicaeportal%2fHomePage.aspx")
        self.driver.find_element(By.ID, "wt17_wtMainContent_wtUserNameInput").click()
        self.driver.find_element(By.ID, "wt17_wtMainContent_wtUserNameInput").send_keys("01237041112")
        self.driver.find_element(By.ID, "wt17_wtMainContent_wtPasswordInput").click()
        self.driver.find_element(By.ID, "wt17_wtMainContent_wtPasswordInput").send_keys("Pf050786")
        self.driver.find_element(By.ID, "wt17_wtMainContent_wt30").click()
        wait.until(EC.frame_to_be_available_and_switch_to_it(0))
        entrar = wait.until(EC.visibility_of_element_located((By.ID,"WebPatterns_wt8_block_wtMainContent_wt6",)))
        entrar.click()
        self.driver.switch_to.default_content()
        self.driver.find_element(By.ID, "select2-chosen-1").click()
        select = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#s2id_autogen1_search",)))
        # select.send_keys("CAE : 4832817 - DR PAULO FERNANDO NUTROLOGIA LTDA")
        select.send_keys("CAE : 6047106 - NUCLEO DRPAULO FERNANDO LTDA")
        option = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"[id^='select2-result-label-'] > span")))
        option.click()
        btn_nfse = wait.until(EC.visibility_of_element_located((By.XPATH,'//span[contains(text(), "NF Eletrônica")]')))
        btn_nfse.click()
        entrar_nfse = wait.until(EC.visibility_of_element_located((By.XPATH,'//span[contains(text(), "Entrar")]')))
        entrar_nfse.click()
        # 1. Armazene a handle da janela principal
        main_window_handle = self.driver.current_window_handle
        # 2. Espere até que uma nova janela esteja disponível
        wait.until(EC.number_of_windows_to_be(2))
        new_window_handle = [window for window in self.driver.window_handles if window != main_window_handle][0]
        # 3. Alterne para a nova janela
        self.driver.switch_to.window(new_window_handle)
        # 1. Espere até que o alerta esteja presente
        wait.until(EC.alert_is_present())
        # 2. Alterne para o alerta
        alert = self.driver.switch_to.alert
        # 3. Aceite o alerta (clique no botão "ok")
        alert.accept()
        self.driver.switch_to.frame("cpo")
        ok_aviso = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/center/a')))
        ok_aviso.click()
        geracao_Nota_Fiscal = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/table/tbody/tr/td[1]/table/tbody/tr[4]/td[2]/font/a')))
        geracao_Nota_Fiscal.click()
        # Emissão das notas ficais apos login
        for (
            id_data,
            cnpj_cpf_data,
            n_cnpj_cpf_data,
            nome_data,
            endereco_data,
            numero_data,
            complemento_data,
            bairro_data,
            cep_data,
            cod_mun_prestador_data,
            cod_mun_tomador_data,
            atividade_economica_data,
            discrimicacao_data,
            valor_data,
            check_data,
            pasta_data,
            link_data,
        ) in zip(
            ListNFService.objects.values_list("id", flat=True),
            cnpj_cpf_list,
            n_cnpj_cpf_list,
            nome_list,
            endereco_list,
            numero_list,
            complemento_list,
            bairro_list,
            cep_list,
            cod_mun_prestador_list,
            cod_mun_tomador_list,
            atividade_economica_list,
            discrimicacao_list,
            valor_list,
            check_list,
            pasta_list,
            link_nfse_list
        ):
            if len(n_cnpj_cpf_data) < 11:
                cnpj_cpf_corrigido = n_cnpj_cpf_data.zfill(11).strip()
            else:
                cnpj_cpf_corrigido = n_cnpj_cpf_data.strip()
            if check_data is False:
                try:
                    select_cnpj_cpf = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(10) > td:nth-child(3) > select > option:nth-child(1)')))
                    select_cnpj_cpf.send_keys(cnpj_cpf_data)
                    if n_cnpj_cpf_data != 'nan':
                        input_cnpj_cpf = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(10) > td:nth-child(3) > input:nth-child(2)')))
                        input_cnpj_cpf.send_keys(cnpj_cpf_corrigido)
                        btn_consultar_cnpj_cpf = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(10) > td:nth-child(3) > input[type=button]:nth-child(3)')))
                        btn_consultar_cnpj_cpf.click()
                    input_cnpj_cpf = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(10) > td:nth-child(3) > input:nth-child(2)')))
                    # input_cnpj_cpf.send_keys('')
                    btn_consultar_cnpj_cpf = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(10) > td:nth-child(3) > input[type=button]:nth-child(3)')))
                    # btn_consultar_cnpj_cpf.click()  
                    sleep(2)
                    input_nome = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(12) > td:nth-child(3) > input')))
                    input_nome.send_keys(nome_data)
                    if endereco_data != 'nan':
                        input_logradouro = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(13) > td:nth-child(3) > input:nth-child(1)')))
                        input_logradouro.send_keys(endereco_data)
                        input_numero = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(13) > td:nth-child(3) > input:nth-child(2)')))
                        input_numero.send_keys(numero_data)
                        input_complemento = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(13) > td:nth-child(3) > input:nth-child(3)')))
                        input_complemento.send_keys(complemento_data)
                        input_bairro = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(14) > td:nth-child(3) > input:nth-child(1)')))
                        input_bairro.send_keys(bairro_data)
                        input_CEP = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(14) > td:nth-child(3) > input:nth-child(2)')))
                        input_CEP.send_keys(cep_data)
                    # input_logradouro = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(13) > td:nth-child(3) > input:nth-child(1)')))
                    # input_logradouro.send_keys('')
                    # input_numero = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(13) > td:nth-child(3) > input:nth-child(2)')))
                    # input_numero.send_keys('')
                    # input_complemento = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(13) > td:nth-child(3) > input:nth-child(3)')))
                    # input_complemento.send_keys('')
                    # input_bairro = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(14) > td:nth-child(3) > input:nth-child(1)')))
                    # input_bairro.send_keys('')
                    # input_CEP = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(14) > td:nth-child(3) > input:nth-child(2)')))
                    # input_CEP.send_keys('')
                    # input_municipio_prestador = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(16) > td:nth-child(3) > input.txt')))
                    # input_municipio_prestador.send_keys(cod_mun_prestador_data)
                    consulta_municipio_prestador = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(16) > td:nth-child(3) > input[type=button]:nth-child(2)')))
                    consulta_municipio_prestador.click()
                    # input_municipio_tomador = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(22) > td:nth-child(3) > input.txt')))
                    # input_municipio_tomador.send_keys(cod_mun_tomador_data)
                    consulta_municipio_tomador = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(22) > td:nth-child(3) > input[type=button]:nth-child(2)')))
                    consulta_municipio_tomador.click()
                    select_atividade_economica = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(24) > td:nth-child(3) > select')))
                    select_atividade_economica.send_keys(atividade_economica_data)
                    input_discriminacao = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(26) > td:nth-child(3) > textarea')))
                    input_discriminacao.send_keys(discrimicacao_data)
                    input_valor = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(29) > td:nth-child(3) > input:nth-child(1)')))
                    input_valor.send_keys(str(valor_data).replace(".", ","))
                    gerar_nfse = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/form/table/tbody/tr[35]/td[1]/input[1]')))
                    gerar_nfse.click()
                    try:
                        # Espere até que o alerta esteja presente
                        wait_short = WebDriverWait(self.driver, 2)  # 2 segundos de espera
                        alert = wait_short.until(EC.alert_is_present())

                        # Aqui você decide se quer aceitar ou rejeitar o alerta.
                        # Para aceitar (clique em "OK"):
                        alert.accept()

                        # Para rejeitar (clique em "Cancelar"):
                        # alert.dismiss()
                    except TimeoutException:
                        # O alerta não apareceu dentro do período de espera de 2 segundos, então prosseguimos normalmente.
                        pass
                    main_window_handle = self.driver.current_window_handle
                    wait.until(EC.number_of_windows_to_be(3))
                    new_window_handle = [window for window in self.driver.window_handles if window != main_window_handle][1]
                    self.driver.switch_to.window(new_window_handle)
                    
                    # ipdb.set_trace()
                    inscricao_municipal = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[2]/td[3]/b/span')))    
                    numero_da_nota = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td[2]/b')))    
                    verificador = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/table/tbody/tr[1]/td[2]/table/tbody/tr[3]/td[2]/b')))    
                    link_da_nota = f'http://www2.goiania.go.gov.br/sistemas/snfse/asp/snfse00200w0.asp?inscricao={inscricao_municipal.text}&nota={numero_da_nota.text}&verificador={verificador.text}'
                    # ipdb.set_trace()
                    self.driver.close()
                    
                    self.driver.switch_to.window(self.driver.window_handles[-1]) 
                    main_window_handle = self.driver.current_window_handle
                    self.driver.switch_to.frame("cpo")
                    # ipdb.set_trace()
                    
                    item = ListNFService.objects.get(id=id_data)
                    item.checkNf = True
                    item.link_nfse = link_da_nota
                    item.save()
                    
                    btn_limpar = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/form/table/tbody/tr[35]/td[1]/input[2]')))
                    btn_limpar.click()
                except WebDriverException as e:
                    print("Erro no WebDriver:", e)
                    traceback.print_exc()
                except Exception as e:
                    print("Erro geral:", e)
                    traceback.print_exc()

def run_imprimir(request):
    test_class_instance = TestImprimir()
    test_class_instance.test_imprimir()
    test_class_instance.tearDown()
    return HttpResponse("Notas impressas com sucesso!")

class TestImprimir(TestCase):
  def __init__(self):
      self.driver = webdriver.Firefox()
      self.vars = {}  
  def tearDown(self):
      self.driver.quit()
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def wait_for_window(self, timeout = 2):
    time.sleep(round(timeout / 1000))
    wh_now = self.driver.window_handles
    wh_then = self.vars["window_handles"]
    if len(wh_now) > len(wh_then):
      return set(wh_now).difference(set(wh_then)).pop()
  
  
  def test_imprimir(self):
    nfse_NF_list = ListNFService.objects.values_list("Numero_NF", flat=True)
    array_link = []
    CONST_NF = ['3286', '3287']
    wait = WebDriverWait(self.driver, 10)
    self.driver.get("https://www10.goiania.go.gov.br/Internet/Login.aspx?OriginalURL=https%3a%2f%2fwww10.goiania.go.gov.br%2fsicaeportal%2fHomePage.aspx")
    self.driver.find_element(By.ID, "wt17_wtMainContent_wtUserNameInput").click()
    self.driver.find_element(By.ID, "wt17_wtMainContent_wtUserNameInput").send_keys("01237041112")
    self.driver.find_element(By.ID, "wt17_wtMainContent_wtPasswordInput").click()
    self.driver.find_element(By.ID, "wt17_wtMainContent_wtPasswordInput").send_keys("Pf050786")
    self.driver.find_element(By.ID, "wt17_wtMainContent_wt30").click()
    wait.until(EC.frame_to_be_available_and_switch_to_it(0))
    entrar = wait.until(EC.visibility_of_element_located((By.ID,"WebPatterns_wt8_block_wtMainContent_wt6",)))
    entrar.click()
    self.driver.switch_to.default_content()
    self.driver.find_element(By.ID, "select2-chosen-1").click()
    select = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#s2id_autogen1_search",)))
    select.send_keys("CAE : 4832817 - DR PAULO FERNANDO NUTROLOGIA LTDA")
    option = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"[id^='select2-result-label-'] > span")))
    option.click()
    btn_nfse = wait.until(EC.visibility_of_element_located((By.XPATH,'//span[contains(text(), "NF Eletrônica")]')))
    btn_nfse.click()
    entrar_nfse = wait.until(EC.visibility_of_element_located((By.XPATH,'//span[contains(text(), "Entrar")]')))
    entrar_nfse.click()
    # 1. Armazene a handle da janela principal
    main_window_handle = self.driver.current_window_handle
    # 2. Espere até que uma nova janela esteja disponível
    wait.until(EC.number_of_windows_to_be(2))
    new_window_handle = [window for window in self.driver.window_handles if window != main_window_handle][0]
    # 3. Alterne para a nova janela
    self.driver.switch_to.window(new_window_handle)
    # 1. Espere até que o alerta esteja presente
    wait.until(EC.alert_is_present())
    # 2. Alterne para o alerta
    alert = self.driver.switch_to.alert
    # 3. Aceite o alerta (clique no botão "ok")
    alert.accept()
    self.driver.switch_to.frame("cpo")
    ok_aviso = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/center/a')))
    ok_aviso.click()
    consulta_Nota_Fiscal_por_numero = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(13) > td:nth-child(2) > font > a > b')))
    consulta_Nota_Fiscal_por_numero.click()
    for nfse_data in nfse_NF_list:
      #   ipdb.set_trace()  
      input_Nota_Fiscal_por_numero = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/form/table/tbody/tr[8]/td[3]/input[1]')))
      input_Nota_Fiscal_por_numero.clear()
      input_Nota_Fiscal_por_numero.send_keys(nfse_data)
      btn_Nota_Fiscal_por_numero = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > table > tbody > tr:nth-child(8) > td:nth-child(3) > input[type=button]:nth-child(2)')))
      btn_Nota_Fiscal_por_numero.click()
      
      self.driver.switch_to.window(self.driver.window_handles[-1])
      # main_window_handle = self.driver.current_window_handle
      inscricao_municipal = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr[2]/td[3]/b/span')))    
      numero_da_nota = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/table/tbody/tr[1]/td[2]/table/tbody/tr[1]/td[2]/b')))    
      nome_cliente = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/b')))    
      verificador = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/table/tbody/tr[1]/td[2]/table/tbody/tr[3]/td[2]/b')))    
      link_da_nota = f'http://www2.goiania.go.gov.br/sistemas/snfse/asp/snfse00200w0.asp?inscricao={inscricao_municipal.text}&nota={numero_da_nota.text}&verificador={verificador.text}'
      array_link.append({'url': link_da_nota, 'nota_number': numero_da_nota.text, 'nome_cliente': nome_cliente.text})
      self.driver.close()
      # ipdb.set_trace()
      
      self.driver.switch_to.window(self.driver.window_handles[-1])      
      # ipdb.set_trace()
      main_window_handle = self.driver.current_window_handle
      self.driver.switch_to.window(new_window_handle) 
      self.driver.switch_to.frame("cpo")
      # ipdb.set_trace() 
      sleep(2)
      
    for item in array_link:
      link = item['url']
      nota_number = item['nota_number']     
      nome = item['nome_cliente']     
      output_path = r"C:\Users\daniel.barbosa\Desktop\notas\outubro\nota_{}_{}.pdf".format(nota_number, nome)
      HTML(url=link).write_pdf(output_path)



