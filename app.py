from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# agendar consultas
@app.route('/marcar_consulta')
def marcar_consulta():
    return render_template('marcar_consulta.html')

# relatorio sobre o paciente
@app.route('/ficha')
def ficha():
    return render_template('ficha_paciente.html')

# ver as consultas que foram agendadas
@app.route('/agendadas')
def agendadas():
    return render_template('agendadas.html')