import math
import json
from pathlib import Path

class GestureRecognizer:
    def __init__(self):
        with open(Path(__file__).parent / "gestures_comands.json", 'r') as arquivo:
            data = json.load(arquivo)
        self.Gestures = list(data.keys())
        self.razao_min_pinca = 0.35

    def __calcular_distancia(self, p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    def recognizer(self, landmarks, hand):
        # Pontos mapeados na lista de landmarks (0 a 20)
        pulso = landmarks[0]
        base_medio = landmarks[9]
        ponta_polegar = landmarks[4]
        ponta_indicador = landmarks[8]
        ponta_medio = landmarks[12]

        # Cálculo da normalização pela palma
        tamanho_palma = self.__calcular_distancia(pulso, base_medio)
        if tamanho_palma == 0:
            return None

        # Distância da pinça
        razao_indicador = self.__calcular_distancia(ponta_polegar, ponta_indicador) / tamanho_palma
        razao_medio = self.__calcular_distancia(ponta_polegar, ponta_medio) / tamanho_palma

        print(razao_indicador)
        print(razao_medio)
        print(hand)

        # Regra de ativação separada por lateralidade
        if hand == "Right":
            if razao_indicador < self.razao_min_pinca:
                return self.Gestures[0]
            if razao_medio < self.razao_min_pinca:
                return self.Gestures[1]
        if hand == "Left":
            if razao_indicador < self.razao_min_pinca:
                return self.Gestures[2]
            if razao_medio < self.razao_min_pinca:
                return self.Gestures[3]