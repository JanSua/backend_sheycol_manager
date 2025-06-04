from flask import Flask, jsonify, request
from flask_migrate import Migrate
from config import Config
from models import db, Credenciales, Tareas
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)  # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
@cross_origin()
def index():
    return '¡!'


# manejo de los usuarios de la aplicación
"""
Funciona si se usa el endpoint create-user como POST, enviando user password y role.
"""


@app.route('/create-user', methods=['POST'])
def crear_usuario():
    data = request.json
    nuevo = Credenciales(user=data['user'],
                         password=data['password'],
                         role=data['role'],
                         )
    print(nuevo)
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario creado'}), 201


"""
Funciona únicamente si se hace un GET y devuelve la lista de todos los usuarios.
"""


@app.route('/list-users', methods=['GET'])
def listar_usuarios():
    usuarios = Credenciales.query.all()
    print(usuarios)
    return jsonify([
        {'id': u.id, 'user': u.user, 'password': u.password, 'role': u.role}
        for u in usuarios
    ])


"""
Funciona únicamente si se envía desde el Front el User
"""


@app.route('/delete-user', methods=["POST"])
def eliminar_usuario():
    data = request.json
    usuario_a_eliminar = Credenciales.query.filter_by(
        user=data['user']).first()
    print(usuario_a_eliminar)
    if usuario_a_eliminar:
        db.session.delete(usuario_a_eliminar)
        db.session.commit()
        return jsonify({'mensaje': 'Usuario eliminado'}), 200
    else:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404


"""
Funciona unicamente si se envía desde el Front el ID y los campos a modificar, los que no se deben modificar se dejan vacíos.
"""


@app.route('/update-user', methods=["POST"])
def actualizar_usuario():

    data = request.json
    usuario = Credenciales.query.filter_by(id=data['id']).first()
    if not usuario:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

    cambios = False
    if 'user' in data and usuario.user != data['user']:
        usuario.user = data['user']
        cambios = True
    if 'password' in data and usuario.password != data['password']:
        usuario.password = data['password']
        cambios = True
    if 'role' in data and usuario.role != data['role']:
        usuario.role = data['role']
        cambios = True

    if cambios:
        db.session.commit()
        return jsonify({'mensaje': 'Usuario actualizado'}), 200
    else:
        return jsonify({'mensaje': 'No hubo cambios'}), 200

# Manejo de las Tareas


@app.route('/create-task', methods=['POST'])
def crear_tarea():
    data = request.json
    nueva = Tareas(name=data['name'],
                   description=data['description'],
                   status=data['status'],
                   date=data['date'],
                   created_date=data['created_date'],
                   prior=data['prior'],
                   comments=data['comments'],
                   created_by=data['created_by'],
                   completed=data['completed'],
                   )
    print(nueva)
    db.session.add(nueva)
    db.session.commit()
    return jsonify({'mensaje': 'Tarea creada'}), 201


@app.route('/list-tasks', methods=['GET'])
def listar_tareas():
    tareas = Tareas.query.all()
    print(tareas)
    return jsonify([
        {'id': u.id, 'nombre': u.name, 'descripción': u.description, 'estado': u.status}
        for u in tareas
    ])


if __name__ == '__main__':
    app.run(debug=True)
