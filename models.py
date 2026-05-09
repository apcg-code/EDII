# models.py

class Voo:
    def __init__(self, id, origem, horarioPartida, destino, horarioChegada, Data):
        self.id = id
        self.origem = origem
        self.horarioPartida = horarioPartida
        self.destino = destino
        self.horarioChegada = horarioChegada
        self.Data = Data

    def __repr__(self):
        return f'<Voo {self.id}: de {self.origem} para {self.destino}>'
