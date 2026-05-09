# routes.py
from main import aNome
from main import aCpf
from main import app
from flask import redirect, render_template, request, session, url_for, flash
from decorators import permitirAcesso
from data_manager import carregar_usuarios, carregar_voos, salvar_voos, salvar_compra, Registro as registro
from datetime import datetime
import pandas as pd
import uuid
import time
import os
from dicionario import definirImg
from grafo import simular_rota, get_todas_cidades
import mapa

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_CSV = os.path.join(DIRETORIO_ATUAL, 'arquivos', 'clientesAgencia.csv')

if os.path.exists(CAMINHO_CSV):
    try:
        dataframe = pd.read_csv(CAMINHO_CSV, sep=";", header=None)
    except pd.errors.EmptyDataError:
        dataframe = pd.DataFrame(columns=[0, 1, 2, 3, 4])
else:
    dataframe = pd.DataFrame(columns=[0, 1, 2, 3, 4])


apcpf = None
chavecpf = 1
apcpf, chavecpf, dfcpf = aCpf.Inserir(apcpf, chavecpf)
regcpf = aCpf.Registro()
resultadocpf = registro()

apNome = None
chaveNome = 1
apNome, chaveNome, dfNome = aNome.Inserir(apNome, chaveNome)
regNome = aNome.Registro()
resultadoNome = []


@app.route("/")
def homepage():
    session.clear()
    return render_template("home.html")


@app.route("/pesquisa", methods=['GET', 'POST'])
def pesquisa():
    if request.method == "POST":
        tempcpf = request.form.get("cpf")
        cpf = None
        if tempcpf:
            cpf = int(tempcpf)
        nome = request.form.get("nome")
        inicial = request.form.get("listar")
        botao = request.form.get("acao")

        if botao == "listarCpf":
            try:
                result = aCpf.listar(apcpf, dataframe)
                flash(f"Listando por CPF...")
                return render_template('resultado.html', result=result)
            except ValueError:
                flash("Erro na listagem", 'error')
                return render_template("pesquisar_cliente.html")

        elif botao == "listarNome":
            try:
                result = aNome.listar(apNome, dataframe)
                flash(f"Listando por nome...")
                return render_template('resultado.html', result=result)
            except ValueError:
                flash("Erro na listagem", 'error')
                return render_template("pesquisar_cliente.html")

        if tempcpf:
            try:
                regcpf.Chave = cpf
                regcpf.Elemento = -1
                i = aCpf.pesquisa(regcpf, apcpf)
                if (i == -1):
                    flash("CPF não encontrado", 'error')
                    return render_template("pesquisar_cliente.html")

                resultadocpf.cpf = dataframe.iloc[i, 0]
                resultadocpf.nome = dataframe.iloc[i, 1]
                resultadocpf.codigo = dataframe.iloc[i, 2]
                resultadocpf.data = dataframe.iloc[i, 3]
                resultadocpf.milhas = dataframe.iloc[i, 4]
                flash(f"Buscando pelo CPF: {cpf}...")
                return render_template('resultado.html', resultado=resultadocpf)
            except ValueError:
                flash("CPF invalido", 'error')
                return render_template("pesquisar_cliente.html")
        elif nome:
            try:
                regNome.Nome = nome
                resultadoNome = aNome.pesquisa(regNome, apNome)
                resultadosF = []
                for i in resultadoNome:
                    if i < len(dataframe):
                        linha = dataframe.iloc[i]
                        resultadosF.append({
                            'cpf': linha[0], 'nome': linha[1], 'codigo': linha[2],
                            'data': linha[3], 'milhas': linha[4]
                        })
                return render_template('resultado.html', resultados=resultadosF)
            except ValueError:
                flash("Nome invalido", 'error')
                return render_template("pesquisar_cliente.html")

        elif inicial:
            try:
                regNome.Nome = inicial
                resultadoNome = aNome.pesquisaInicial(regNome, apNome)
                resultados = []
                for i in resultadoNome:
                    if i < len(dataframe):
                        linha = dataframe.iloc[i]
                        resultados.append({
                            'cpf': linha[0], 'nome': linha[1], 'codigo': linha[2],
                            'data': linha[3], 'milhas': linha[4]
                        })
                return render_template('resultado.html', resultados=resultados)
            except ValueError:
                flash("Inicial invalida", 'error')
                return render_template("pesquisar_cliente.html")

    return render_template("pesquisar_cliente.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        usuarios = carregar_usuarios()
        for dados in usuarios.values():
            if email == dados['email'] and senha == dados['senha']:
                session['logado'] = True
                session['prioridade'] = dados['prioridade']
                if dados['prioridade'] == 2:
                    return redirect(url_for('adm'))
                else:
                    return redirect(url_for('voosDisponiveis'))
        flash('Email ou senha inválidos.', 'danger')
    return render_template('login.html')


@app.route('/TelaInicial')
def telaInicial():
    voos = carregar_voos()
    return render_template("tela_inicial.html", voos=voos)


@app.route('/administrador')
@permitirAcesso(2)
def adm():
    return render_template("administrador.html")


@app.route('/gerirVoo')
@permitirAcesso(2)
def gerirVoo():
    voos = carregar_voos()
    return render_template("gestaoVoo.html", voos=voos)


@app.route('/voosDisponiveis')
def voosDisponiveis():
    voos = carregar_voos()
    return render_template("voosDisponiveis.html", voos=voos)


@app.route('/adicionar_voo', methods=['GET', 'POST'])
@permitirAcesso(2)
def adicionar_voo():
    if request.method == 'POST':
        voos = carregar_voos()
        if not isinstance(voos, list):
            voos = []
        novo_id = max([v['id'] for v in voos], default=0) + 1
        img = definirImg(request.form.get('destino'))
        novo_voo = {
            "id": novo_id,
            "origem": request.form.get('origem'),
            "destino": request.form.get('destino'),
            "Data": request.form.get('data'),
            "horarioPartida": request.form.get('partida'),
            "horarioChegada": request.form.get('chegada'),
            "preco": float(request.form.get('preco')),
            "assentos_disponiveis": int(request.form.get('assentos')),
            "imagem": img
        }
        voos.append(novo_voo)
        salvar_voos(voos)
        flash('Voo criado!', 'success')
        return redirect(url_for('gerirVoo'))
    return render_template('form_voo.html', voo=None)


@app.route('/deletar_voo', methods=['POST'])
@permitirAcesso(2)
def deletar_voo():
    try:
        id_para_deletar = int(request.form.get('voo_id'))
        lista_voos = carregar_voos()
        nova_lista = [
            voo for voo in lista_voos if voo['id'] != id_para_deletar]
        salvar_voos(nova_lista)
        flash('Voo deletado!', 'success')
    except Exception as e:
        flash(f'Erro: {e}', 'danger')
    return redirect(url_for('gerirVoo'))


@app.route('/editar_voo/<int:voo_id>', methods=["GET", "POST"])
@permitirAcesso(2)
def editar_voo(voo_id):
    voos = carregar_voos()
    voo_idx = next((i for i, v in enumerate(voos) if v['id'] == voo_id), None)
    if voo_idx is None:
        flash('Voo não encontrado.', 'danger')
        return redirect(url_for('gerirVoo'))

    if request.method == 'POST':
        img = definirImg(request.form.get('destino'))
        voos[voo_idx]['origem'] = request.form.get('origem')
        voos[voo_idx]['destino'] = request.form.get('destino')
        voos[voo_idx]['Data'] = request.form.get('data')
        voos[voo_idx]['horarioPartida'] = request.form.get('partida')
        voos[voo_idx]['horarioChegada'] = request.form.get('chegada')
        voos[voo_idx]['preco'] = float(request.form.get('preco'))
        voos[voo_idx]['assentos_disponiveis'] = int(
            request.form.get('assentos'))
        voos[voo_idx]['imagem'] = img
        salvar_voos(voos)
        flash('Voo atualizado!', 'success')
        return redirect(url_for('gerirVoo'))
    return render_template('form_voo.html', voo=voos[voo_idx])


@app.route('/excluir_voo/<int:id_voo>')
@permitirAcesso(2)
def excluir_voo(id_voo):
    voos = carregar_voos()
    nova_lista = [v for v in voos if v['id'] != id_voo]
    if len(nova_lista) < len(voos):
        salvar_voos(nova_lista)
        flash('Voo excluído.', 'warning')
    return redirect(url_for('gerirVoo'))


@app.route("/sobre")
def sobre():
    return "Pagina sobre..."


@app.route("/welcome")
def welcome():
    return render_template("homepage.html")


@app.route('/comprar/<int:id_voo>', methods=['GET'])
def pagina_compra(id_voo):
    voos = carregar_voos()
    voo_escolhido = next((v for v in voos if v['id'] == id_voo), None)
    if not voo_escolhido:
        flash("Voo não encontrado.", "danger")
        return redirect(url_for('voosDisponiveis'))
    return render_template('compra.html', voo=voo_escolhido)


@app.route('/confirmar_compra/<int:id_voo>', methods=['POST'])
def confirmar_compra(id_voo):
    nome_cliente = request.form.get('nome_cliente')
    cpf_cliente = request.form.get('cpf_cliente')
    voos = carregar_voos()
    voo_escolhido = next((v for v in voos if v['id'] == id_voo), None)
    if voo_escolhido and voo_escolhido.get('assentos_disponiveis', 0) > 0:
        codigo_reserva = str(uuid.uuid4())[:8].upper()
        milhas_ganhas = int(float(voo_escolhido.get('preco', 0)))
        nova_compra = {
            "codigo_reserva": codigo_reserva,
            "cliente_nome": nome_cliente,
            "cliente_cpf": cpf_cliente,
            "voo_origem": voo_escolhido['origem'],
            "voo_destino": voo_escolhido['destino'],
            "data_viagem": voo_escolhido['Data'],
            "preco_pago": voo_escolhido.get('preco', 0),
            "milhas_acumuladas": milhas_ganhas,
            "data_compra": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        voo_escolhido['assentos_disponiveis'] -= 1
        if salvar_voos(voos) and salvar_compra(nova_compra):
            flash(
                f"Compra confirmada! Código: {codigo_reserva}. Ganhou {milhas_ganhas} milhas!", "success")
        else:
            flash("Erro ao salvar.", "danger")
    else:
        flash("Voo lotado ou inválido.", "warning")
    return redirect(url_for('voosDisponiveis'))


@app.route('/simulacao', methods=['GET', 'POST'])
def simulacao():
    cidades = get_todas_cidades()
    caminho = None
    custo_total = 0
    erro = None

    if request.method == 'POST':
        origem = request.form.get('origem')
        destino = request.form.get('destino')

        if origem == destino:
            erro = "Origem e destino não podem ser iguais."
        else:
            nomes_cidades, _ = simular_rota(origem, destino)

            if not nomes_cidades:
                erro = f"Não há rota disponível entre {origem} e {destino}."
            else:
                voos_reais_encontrados = []
                todos_voos = carregar_voos()

                rota_valida = True
                custo_real_acumulado = 0

                for i in range(len(nomes_cidades) - 1):
                    cidade_atual = nomes_cidades[i]
                    proxima_cidade = nomes_cidades[i+1]

                    voo_trecho = next(
                        (v for v in todos_voos if v['origem'] == cidade_atual and v['destino'] == proxima_cidade and v['assentos_disponiveis'] > 0), None)

                    if voo_trecho:
                        voos_reais_encontrados.append(voo_trecho)
                        custo_real_acumulado += float(voo_trecho['preco'])
                    else:
                        rota_valida = False
                        erro = f"Rota quebrada: Voo de {cidade_atual} para {proxima_cidade} não encontrado ou lotado."
                        break

                if rota_valida:
                    caminho = voos_reais_encontrados
                    custo_total = custo_real_acumulado
                    session['combo_ids'] = [v['id'] for v in caminho]

    return render_template('simulacao.html', cidades=cidades, caminho=caminho, custo=custo_total, erro=erro)


@app.route('/resumo_compra_combo')
def resumo_compra_combo():
    combo_ids = session.get('combo_ids', [])
    if not combo_ids:
        flash("Nenhuma rota selecionada para compra.", "warning")
        return redirect(url_for('simulacao'))

    todos_voos = carregar_voos()
    voos_do_combo = [v for v in todos_voos if v['id'] in combo_ids]

    total_preco = sum([v['preco'] for v in voos_do_combo])

    return render_template('compra_combo.html', voos=voos_do_combo, total=total_preco)


@app.route('/confirmar_compra_combo', methods=['POST'])
def confirmar_compra_combo():
    combo_ids = session.get('combo_ids', [])
    if not combo_ids:
        return redirect(url_for('simulacao'))

    nome_cliente = request.form.get('nome_cliente')
    cpf_cliente = request.form.get('cpf_cliente')

    todos_voos = carregar_voos()
    voos_para_comprar = [v for v in todos_voos if v['id'] in combo_ids]

    for voo in voos_para_comprar:
        if voo['assentos_disponiveis'] <= 0:
            flash(
                f"O trecho {voo['origem']} -> {voo['destino']} acabou de lotar!", "danger")
            return redirect(url_for('simulacao'))

    codigos_gerados = []
    total_milhas = 0

    for voo in voos_para_comprar:
        codigo_reserva = str(uuid.uuid4())[:8].upper()
        milhas = int(float(voo.get('preco', 0)))
        total_milhas += milhas

        nova_compra = {
            "codigo_reserva": codigo_reserva,
            "cliente_nome": nome_cliente,
            "cliente_cpf": cpf_cliente,
            "voo_origem": voo['origem'],
            "voo_destino": voo['destino'],
            "data_viagem": voo['Data'],
            "preco_pago": voo.get('preco', 0),
            "milhas_acumuladas": milhas,
            "data_compra": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        voo['assentos_disponiveis'] -= 1
        salvar_compra(nova_compra)
        codigos_gerados.append(codigo_reserva)

    salvar_voos(todos_voos)
    session.pop('combo_ids', None)

    flash(
        f"Combo comprado com sucesso! Reservas: {', '.join(codigos_gerados)}", "success")
    return redirect(url_for('voosDisponiveis'))


@app.route('/visualizar_grafo')
@permitirAcesso(2)
def visualizar_grafo():
    from grafo import gerar_imagem_grafo
    import os

    nome_arquivo = 'grafo_gerado.png'
    caminho_imagem = os.path.join(
        app.root_path, 'static', 'images', nome_arquivo)

    try:
        gerar_imagem_grafo(caminho_imagem)
    except Exception as e:
        print(f"Erro ao gerar grafo: {e}")
        pass

    return render_template('visualizar_grafo.html')


@app.route('/mapa')
def show_map():
    return render_template('map.html')
