import math
import json
from pathlib import Path
from .Comands import Comands

class GestureRecognizer:
    def __init__(self):
        with open(Path(__file__).parent / "gestures_comands.json", 'r') as arquivo:
            data = json.load(arquivo)
        self.Gestures = list(data.keys())
        self.razao_min_pinca = 0.35
        self.razao_min_fechado = 0.3
        self.executor = Comands()

    def __calcular_distancia(self, p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    def __pontos_dedos(self, landmarks):
        self.landmark = {
            "pulso": landmarks[0], 
            "base_medio": landmarks[9], 
            "ponta_polegar": landmarks[4],
            "ponta_indicador": landmarks[8],
            "ponta_medio": landmarks[12], 
            "ponta_anelar": landmarks[16], 
            "ponta_mindinho": landmarks[20]
        }

    def __tamanho_palma(self):
        self.palma = self.__calcular_distancia(self.landmark["pulso"], self.landmark["base_medio"])

    def recognizer_gesto(self, hand):
        if self.palma == 0:
            return None

        # Distância da pinça
        razao_indicador = self.__calcular_distancia(self.landmark["ponta_polegar"], self.landmark["ponta_indicador"]) / self.palma
        razao_medio = self.__calcular_distancia(self.landmark["ponta_polegar"], self.landmark["ponta_medio"]) / self.palma

        print(razao_indicador)
        print(razao_medio)
        print(hand)

        # Regra de ativação separada por lateralidade
        if hand == "Right":
            if razao_indicador < self.razao_min_pinca:
                self.executor.exec(self.Gestures[0])
                return self.Gestures[0]
            if razao_medio < self.razao_min_pinca:
                self.executor.exec(self.Gestures[1])
                return self.Gestures[1]
        if hand == "Left":
            if razao_indicador < self.razao_min_pinca:
                self.executor.exec(self.Gestures[2])
                return self.Gestures[2]
            if razao_medio < self.razao_min_pinca:
                self.executor.exec(self.Gestures[3])
                return self.Gestures[3]

    def recognizer(self, landmarks, hand):
        self.__pontos_dedos(landmarks)
        self.__tamanho_palma()

        return self.recognizer_gesto(hand)