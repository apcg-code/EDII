from igraph import Graph
from igraph import plot

grafo = Graph(directed=True)
grafo.add_vertices(9)

nomes = ["Brasilia", "Belo Horizonte", "Sao Paulo", "Rio de Janeiro",
         "Salvador", "Fortaleza", "Belem", "Manaus", "Florianopolis"]

for i in range(len(grafo.vs)):
    grafo.vs[i]["id"] = i
    grafo.vs[i]['label'] = nomes[i]

grafo.add_edges([
    (0, 2), (0, 8), (0, 7), (0, 5), (0, 4), (0, 6), (0, 3), (0, 1),
    (1, 0), (1, 5), (1, 8), (1, 2),
    (2, 0), (2, 4), (2, 8), (2, 3), (2, 5), (2, 7), (2, 1),
    (3, 0), (3, 2), (3, 1),
    (4, 0), (4, 2), (4, 3), (4, 7),
    (5, 0), (5, 2), (5, 6), (5, 3),
    (6, 0), (6, 2), (6, 4),
    (7, 0), (7, 2), (7, 1),
    (8, 2), (8, 3), (8, 1), (8, 7)
])

pesos = [
    2, 4, 3, 3, 2, 2, 2, 1,
    1, 3, 3, 1,
    2, 2, 2, 1, 4, 5, 1,
    2, 1, 1,
    2, 2, 2, 4,
    3, 4, 3, 5,
    2, 4, 3,
    3, 5, 4,
    2, 3, 3, 6
]

grafo.es['weight'] = pesos
grafo.es['label'] = pesos


def converter(cidade):
    cidade = cidade.strip()
    if cidade == "Brasilia":
        return 0
    elif cidade == "Belo Horizonte":
        return 1
    elif cidade == "Sao Paulo":
        return 2
    elif cidade == "Rio de Janeiro":
        return 3
    elif cidade == "Salvador":
        return 4
    elif cidade == "Fortaleza":
        return 5
    elif cidade == "Belem":
        return 6
    elif cidade == "Manaus":
        return 7
    elif cidade == "Florianopolis":
        return 8
    else:
        return -1


def reverter(id_vertice):
    if 0 <= id_vertice < len(nomes):
        return nomes[id_vertice]
    else:
        return "Desconhecido"


def simular_rota(origem, destino):

    o = converter(origem)
    d = converter(destino)

    if o == -1 or d == -1:
        return ["Cidade inválida"], 0

    caminhos = grafo.get_shortest_paths(
        o, to=d, weights='weight', output="vpath")

    if not caminhos or not caminhos[0]:
        return [], 0

    caminho_ids = caminhos[0]

    custo_total = 0
    cidades_nomes = []

    for i in range(len(caminho_ids)):
        cidades_nomes.append(reverter(caminho_ids[i]))

        if i < len(caminho_ids) - 1:
            eid = grafo.get_eid(caminho_ids[i], caminho_ids[i+1])
            custo_total += grafo.es[eid]['weight']

    return cidades_nomes, custo_total


def get_todas_cidades():
    return sorted(nomes)


def gerar_imagem_grafo(caminho_salvar):

    coordenadas_mapa = [
        [-47.929, -15.780],  # 0 - Brasília
        [-43.934, -19.916],  # 1 - Belo Horizonte
        [-46.633, -23.550],  # 2 - São Paulo
        [-43.197, -22.909],  # 3 - Rio de Janeiro
        [-38.510, -12.971],  # 4 - Salvador
        [-38.542, -3.717],   # 5 - Fortaleza
        [-48.502, -1.455],   # 6 - Belem
        [-60.022, -3.119],   # 7 - Manaus
        [-48.548, -27.595]   # 8 - Florianopolis
    ]

    layout_geo = []
    for long, lat in coordenadas_mapa:
        layout_geo.append([long, -lat])

    visual_style = {}
    visual_style["layout"] = layout_geo
    visual_style["bbox"] = (800, 800)
    visual_style["margin"] = 50
    visual_style["vertex_size"] = 25
    visual_style["vertex_label_size"] = 14
    visual_style["vertex_label_dist"] = 1.5
    visual_style["vertex_color"] = '#5a17c8'
    visual_style["vertex_label_color"] = 'black'
    visual_style["edge_width"] = [1.5 for _ in grafo.es]
    visual_style["edge_curved"] = 0.2
    visual_style["background"] = None

    plot(grafo, caminho_salvar, **visual_style)
