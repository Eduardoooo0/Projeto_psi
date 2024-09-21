from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from flask_login import LoginManager, login_required, login_user, logout_user
from models import User, obter_conexao
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'VASCODAGAMA'

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


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

@app.route('/cadastro', methods = ['GET','POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')
    else:
        email = request.form.get('email')
        senha = request.form.get('senha')
        senha_hash = generate_password_hash(senha)
        if not User.exists(email):
            user = User(email=email,senha=senha_hash)
            user.save()
            login_user(user)
            return redirect(url_for('index'))

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = User.get_by_email(email)
        if user and check_password_hash(user['senha'],senha):
            login_user(User.get(user['id']))
            return redirect(url_for('index'))
        else:
            flash('Dados incorretos')
            return render_template('login.html')
