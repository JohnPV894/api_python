from flask import Flask, jsonify, request

from flask_pymongo import PyMongo
#from pymongo import MongoCliente


app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb+srv://santiago894:P5wIGtXue8HvPvli@cluster0.6xkz1.mongodb.net'
mongo = PyMongo(app)
usuarios = [
      {"id":1,"nombre":"john"},
      {"id":2,"nombre":"sergio"},
      {"id":3,"nombre":"daniel"},
]


@app.route('/api/users',methods=["GET"])
def obtenerDocumentosColeccion():
    db=mongo.cx.get_database("express")
    coleccion = db.get_collection("estudiantes")
    resultados = coleccion.find()
    devolver = []
    for resultado in resultados:
          devolver.append(resultado)
    return devolver


def is_null(string):
    return string is None or string.strip() == ""

#Buscar usuarios 
@app.route('/api/users/buscar',methods=["POST"])
def prueba():
    nombre = request.args.get('nombre')
    #Validar entrada 
    if is_null(nombre):
        return jsonify({"error": "Debe proporcionar un nombre"}), 401 
    db=mongo.cx.get_database("express")
    coleccion = db.get_collection("estudiantes")
    resultados = coleccion.find({"nombre": nombre})
    devolver = []
    for resultado in resultados:
          devolver.append(resultado)
    if devolver==[]:return jsonify({"error": "no se encontraron coincidencias"}), 200
    return devolver

@app.route('/')
def raiz():
    return 'Funcionando bien'

@app.route('/api/users/',methods=["POST"])
def crearUsuario():
    #Recoger Parametros
    nombre = request.args.get('nombre')
    apellido = request.args.get('apellido')
    telefono = request.args.get('telefono')
    #Validar que no esten nulos
    if is_null(nombre) or is_null(apellido) or is_null(telefono):
      return jsonify("404 Parametros incompletos")
    #Agregar nuevo usuario al lugar de almacenamiento
    usuario={
        "nombre":nombre,
        "apellido":apellido,
        "telefono":telefono
    }
    
    try:
        db=mongo.cx.get_database("express")
        coleccion = db.get_collection("estudiantes")
        resultado = coleccion.insert_one(usuario)
        # Confirmar que se insertó correctamente
        if resultado.inserted_id:
            usuario["_id"] = str(resultado.inserted_id)  # Convertir ObjectId a string para JSON
            return jsonify(usuario), 201
        else:
            return jsonify({"error": "No se pudo insertar el usuario"}), 500

    except Exception as e:
        return jsonify({"error": f"Error en la base de datos: {str(e)}"}), 500


app.run() 
#adaptador a mongo

