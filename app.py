import sqlite3
from datetime import datetime
from sqlite3 import IntegrityError

import flask
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/aluguer.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    firstname = db.Column(db.String(200))

class Reserva(db.Model):
    __tablename__ = "reservas"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    veiculo = db.Column(db.String(50))
    valorDiaria = db.Column(db.Integer)
    dataInicio = db.Column(db.Date)
    dataFim = db.Column(db.Date)
    dias = db.Column(db.Integer)
    total = db.Column(db.Integer)

class Veiculo(db.Model):
    __tablename__ = "veiculos"
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(50), primary_key=True)
    tipo = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    transmissao = db.Column(db.String(50))
    quantidadePessoas = db.Column(db.Integer)
    imagem = db.Column(db.String(50))
    extensao = db.Column(db.String(50))
    revisao = db.Column(db.Integer)
    revisaoProx = db.Column(db.Integer)
    legalizacao = db.Column(db.Integer)
    valorDiaria = db.Column(db.Integer)

class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cartao = db.Column(db.Integer)
    multibanco = db.Column(db.Integer)
    paypal = db.Column(db.Integer)

with app.app_context():
    db.create_all()
    #db.session.commit()

carro = [{"tipo": "Carro", "marca": "Honda", "transmissão": "Automático", "categoria": "Médio",
              "Quantidade de pessoas": "5", "Valor da diária": 58, "imagem": "civic1", "Modelo": "Civic", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 1234567890 },
             {"tipo": "Carro", "marca": "Opel", "transmissão": "Manual", "categoria": "Pequeno",
              "Quantidade de pessoas": "5", "Valor da diária": 32, "imagem": "onix", "Modelo": "Onix", "extensao": "png", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 1234567891 },
             {"tipo": "Carro", "marca": "Volkswagen", "transmissão": "Manual", "categoria": "Pequeno",
              "Quantidade de pessoas": "5", "Valor da diária": 32, "imagem": "polo", "Modelo": "Polo", "extensao": "webp", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 1234567892 },
             {"tipo": "Carro", "marca": "Hyundai", "transmissão": "Automático", "categoria": "SUV",
              "Quantidade de pessoas": "5", "Valor da diária": 85, "imagem": "santafe", "Modelo": "Santa Fé", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 1234567893 },
             {"tipo": "Carro", "marca": "BMW", "transmissão": "Automático", "categoria": "Luxo",
              "Quantidade de pessoas": "5", "Valor da diária": 90, "imagem": "schnitzer3", "Modelo": "X1 AC", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 1234567894 },
             {"tipo": "Carro", "marca": "BMW", "transmissão": "Automático", "categoria": "SUV",
              "Quantidade de pessoas": "5", "Valor da diária": 85, "imagem": "X1E84", "Modelo": "X1 E84", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 1234567895 },
             {"tipo": "Carro", "marca": "Tesla", "transmissão": "Automático", "categoria": "Luxo",
              "Quantidade de pessoas": "5", "Valor da diária": 98, "imagem": "y", "Modelo": "y", "extensao": "jfif", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 1234567896 },
             {"tipo": "Carro", "marca": "Aston Martin", "transmissão": "Automático", "categoria": "Luxo",
              "Quantidade de pessoas": "5", "Valor da diária": 120, "imagem": "hyundai", "Modelo": "EQ900", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 1234567897 },
             {"tipo": "Carro", "marca": "Toyota", "transmissão": "Automático", "categoria": "SUV",
              "Quantidade de pessoas": "5", "Valor da diária": 85, "imagem": "tpyotasw4", "Modelo": "SW4", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 1234567898 },
             {"tipo": "Carro", "marca": "Lamborghini", "transmissão": "Automático", "categoria": "Luxo",
              "Quantidade de pessoas": "2", "Valor da diária": 280, "imagem": "lamborghini1", "Modelo": "SC18", "extensao": "jfif", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 1234567899 },
             {"tipo": "Carro", "marca": "Ranger Rover", "transmissão": "Automático", "categoria": "SUV",
              "Quantidade de pessoas": "5", "Valor da diária": 170, "imagem": "rangerover", "Modelo": "Evoque", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 2234567890 },
             {"tipo": "Carro", "marca": "Volkswagen", "transmissão": "Automático", "categoria": "Grande",
              "Quantidade de pessoas": "5", "Valor da diária": 77, "imagem": "amarok", "Modelo": "Amarok", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 1334567890 }]

moto = [{"tipo": "Moto", "marca": "Honda", "transmissão": "Manual", "categoria": "Pequeno",
         "Quantidade de pessoas": "2", "Valor da diária": 12, "imagem": "biz", "Modelo": "biz", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 3234567890 },
        {"tipo": "Moto", "marca": "Guzzi", "transmissão": "Manual", "categoria": "Luxo",
         "Quantidade de pessoas": "2", "Valor da diária": 54, "imagem": "guzzi1400", "Modelo": "Audace", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 3234567891 },
        {"tipo": "Moto", "marca": "Honda", "transmissão": "Manual", "categoria": "Luxo",
         "Quantidade de pessoas": "2", "Valor da diária": 54, "imagem": "HondaCBR600RR", "Modelo": "CBR", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 3234567892},
        {"tipo": "Moto", "marca": "Honda", "transmissão": "Manual", "categoria": "Média",
         "Quantidade de pessoas": "2", "Valor da diária": 22, "imagem": "HondaCG160", "Modelo": "CG", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 3234567893},
        {"tipo": "Moto", "marca": "Suzuki", "transmissão": "Manual", "categoria": "Grande",
         "Quantidade de pessoas": "2", "Valor da diária": 28, "imagem": "suzukiGSX-R600", "Modelo": "GSX", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 3234567894},
        {"tipo": "Moto", "marca": "Vespa", "transmissão": "Manual", "categoria": "Pequeno",
         "Quantidade de pessoas": "2", "Valor da diária": 12, "imagem": "VESPA", "Modelo": "GTS", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 3234567895},
        {"tipo": "Moto", "marca": "Yamaha", "transmissão": "Manual", "categoria": "Médio",
         "Quantidade de pessoas": "2", "Valor da diária": 22, "imagem": "yamahayfm250", "Modelo": "YFM", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 3234567896},
        {"tipo": "Moto", "marca": "BMW", "transmissão": "Automática", "categoria": "Luxo",
         "Quantidade de pessoas": "2", "Valor da diária": 54, "imagem": "bmw", "Modelo": "S", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 3234567897},
        {"tipo": "Moto", "marca": "Honda", "transmissão": "Manual", "categoria": "Grande",
         "Quantidade de pessoas": "2", "Valor da diária": 28, "imagem": "hondahornet", "Modelo": "Hornet", "extensao": "jpg", "revisao" : 82024, "revisaoProx": 82025, "legalizacao" : 3234567898} ]


def inserir_veiculos():
    veiculos_existentes = Veiculo.query.all()
    modelos_existentes = {veiculo.modelo for veiculo in veiculos_existentes}

    for v in carro + moto:
        if v['Modelo'] not in modelos_existentes:
            novo_veiculo = Veiculo(
                tipo=v['tipo'],
                marca=v['marca'],
                modelo=v['Modelo'],
                categoria=v['categoria'],
                transmissao=v['transmissão'],
                quantidadePessoas=int(v['Quantidade de pessoas']),
                imagem=v['imagem'],
                extensao=v['extensao'],
                revisao=v['revisao'],
                revisaoProx=v['revisaoProx'],
                legalizacao=v['legalizacao'],
                valorDiaria=v['Valor da diária'])
            db.session.add(novo_veiculo)
    db.session.commit()

with app.app_context():
    db.create_all()
    inserir_veiculos()


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(username=email).first()
        print(f"Usuário encontrado: {user}")

        if user and check_password_hash(user.password, password):
            session['firstname'] = user.firstname
            session['user_id'] = user.id
            print(f"Usuário autenticado: {email}")
            return redirect(url_for("home"))
        else:
            print("Falha na autenticação: Usuário ou senha inválidos.")
            return render_template("login.html", message="Usuário ou senha inválidos")
    return render_template("login.html")


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            print("Esse usuário já está em uso. Por favor escolha outro.")
            session['message'] = "Esse usuário já está em uso. Por favor escolha outro."
            return redirect(url_for('cadastro'))
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, firstname=firstname)
            try:
                db.session.add(new_user)
                db.session.commit()
                print("Usuário criado com sucesso.")
                session['message'] = "O seu cadastro foi feito com sucesso"
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                print("Erro ao criar usuário: usuário já existe.")
                session['message'] = "Erro ao criar usuário: usuário já existe."
                return redirect(url_for('cadastro'))

    return render_template('cadastro.html', message=session.pop('message', None))

@app.route('/verificar_cadastro', methods=['POST'])
def verificar_cadastro():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if user:
        return "Usuário já cadastrado!"
    else:
        return "Usuário ainda não cadastrado"


def buscar_veiculos(pesquisa=None, marca=None, transmissao=None, categoria=None, valor_diaria=None):
    query = Veiculo.query

    data_inicio_str = session.get('dataInicio')
    data_fim_str = session.get('dataFim')

    data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d') if data_inicio_str else None
    data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d') if data_fim_str else None

    reservas_feitas = []
    if data_inicio and data_fim:
        reservas_feitas = Reserva.query.filter(
            (data_fim >= Reserva.dataInicio) &
            (data_inicio <= Reserva.dataFim)).all()

    modelos_reservados = {reserva.veiculo for reserva in reservas_feitas}
    if pesquisa:
        query = query.filter(
            (Veiculo.marca.ilike(f'%{pesquisa}%')) |
            (Veiculo.modelo.ilike(f'%{pesquisa}%')))

    if marca:
        query = query.filter(Veiculo.marca.ilike(f'%{marca}%'))

    if transmissao:
        query = query.filter(Veiculo.transmissao.ilike(f'%{transmissao}%'))

    if categoria:
        query = query.filter(Veiculo.categoria.ilike(f'%{categoria}%'))

    if valor_diaria:
        query = query.filter(Veiculo.valorDiaria == valor_diaria)

    resultados_carros = query.filter(Veiculo.tipo == "Carro", ~Veiculo.modelo.in_(modelos_reservados)).all()
    resultados_motos = query.filter(Veiculo.tipo == "Moto", ~Veiculo.modelo.in_(modelos_reservados)).all()
    print("Dados de pesquisa:", pesquisa, marca, transmissao, categoria, valor_diaria)
    return {"carros": resultados_carros, "motos": resultados_motos}


@app.route('/armazenar_datas', methods=['POST'])
def armazenar_datas():
    data = request.get_json()
    data_inicio = data.get('dataInicio')
    data_fim = data.get('dataFim')

    session['dataInicio'] = data_inicio
    session['dataFim'] = data_fim

    return jsonify({"message": "Datas armazenadas com sucesso!"}), 200


@app.route('/reserva/<modelo>', methods=['GET'])
def obter_reserva(modelo):
    veiculo = Veiculo.query.filter_by(modelo=modelo).first()
    if veiculo:
        return jsonify({
            'veiculo': veiculo.modelo,
            'valor_diaria': veiculo.valorDiaria,
            'marca': veiculo.marca,
            'tipo': veiculo.tipo})
    return jsonify({'error': 'Veículo não encontrado'}), 404


@app.route('/pagamento', methods=['GET', 'POST'])
def pagamento():
    if request.method == 'POST':
        print("Dados recebidos:", request.form)
        if 'user_id' not in session:
            return jsonify({'error': 'Usuário não autenticado.'}), 403

        modelo = request.form.get('modelo')
        valor_diaria_str = request.form.get('valorDiaria')

        if valor_diaria_str is None or valor_diaria_str == '':
            return "Valor da diária não foi passado", 400

        try:
            valor_diaria = int(valor_diaria_str)
        except ValueError:
            return "Valor da diária inválido", 400

        dias = int(request.form.get('dias'))
        total = valor_diaria * dias
        data_inicio_str = session.get('dataInicio')
        data_fim_str = session.get('dataFim')


        data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date() if data_inicio_str else None
        data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date() if data_fim_str else None
        reserva_existente = Reserva.query.filter_by(veiculo=modelo, user_id=session['user_id']).filter(
            (data_fim >= Reserva.dataInicio) &
            (data_inicio <= Reserva.dataFim)).first()

        if reserva_existente:

            return redirect(url_for('minhas_reservas'))

        nova_reserva = Reserva(
            user_id=session['user_id'],
            veiculo=modelo,
            valorDiaria=valor_diaria,
            dataInicio=data_inicio,
            dataFim=data_fim,
            dias=dias,
            total=total)

        try:
            db.session.add(nova_reserva)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


        return redirect(url_for('minhas_reservas'))

    modelo = request.args.get('modelo')
    valor_diaria = request.args.get('valorDiaria')

    if valor_diaria is None:
        return "Valor da diária não foi passado", 400
    try:
        valor_diaria = int(valor_diaria)
    except ValueError:
        return "Valor da diária inválido", 400

    data_inicio_str = session.get('dataInicio')
    data_fim_str = session.get('dataFim')
    data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d')
    data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d')

    dias = (data_fim - data_inicio).days
    print(f"Valor da diária: {valor_diaria}")

    return render_template('pagamento.html', modelo=modelo, valor_diaria=valor_diaria, dias=dias,
                           data_inicio=data_inicio, data_fim=data_fim)


@app.route('/index', methods=['GET', 'POST'])
def index():
    print("Acesso à rota /index")

    valor_diaria_str = request.form.get('valorDiaria', None)
    search_input = request.args.get('search_input', '')
    marca = request.form.get('marca', None)
    transmissao = request.form.get('transmissao', None)
    categoria = request.form.get('categoria', None)
    print("Valor da diária recebido:", valor_diaria_str)

    if request.method == 'POST':
        valor_diaria_str = request.form.get('valorDiaria')

    if valor_diaria_str is None or valor_diaria_str == '':
        return "Valor da diária não foi passado", 400

    try:
        valor_diaria = int(valor_diaria_str)
    except ValueError:
        return "Valor da diária inválido", 400

    else:
        valor_diaria_str = session.get('valorDiaria')
        if valor_diaria_str is not None:
            valor_diaria = int(valor_diaria_str)

    resultados = buscar_veiculos(search_input, marca, transmissao, categoria, valor_diaria)
    print("Metodo:", request.method)
    print("Form Data:", request.form)

    if resultados is None:
        resultados = {"carros": [], "motos": []}
    return render_template('index.html', resultados=resultados)


@app.route('/reservas')
def minhas_reservas():
    if 'firstname' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(firstname=session['firstname']).first()

    reservas = Reserva.query.filter_by(user_id=user.id).all()

    return render_template('reservas.html', reservas=reservas)

@app.route('/reservas', methods=['POST'])
def reservar():
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado.'}), 403

    data = request.json
    print("Dados recebidos:", data)

    user_id = session['user_id']
    user = User.query.get(user_id)
    reservas_conflito = Reserva.query.filter_by(veiculo=data['veiculo']).filter(
        (data['dataFim'] >= Reserva.dataInicio) &
        (data['dataInicio'] <= data['dataFim'])).first()

    if reservas_conflito:
        return jsonify({'error': 'Este veículo já está reservado nessas datas.'}), 400

    if user:
        dataInicio = datetime.strptime(data['dataInicio'], '%Y-%m-%d').date()
        dataFim = datetime.strptime(data['dataFim'], '%Y-%m-%d').date()

        nova_reserva = Reserva(
            veiculo=data['veiculo'],
            valorDiaria=data['valorDiaria'],
            dataInicio=dataInicio,
            dataFim=dataFim,
            dias=data['dias'],
            total=data['total'],
            user_id=user_id)

        try:
            db.session.add(nova_reserva)
            db.session.commit()
            return jsonify({'message': 'Reserva criada com sucesso!'}), 201
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': 'Erro de integridade, verifique os dados recebidos.'}), 400
        except Exception as e:
            db.session.rollback()
            print("Erro ao criar reserva:", e)
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Usuário não encontrado.'}), 404

@app.route('/editar_reserva/<int:reserva_id>', methods=['POST'])
def editar_reserva(reserva_id):
    reserva = Reserva.query.get(reserva_id)
    if reserva:
        reserva.dataInicio = datetime.strptime(request.form['dataInicio'], '%Y-%m-%d').date()
        reserva.dataFim = datetime.strptime(request.form['dataFim'], '%Y-%m-%d').date()
        reserva.dias = (reserva.dataFim - reserva.dataInicio).days
        reserva.total = reserva.dias * reserva.valorDiaria

        db.session.commit()
        return redirect(url_for('minhas_reservas'))
    return "Reserva não encontrada!"

@app.route('/cancelar_reserva/<int:reserva_id>', methods=['POST'])
def cancelar_reserva(reserva_id):
    reserva = Reserva.query.get(reserva_id)
    if reserva:
        db.session.delete(reserva)
        db.session.commit()
        return redirect(url_for('minhas_reservas'))
    return "Reserva não encontrada!"

@app.route('/', methods=["GET", "POST"])
def home():
    search_input = request.form.get('search_input', '') if request.method == 'POST' else ''
    marca = request.form.get('marca', None)
    transmissao = request.form.get('transmissao', None)
    categoria = request.form.get('categoria', None)
    valor_diaria_input = request.form.get('Valor da diária', None)

    valor_diaria = int(valor_diaria_input) if valor_diaria_input and valor_diaria_input.isdigit() else None
    resultados = buscar_veiculos(search_input, marca, transmissao, categoria, valor_diaria)

    if resultados is None:
        resultados = {"carros": [], "motos": []}

    print("Resultados da busca:", resultados)

    return render_template('index.html', resultados=resultados)


if __name__ == '__main__':
    app.run(debug=True)