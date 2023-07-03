from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user:password@localhost/clientes'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/clientes'
# URL de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


# defino la tabla
class Clientes(db.Model):   # la clase Cliente hereda de db.Model (variable db creada como SQLAlchemy)   
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nomape=db.Column(db.String(100))
    edad=db.Column(db.Integer)
    dni=db.Column(db.Integer)
    direccion=db.Column(db.String(100))
    sueldo=db.Column(db.Integer)
    imagen=db.Column(db.String(400))

    def __init__(self,nomape,edad,dni,direccion,sueldo,imagen):   #crea el  constructor de la clase
        self.nomape=nomape   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.edad=edad
        self.dni=dni
        self.direccion=direccion
        self.sueldo=sueldo
        self.imagen=imagen
        
    #  si hay que crear mas tablas , se hace aqui

with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class ClientesSchema(ma.Schema): #variable ma creada como Marshmallow
    class Meta:
        fields=('id','nomape','edad','dni','direccion','sueldo','imagen')




cliente_schema=ClientesSchema()            # El objeto producto_schema es para traer un producto
clientes_schema=ClientesSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto


# crea los endpoint o rutas (json) ****CONSULTA TODOS
@app.route('/clientes',methods=['GET'])
def get_Clientes():
    all_clientes=Clientes.query.all()         # el metodo query.all() lo hereda de db.Model
    result=clientes_schema.dump(all_clientes)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla




@app.route('/clientes/<id>',methods=['GET']) #CONSULTA UN REGISTRO
def get_cliente(id):
    cliente=Clientes.query.get(id)
    return cliente_schema.jsonify(cliente)   # retorna el JSON de un producto recibido como parametro




@app.route('/clientes/<id>',methods=['DELETE'])#BORRA UN REGISTRO POR ID
def delete_cliente(id):
    cliente=Clientes.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    return cliente_schema.jsonify(cliente)   # me devuelve un json con el registro eliminado


@app.route('/clientes', methods=['POST']) # crea ruta o endpoint #ALTA DE REGISTRO
def create_cliente():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nomape=request.json['nomape']
    edad=request.json['edad']
    dni=request.json['dni']
    direccion=request.json['direccion']
    sueldo=request.json['sueldo']
    imagen=request.json['imagen']
    new_cliente=Clientes(nomape,edad,dni,direccion,sueldo,imagen)
    db.session.add(new_cliente)
    db.session.commit()
    return cliente_schema.jsonify(new_cliente) #devuelve el registro creado


@app.route('/clientes/<id>' ,methods=['PUT']) #MODIFICA REGISTRO
def update_cliente(id):
    cliente=Clientes.query.get(id)
 
    cliente.nomape=request.json['nomape']
    cliente.edad=request.json['edad']
    cliente.dni=request.json['dni']
    cliente.direccion=request.json['direccion']
    cliente.sueldo=request.json['sueldo']
    cliente.imagen=request.json['imagen']


    db.session.commit()
    return cliente_schema.jsonify(cliente) #devuelve registro modificado
 


# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000