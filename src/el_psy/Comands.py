import mouse
import json
from pathlib import Path

class Comands:
    def __init__(self):
        with open(Path(__file__).parent / "gestures_comands.json", 'r') as arquivo:
            self.Comands = json.load(arquivo)

    def exec(self, gesto):
        if not gesto:
            return
        eval(self.Comands[gesto])