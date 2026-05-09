# data_manager.py
import json
import csv
import os
from datetime import datetime

_DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
_ARQUIVO_USUARIOS = os.path.join(_DIRETORIO_ATUAL, 'arquivos', 'usuarios.json')
_ARQUIVO_VOOS = os.path.join(_DIRETORIO_ATUAL, 'arquivos', 'voo.json')
def _get_caminho(nome_arquivo):
    return os.path.join(_DIRETORIO_ATUAL, 'arquivos', nome_arquivo)
def carregar_usuarios():
    try:
        with open(_ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return dados.get("Usuarios", {})
    except Exception as e:
        print(f"ERRO AO CARREGAR O ARQUIVO de usuários: {e}")
        return {}

def carregar_voos():
    try:
        with open(_ARQUIVO_VOOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return dados.get("Voos", [])
    except Exception as e:
        print(f"ERRO AO CARREGAR O ARQUIVO de voos: {e}")
        return []

def salvar_voos(lista_de_voos):
    try:
        with open(_ARQUIVO_VOOS, "w", encoding="utf-8") as arquivo:
            dados_para_salvar = {"Voos": lista_de_voos}
            json.dump(dados_para_salvar, arquivo, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"ERRO AO SALVAR O ARQUIVO de voos: {e}")
        return False

class Registro:
  def __init__(self):
    self.cpf = None
    self.nome = None
    self.codigo = None
    self.data = None
    self.milhas = None

def salvar_compra(nova_compra):
    
    caminho = _get_caminho('clientesAgencia.csv')
    
    data_viagem = nova_compra.get('data_viagem', '')
    try:
        data_obj = datetime.strptime(data_viagem, "%Y-%m-%d")
        data_formatada = data_obj.strftime("%d/%m/%Y")
    except ValueError:
        data_formatada = data_viagem 

    
    linha = [
        nova_compra.get('cliente_cpf', ''),
        nova_compra.get('cliente_nome', ''),
        nova_compra.get('codigo_reserva', ''),
        data_formatada,
        nova_compra.get('milhas_acumuladas', 0)
    ]

    try:
        with open(caminho, 'a', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo, delimiter=';')
            escritor.writerow(linha)
        return True
    except Exception as e:
        print(f"Erro ao salvar compra no CSV: {e}")
        return False