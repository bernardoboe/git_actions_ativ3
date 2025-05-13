from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Operações Matemáticas API',
          description='API que realiza soma e multiplicação de dois números',
          doc='/swagger')

ns = api.namespace('operacoes', description='Endpoints matemáticos')

modelo = api.model('Operacao', {
    'num1': fields.Float(required=True, description='Primeiro número'),
    'num2': fields.Float(required=True, description='Segundo número'),
})

@ns.route('/soma')
class Soma(Resource):
    @ns.expect(modelo)
    def post(self):
        """Realiza a soma de dois números"""
        data = request.get_json()
        num1 = data.get('num1')
        num2 = data.get('num2')

        resultado = num1 + num2
        return {'resultado': resultado}
        

@ns.route('/multiplicacao')
class Multiplicacao(Resource):
    @ns.expect(modelo) 
    def post(self):
        """Realiza a multiplicação de dois números"""
        data = request.get_json()
        num1 = data.get('num1')
        num2 = data.get('num2')
        resultado = num1 * num2
        
        return {'resultado': resultado}

if __name__ == '__main__':

    app.run(debug=True)
