import mouse
import tkinter as tk
import json
from pathlib import Path
import time

class Comands:
    def __init__(self):
        with open(Path(__file__).parent / "gestures_comands.json", 'r') as arquivo:
            self.Comands = json.load(arquivo)
        self.x, self.y = None, None
        self.sensibilidade = 1.5
        root = tk.Tk()
        self.LARGURA_TELA = root.winfo_screenwidth()
        self.ALTURA_TELA = root.winfo_screenheight()
        root.destroy()

    def exec(self, gesto):
        if not gesto:
            return
        eval(self.Comands[gesto])
        time.sleep(0.2)

    def cursor(self, x, y):
        # Guarda a primeira posição da mão detectada
        if self.x is None or self.y is None:
            self.x = x
            self.y = y
            return

        # Calcula quanto a mão se moveu desde o quadro anterior
        dx = (self.x - x) * self.LARGURA_TELA
        dy = (y - self.y) * self.ALTURA_TELA

        # Suavização e conversão para deslocamento inteiro
        dx = int(dx * self.sensibilidade)
        dy = int(dy * self.sensibilidade)

        # Move o cursor relativamente à posição atual
        mouse.move(dx, dy, absolute=False)

        # Atualiza a posição da mão para o próximo quadro
        self.x = x
        self.y = y
