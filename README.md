
# Sistema de Gerenciamento de Voos (Flight Manager)

Este projeto foi desenvolvido como **Trabalho Final da disciplina de Estrutura de Dados II**. O objetivo principal é aplicar conceitos fundamentais de organização de dados, manipulação de arquivos e lógica de programação em um ambiente Web real utilizando o framework Flask.

---

## Sobre o Projeto

O **Flight Manager** é uma aplicação voltada para a gestão e reserva de passagens aéreas. O sistema separa as funcionalidades por níveis de acesso, garantindo que usuários comuns possam visualizar e reservar voos, enquanto administradores possuem controle sobre a malha aérea e usuários.

### Principais Funcionalidades:

* **Autenticação de Usuários:** Sistema de login seguro com diferentes níveis de permissão.
* **RBAC (Role-Based Access Control):** Controle de acesso baseado em funções (Admin/Usuário) utilizando *Python Decorators*.
* **Persistência de Dados:** Armazenamento e leitura de dados via arquivos JSON, simulando um banco de dados NoSQL.
* **Gestão de Voos:** Visualização dinâmica de passagens disponíveis, preços e assentos.

---

## Tecnologias Utilizadas

Para este projeto, optei por uma stack que equilibra simplicidade e robustez para o aprendizado acadêmico:

* **Python:** Linguagem base pela sua versatilidade na manipulação de estruturas.
* **Flask:** Micro-framework web para a construção das rotas e lógica de servidor.
* **Jinja2:** Engine de templates para renderização dinâmica de dados no HTML.
* **JSON:** Utilizado para persistência de dados, explorando o conceito de dicionários e listas encadeadas.

---

## Arquitetura e Estrutura de Dados

Como este é um projeto para a disciplina de **Estrutura de Dados**, o código foi desenhado priorizando a organização e separação de responsabilidades:

* **`models.py`**: Definição das classes (Objetos), representando a estrutura de dados central do sistema (Entidade Voo).
* **`dicionario.py`**: Camada de persistência e conversão. Aqui, transformamos dados brutos (JSON) em estruturas Pythonic (*Dicionários e Listas de Objetos*) para otimizar a busca e manipulação em memória.
* **`decorators.py`**: Implementação de funções de alta ordem para garantir a segurança das rotas, demonstrando conhecimento em lógica de fluxo.
* **`routes.py`**: Gerenciamento do fluxo de navegação e controle das regras de negócio.

---

## Como Executar o Projeto

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git

```


2. **Crie um ambiente virtual:**
```bash
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

```


3. **Instale as dependências:**
```bash
pip install flask

```


4. **Inicie o servidor:**
```bash
python main.py

```


Acesse no navegador: `http://127.0.0.1:5000`

---

##  Requisitos de Negócio (Lógica de Acesso)

O sistema opera com dois níveis de prioridade:

1. **Usuário (Nível 1):** Acesso à consulta de voos e reservas.
2. **Administrador (Nível 2):** Acesso completo ao painel administrativo e gestão do sistema.


###  Por que este projeto é relevante para o meu perfil?

"Neste projeto, não apenas criei um site, mas resolvi problemas de organização de informação. Usei **Decorators** para evitar repetição de código, tratei a persistência com **JSON** para entender como os dados fluem entre o disco e a memória, e apliquei **Orientação a Objetos** para criar modelos escaláveis. Isso me ajudou a solidificar uma base em algoritimos e estrutura de dados me dando um bom ponto de partida para aprender frameworks mais complexos."

---
