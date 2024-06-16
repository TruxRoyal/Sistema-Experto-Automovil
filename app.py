from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from src.base_conocimiento import BaseConocimiento
from src.motor_inferencia import MotorInferencia
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

base_conocimiento = BaseConocimiento('data/reglas.json')
motor_inferencia = MotorInferencia(base_conocimiento.reglas)

@app.route('/')
def index():
    sintomas_disponibles = base_conocimiento.obtener_sintomas_disponibles()
    return render_template('index.html', sintomas_disponibles=sintomas_disponibles)

@app.route('/registro_sintomas', methods=['POST'])
def registro_sintomas():
    data = request.json
    nombre = data.get('nombre')
    email = data.get('email')
    sintomas = data.get('sintomas')
    if not nombre or not email or not sintomas:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400
    
    diagnostico, recomendacion = motor_inferencia.diagnosticar(sintomas)
    if diagnostico is None:
        return jsonify({"error": "No se pudo determinar el diagnóstico. Intente con más síntomas o busque ayuda profesional."}), 400

    consulta = {
        "nombre": nombre,
        "email": email,
        "sintomas": sintomas,
        "diagnostico": diagnostico,
        "recomendacion": recomendacion
    }

    with open('data/consultas.json', 'a') as f:
        json.dump(consulta, f)
        f.write('\n')

    return jsonify({
        'message': "Síntomas registrados exitosamente",
        'diagnostico': diagnostico,
        'recomendacion': recomendacion
    }), 200

@app.route('/historial', methods=['POST'])
def historial():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email es obligatorio"}), 400
    try:
        with open('data/consultas.json', 'r') as f:
            consultas = [json.loads(line) for line in f]
            consultas_usuario = [consulta for consulta in consultas if consulta.get('email') == email]
        return jsonify(consultas_usuario), 200
    except Exception as e:
        return jsonify({"error": "No se pudo acceder al historial de consultas"}), 500

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin.html', error='Credenciales inválidas')
    return render_template('admin.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    reglas = base_conocimiento.reglas
    return render_template('admin_dashboard.html', reglas=reglas)


@app.route('/admin/update_knowledge_base', methods=['POST'])
def update_knowledge_base():
    if not session.get('admin'):
        return jsonify({"error": "No autorizado"}), 403
    
    data = request.json
    sintomas = data.get('sintomas')
    diagnostico = data.get('diagnostico')
    recomendacion = data.get('recomendacion')
    
    if not sintomas or not diagnostico or not recomendacion:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400
    
    nueva_regla = {
        "sintomas": sintomas,
        "diagnostico": diagnostico,
        "recomendacion": recomendacion
    }
    
    base_conocimiento.agregar_regla(nueva_regla)
    
    return jsonify({"message": "Base de conocimientos actualizada exitosamente"}), 200


if __name__ == "__main__":
    app.run(debug=True)
