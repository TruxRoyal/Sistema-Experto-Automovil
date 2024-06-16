import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from base_conocimiento import BaseConocimiento
from motor_inferencia import MotorInferencia
from interfaz import Interfaz

def main():
    base_conocimiento = BaseConocimiento('data/reglas.json')
    motor_inferencia = MotorInferencia(base_conocimiento.reglas)
    interfaz = Interfaz(motor_inferencia)
    interfaz.iniciar()

if __name__ == "__main__":
    main()
