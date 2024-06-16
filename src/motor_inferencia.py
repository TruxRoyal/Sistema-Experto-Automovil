import json
from difflib import SequenceMatcher

class MotorInferencia:
    def __init__(self, reglas):
        self.reglas = reglas

    def calcular_similitud(self, sintoma1, sintoma2):
        return SequenceMatcher(None, sintoma1, sintoma2).ratio()

    def diagnosticar(self, sintomas):
        sintomas = [s.lower().strip() for s in sintomas]
        mejor_puntaje = 0
        mejor_diagnostico = None
        mejor_recomendacion = None

        for regla in self.reglas:
            sintomas_regla = [s.lower().strip() for s in regla["sintomas"]]
            coincidencias_exactas = sum(1 for sintoma in sintomas_regla if sintoma in sintomas)
            coincidencias_parciales = sum(self.calcular_similitud(sintoma, s) > 0.5 for sintoma in sintomas_regla for s in sintomas)

            puntaje = coincidencias_exactas * 1.0 + coincidencias_parciales * 0.5 

            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_diagnostico = regla["diagnostico"]
                mejor_recomendacion = regla["recomendacion"]
                
        umbral = 0.5  

        if mejor_puntaje >= umbral:
            return mejor_diagnostico, mejor_recomendacion
        else:
            return None, {
                "pasos": ["Intente proporcionar más detalles sobre los síntomas."],
                "herramientas": [],
                "sintomas_adicionales": [],
                "consideraciones_seguridad": [],
                "recursos": [],
                "nivel_dificultad": "N/A",
                "consulta_profesional": "Consulte a un profesional si no está seguro de cómo proceder."
            }

def cargar_reglas(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        reglas = json.load(file)
    return reglas
