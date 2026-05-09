import json
from models import Voo


def carregar_usuarios():
    try:
        with open("./arquivos/usuarios.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return dados.get("Usuarios", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def carregar_voos():
    lista_de_objetos_voo = []
    try:
        with open("./arquivos/voo.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            voo_dict = dados.get("voo")
            if voo_dict:
                novo_voo = Voo(
                    id=voo_dict['id'],
                    origem=voo_dict['origem'],
                    horarioPartida=voo_dict['horarioPartida'],
                    destino=voo_dict['destino'],
                    horarioChegada=voo_dict['horarioChegada'],
                    Data=voo_dict['Data']
                )
                lista_de_objetos_voo.append(novo_voo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    return lista_de_objetos_voo


def definirImg(destino):

    if destino == "Brasilia":
        return "images/Brasilia.jpg"
    elif destino == "Belo Horizonte":
        return "images/BeloHorizonte.jpg"
    elif destino == "São Paulo":
        return "images/SaoPaulo.jpg"
    elif destino == "Rio de Janeiro":
        return "images/RiodeJaneiro.jpg"
    elif destino == "Salvador":
        return "images/Salvador.jpg"
    elif destino == "Fortaleza":
        return "images/Fortaleza.jpg"
    elif destino == "Belem":
        return "images/Belem.jpg"
    elif destino == "Manaus":
        return "images/Manaus.jpeg"
    elif destino == "Florianopolis":
        return "images/Florianopolis.jpg"
    else:
        return "images/aviao.png"
