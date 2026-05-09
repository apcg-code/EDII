import folium
from folium import Icon
import os

CIDADES_NOMES = ["Brasilia", "Belo Horizonte", "Sao Paulo", "Rio de Janeiro",
                 "Salvador", "Fortaleza", "Belem", "Manaus", "Florianopolis"]

CIDADES_COORDENADAS = [
    (-15.83, -47.86),  # Brasilia
    (-19.92, -43.94),  # Belo Horizonte
    (-23.55, -46.64),  # Sao Paulo
    (-22.91, -43.15),  # Rio de Janeiro
    (-12.96, -38.51),  # Salvador
    (-3.71, -38.54),  # Fortaleza
    (-1.45, -48.50),  # Belem
    (-3.04, -60.03),  # Manaus
    (-27.59, -48.55)  # Florianopolis
]

rota = [
    (0, 2), (0, 8), (0, 7), (0, 5), (0, 4), (0, 6), (0, 3), (0, 1),
    (1, 0), (1, 5), (1, 8), (1, 2),
    (2, 0), (2, 4), (2, 8), (2, 3), (2, 5), (2, 7), (2, 1),
    (3, 0), (3, 2), (3, 1),
    (4, 0), (4, 2), (4, 3), (4, 7),
    (5, 0), (5, 2), (5, 6), (5, 3),
    (6, 0), (6, 2), (6, 4),
    (7, 0), (7, 2), (7, 1),
    (8, 2), (8, 3), (8, 1), (8, 7)
]

mapa_conexoes = folium.Map(location=[-15.7801, -47.9292], zoom_start=4)

linhas_desenhadas = set()

for idx_origem, idx_destino in rota:

    chave = tuple(sorted((idx_origem, idx_destino)))

    if chave not in linhas_desenhadas:
        coord_origem = CIDADES_COORDENADAS[idx_origem]
        coord_destino = CIDADES_COORDENADAS[idx_destino]

        folium.PolyLine(
            locations=[coord_origem, coord_destino],
            color='purple',
            weight=2.5,
            opacity=0.5,
            tooltip=f"{CIDADES_NOMES[idx_origem]} - {CIDADES_NOMES[idx_destino]}"
        ).add_to(mapa_conexoes)

        linhas_desenhadas.add(chave)

for i, (lat, lon) in enumerate(CIDADES_COORDENADAS):
    nome = CIDADES_NOMES[i]
    icon = Icon(color='darkpurple', icon='plane', prefix='glyphicon')

    folium.Marker(
        location=[lat, lon],
        popup=f'<b>{nome}</b>',
        icon=icon
    ).add_to(mapa_conexoes)

diretorio_atual = os.path.dirname(os.path.abspath(__file__))

caminho_arquivo = os.path.join(diretorio_atual, "templates", "map.html")

mapa_conexoes.save(caminho_arquivo)
print(f"O arquivo foi gerado em: {caminho_arquivo}")
