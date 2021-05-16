from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:170204021@localhost/flaskmysql5'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Mudanza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    propietario = db.Column(db.String(50), unique=True)
    origen = db.Column(db.String(70), unique=True)
    destino = db.Column(db.String(70), unique=True)
    fecha = db.Column(db.DateTime)
    fecha_llegada = db.Column(db.DateTime)

    def __init__(self, propietario, origen, destino, fecha, fecha_llegada):
        self.propietario = propietario
        self.origen = origen
        self.destino = destino
        self.fecha = fecha
        self.fecha_llegada = fecha_llegada

db.create_all()

class EsquemaMudanza(ma.Schema):
    class Meta:
        fields = ('id', 'propietario', 'origen', 'destino', 'fecha', 'fecha_llegada')

esquema_mudanza = EsquemaMudanza()
esquemas_mudanza = EsquemaMudanza(many=True)

@app.route('/mudanzas', methods=['POST'])
def crear_mudanza():
    propietario = request.json['propietario']
    origen = request.json['origen']
    destino = request.json['destino']
    fecha = request.json['fecha']
    hora = request.json['fecha_llegada']
    nueva_mudanza= Mudanza(propietario, origen, destino, fecha, hora)
    db.session.add(nueva_mudanza)
    db.session.commit()
    return esquema_mudanza.jsonify(nueva_mudanza)

@app.route('/mudanzas', methods=['GET'])
def obtener_mudanzas():
    todas_las_mudanzas = Mudanza.query.all()
    resultado = esquemas_mudanza.dump(todas_las_mudanzas)
    return jsonify(resultado)

@app.route('/mudanzas/<id>', methods=['GET'])
def obtener_una_mudanza(id):
    una_mudanza = Mudanza.query.get(id)
    return esquema_mudanza.jsonify(una_mudanza)

if __name__ == "__main__":
    app.run(debug=True)
