import pandas as pd
import string
import os


ordem = 4


class Registro:
    def __init__(self):
        self.Chave = None
        self.Elemento = None


class Pagina:
    def __init__(self, ordem):
        self.n = 0
        self.r = [None for i in range(ordem)]
        self.p = [None for i in range(ordem+1)]


def pesquisa(x, Ap):

    i = 1
    if (Ap == None):
        print("Registro não está presente na árvore\n")
        return None

    while (i < Ap.n and x.Chave > Ap.r[i - 1].Chave):
        i += 1
    if (x.Chave == Ap.r[i - 1].Chave):
        x = Ap.r[i - 1]
        return x

    if (x.Chave < Ap.r[i - 1].Chave):
        x = pesquisa(x, Ap.p[i - 1])
    else:
        x = pesquisa(x, Ap.p[i])

    return x.Elemento


def _InsereNaPagina(Ap, Reg, ApDir):
    k = Ap.n
    NaoAchouPosicao = (k > 0)
    while (NaoAchouPosicao):
        if (Reg.Chave >= Ap.r[k - 1].Chave):
            NaoAchouPosicao = False
            break
        Ap.r[k] = Ap.r[k - 1]
        Ap.p[k + 1] = Ap.p[k]
        k -= 1
        if (k < 1):
            NaoAchouPosicao = False

    Ap.r[k] = Reg
    Ap.p[k + 1] = ApDir
    Ap.n += 1


def _Ins(Reg, Ap, Cresceu, RegRetorno, ApRetorno, Ordem):
    i = 1
    J = None
    if (Ap == None):
        Cresceu = True
        RegRetorno = Reg
        ApRetorno = None
        return Cresceu, RegRetorno, ApRetorno

    while (i < Ap.n and Reg.Chave > Ap.r[i - 1].Chave):
        i += 1

    if (Reg.Chave == Ap.r[i - 1].Chave):
        print(" Erro: Registro já está presente\n")
        Cresceu = False
        return Cresceu, RegRetorno, ApRetorno

    if (Reg.Chave < Ap.r[i - 1].Chave):
        i -= 1

    Cresceu, RegRetorno, ApRetorno = _Ins(
        Reg, Ap.p[i], Cresceu, RegRetorno, ApRetorno, Ordem)

    if (not Cresceu):
        return Cresceu, RegRetorno, ApRetorno
    if (Ap.n < Ordem):  # Página tem espaco
        _InsereNaPagina(Ap, RegRetorno, ApRetorno)
        Cresceu = False
        return Cresceu, RegRetorno, ApRetorno

    ApTemp = Pagina(Ordem)
    ApTemp.n = 0
    ApTemp.p[0] = None
    if (i < (Ordem//2) + 1):
        _InsereNaPagina(ApTemp, Ap.r[Ordem - 1], Ap.p[Ordem])
        Ap.n -= 1
        _InsereNaPagina(Ap, RegRetorno, ApRetorno)
    else:
        _InsereNaPagina(ApTemp, RegRetorno, ApRetorno)
    for J in range((Ordem//2) + 2, Ordem + 1):
        _InsereNaPagina(ApTemp, Ap.r[J - 1], Ap.p[J])
    Ap.n = (Ordem//2)
    ApTemp.p[0] = Ap.p[(Ordem//2) + 1]
    RegRetorno = Ap.r[(Ordem//2)]
    ApRetorno = ApTemp
    return Cresceu, RegRetorno, ApRetorno


def _Insere(Reg, Ap, Ordem):
    Cresceu = False
    RegRetorno = Registro()
    ApRetorno = Pagina(Ordem)
    Cresceu, RegRetorno, ApRetorno = _Ins(
        Reg, Ap, Cresceu, RegRetorno, ApRetorno, Ordem)
    if (Cresceu):
        ApTemp = Pagina(Ordem)
        ApTemp.n = 1
        ApTemp.r[0] = RegRetorno
        ApTemp.p[1] = ApRetorno
        ApTemp.p[0] = Ap
        Ap = ApTemp
    return Ap


def _InserirElementos(Ap, ordem, dataframe, chave):
    tam_lin, tam_col = dataframe.shape
    for i in range(tam_lin):
        reg = Registro()
        reg.Chave = dataframe.iloc[i, 0]
        reg.Elemento = i
        Ap = _Insere(reg, Ap, ordem)
        chave += 1
    return Ap, chave


def Inserir(Ap, chave):
    DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
    CAMINHO_CSV = os.path.join(
        DIRETORIO_ATUAL, 'arquivos', 'clientesAgencia.csv')

    if os.path.exists(CAMINHO_CSV):
        # 'sep' pode ser ; ou , dependendo de como você salvou. O padrão do seu erro anterior era ;
        dataframe = pd.read_csv(CAMINHO_CSV, sep=";", header=None)
    else:
        print(f"ERRO: Arquivo não encontrado em {CAMINHO_CSV}")
        dataframe = pd.DataFrame()

    Ap, chave = _InserirElementos(Ap, ordem, dataframe, chave)
    return Ap, chave, dataframe
# Impressão


def listar(ap, dataframe):
    resultado = []

    def Imprimir(ap, resultado):
        if (ap != None):
            i = 0
            while i < ap.n:
                Imprimir(ap.p[i], resultado)
                resultado.append(
                    f" Chave: {ap.r[i].Chave}  - Nome: {dataframe.iloc[ap.r[i].Elemento, 1]}  - Elemento:  {ap.r[i].Elemento}")
                i += 1
            Imprimir(ap.p[i], resultado)
    Imprimir(ap, resultado)
    return resultado


def ImprimeMenorDataFrame(x, Ap, df):
    if (Ap != None):
        i = 0
        while i < Ap.n:
            ImprimeMenorDataFrame(x, Ap.p[i], df)
            if (Ap.r[i].Chave < x.Chave):
                print(df.iloc[Ap.r[i].Elemento])
            i += 1
        ImprimeMenorDataFrame(x, Ap.p[i], df)


def ImprimeMaiorDataFrame(x, Ap, df):
    if (Ap != None):
        i = 0
        while i < Ap.n:
            ImprimeMaiorDataFrame(x, Ap.p[i], df)
            if (Ap.r[i].Chave > x.Chave):
                print(df.iloc[Ap.r[i].Elemento])
            i += 1
        ImprimeMaiorDataFrame(x, Ap.p[i], df)
