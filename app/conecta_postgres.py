import psycopg2
import time
from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Aluno API',
          description='API para conectar e consultar dados no PostgreSQL e realizar operações matemáticas',
          doc='/swagger')

# Mesmo namespace para tudo
ns = api.namespace('alunos', description='Operações de conexão com PostgreSQL e matemáticas')

# Modelo para entrada das operações matemáticas
operacao_model = api.model('Operacao', {
    'num1': fields.Float(required=True, description='Primeiro número'),
    'num2': fields.Float(required=True, description='Segundo número'),
})


def get_connection():
    conn = psycopg2.connect(
        host="db",
        dbname="postgres",
        user="postgres",
        password="senha123"
    )
    return conn


@ns.route('/')
class AlunosList(Resource):
    def get(self):
        time.sleep(5)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alunos(
                id SERIAL PRIMARY KEY,
                nome VARCHAR(50)
            );
        """)
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM alunos;")
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute("INSERT INTO alunos (nome) VALUES ('João'), ('Maria'), ('José');")
            conn.commit()

        cur.execute("SELECT * FROM alunos;")
        alunos = cur.fetchall()
        cur.close()
        conn.close()
        return {'alunos': [{'id': aluno[0], 'nome': aluno[1]} for aluno in alunos]}


@ns.route('/soma')
class Soma(Resource):
    @ns.expect(operacao_model)
    def post(self):
        data = request.get_json()
        resultado = data['num1'] + data['num2']
        return {'resultado': resultado}


@ns.route('/multiplicacao')
class Multiplicacao(Resource):
    @ns.expect(operacao_model)
    def post(self):
        data = request.get_json()
        resultado = data['num1'] * data['num2']
        return {'resultado': resultado}
