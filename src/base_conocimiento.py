import json

class BaseConocimiento:
    def __init__(self, filepath):
        self.filepath = filepath
        self.reglas = self.cargar_reglas()

    def cargar_reglas(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    def agregar_regla(self, nueva_regla):
        if not any(regla["sintomas"] == nueva_regla["sintomas"] and regla["diagnostico"] == nueva_regla["diagnostico"] for regla in self.reglas):
            self.reglas.append(nueva_regla)
            self.guardar_reglas()

    def guardar_reglas(self):
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(self.reglas, file, ensure_ascii=False, indent=4)

    def obtener_sintomas_disponibles(self):
        sintomas = set()
        for regla in self.reglas:
            for sintoma in regla['sintomas']:
                sintomas.add(sintoma)
        return list(sintomas)
