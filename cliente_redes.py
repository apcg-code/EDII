import requests

URL = 'http://localhost:5001/api/voos'

print("--- 1. INICIANDO REQUISIÇÃO GET ---")
resposta_get = requests.get(URL)

print(f"Status HTTP retornado: {resposta_get.status_code}")
if resposta_get.status_code == 200:
    voos = resposta_get.json()
    print(f"Sucesso! O servidor retornou {len(voos)} voos cadastrados.")
    print(f"Mostrando o primeiro voo da lista para conferência:")
    print(voos[0])
print("\n" + "="*50 + "\n")


print("--- 2. INICIANDO REQUISIÇÃO POST ---")
# Criando um payload (corpo da mensagem) exatamente no formato que seu JSON exige
novo_voo_payload = {
    "id": 122,  # Continuei a numeração do seu JSON
    "origem": "Salvador",
    "destino": "Recife",
    "Data": "2026-01-10",
    "horarioPartida": "10:00",
    "horarioChegada": "11:30",
    "preco": 350.0,
    "assentos_disponiveis": 50,
    "imagem": "images/Recife.jpg"
}

resposta_post = requests.post(URL, json=novo_voo_payload)

print(f"Status HTTP retornado: {resposta_post.status_code}")
if resposta_post.status_code == 201:
    print("Sucesso! Resposta do Servidor:")
    print(resposta_post.json())
