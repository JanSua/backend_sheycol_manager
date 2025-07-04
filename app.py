from flask import Flask, jsonify, request
from flask_migrate import Migrate
from config import Config
from models import db, Credential, Task, Supplier, Order, Payment, Customer
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(Config)

# Configuración de JWT
jwt = JWTManager(app)

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
    # Check if the user already exists
    usuario_existente = Credential.query.filter_by(
        username=data['username']).first()
    if usuario_existente:
        return jsonify({'mensaje': 'El usuario ya existe'}), 400

    nuevo = Credential(username=data['username'],
                       password=data['password'],
                       role=data['role'],
                       )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario creado'}), 201


"""
Funciona únicamente si se hace un GET y devuelve la lista de todos los usuarios.
"""


@app.route('/list-users', methods=['GET'])
def listar_usuarios():
    usuarios = Credential.query.all()
    return jsonify([
        {'id': u.id, 'user': u.username, 'password': u.password, 'role': u.role}
        for u in usuarios
    ])


@app.route('/get-user/<username>', methods=['GET'])
def obtener_usuario(username):
    usuario = Credential.query.filter_by(username=username).first()
    if usuario:
        return jsonify({
            'id': usuario.id,
            'user': usuario.username,
            'password': usuario.password,
            'role': usuario.role
        }), 200
    else:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404


"""
Funciona únicamente si se envía desde el Front el User
"""


@app.route('/delete-user', methods=["POST"])
def eliminar_usuario():
    data = request.json
    usuario_a_eliminar = Credential.query.filter_by(
        username=data['username']).first()
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
    usuario = Credential.query.filter_by(id=data['id']).first()
    if not usuario:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

    cambios = False
    if 'username' in data and usuario.username != data['username']:
        usuario.username = data['username']
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
    current_user = get_jwt_identity()
    data = request.json
    nueva = Task(
        name=data['name'],
        description=data['description'],
        status=data.get('status'),
        due_date=data.get('due_date'),
        created_date=data.get('created_date'),
        priority=data['priority'],
        comments=data.get('comments'),
        created_by=data.get('created_by', current_user['id']),
        completed=data.get('completed', False),
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({'mensaje': 'Tarea creada'}), 201


@app.route('/list-tasks', methods=['GET'])
def listar_tareas():
    tareas = Task.query.all()
    return jsonify([
        {
            'id': t.id,
            'name': t.name,
            'description': t.description,
            'status': t.status,
            'due_date': t.due_date,
            'created_date': t.created_date,
            'priority': t.priority,
            'comments': t.comments,
            'created_by': t.created_by,
            'completed': t.completed
        }
        for t in tareas
    ])


@app.route('/get-task/<int:task_id>', methods=['GET'])
def listar_tarea(task_id):
    tarea = Task.query.filter_by(id=task_id).first()
    if tarea:
        return jsonify({
            'id': tarea.id,
            'name': tarea.name,
            'description': tarea.description,
            'status': tarea.status,
            'due_date': tarea.due_date,
            'created_date': tarea.created_date,
            'priority': tarea.priority,
            'comments': tarea.comments,
            'created_by': tarea.created_by,
            'completed': tarea.completed
        }), 200
    else:
        return jsonify({'mensaje': 'Tarea no encontrada'}), 404


@app.route('/update-task', methods=['POST'])
def actualizar_tarea():
    data = request.json
    tarea = Task.query.filter_by(id=data['id']).first()
    if not tarea:
        return jsonify({'mensaje': 'Tarea no encontrada'}), 404

    cambios = False
    if 'name' in data and tarea.name != data['name']:
        tarea.name = data['name']
        cambios = True
    if 'description' in data and tarea.description != data['description']:
        tarea.description = data['description']
        cambios = True
    if 'status' in data and tarea.status != data['status']:
        tarea.status = data['status']
        cambios = True
    if 'due_date' in data and tarea.due_date != data['due_date']:
        tarea.due_date = data['due_date']
        cambios = True
    if 'priority' in data and tarea.priority != data['priority']:
        tarea.priority = data['priority']
        cambios = True
    if 'comments' in data and tarea.comments != data['comments']:
        tarea.comments = data['comments']
        cambios = True
    if 'created_by' in data and tarea.created_by != data['created_by']:
        tarea.created_by = data['created_by']
        cambios = True
    if 'completed' in data and tarea.completed != data['completed']:
        tarea.completed = data['completed']
        cambios = True

    if cambios:
        db.session.commit()
        return jsonify({'mensaje': 'Tarea actualizada'}), 200
    else:
        return jsonify({'mensaje': 'No hubo cambios'}), 200


@app.route('/delete-task', methods=['POST'])
def eliminar_tarea():
    data = request.json
    tarea = Task.query.filter_by(id=data['id']).first()
    if tarea:
        db.session.delete(tarea)
        db.session.commit()
        return jsonify({'mensaje': 'Tarea eliminada'}), 200
    else:
        return jsonify({'mensaje': 'Tarea no encontrada'}), 404

# Manejo de los Proveedores


@app.route('/create-supplier', methods=['POST'])
def crear_proveedor():
    data = request.json
    nuevo = Supplier(
        company_name=data['company_name'],
        company_nit=data['company_nit'],
        contact_person=data.get('contact_person'),
        phone1=data.get('phone1'),
        phone2=data.get('phone2'),
        email=data.get('email'),
        supplier_type=data.get('supplier_type', 'other'),
        location=data.get('location'),
        address=data.get('address'),
        comments=data.get('comments'),
        is_active=data.get('is_active', True)
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Proveedor creado'}), 201


@app.route('/list-suppliers', methods=['GET'])
def listar_proveedores():
    proveedores = Supplier.query.all()
    return jsonify([
        {
            'id': p.id,
            'company_name': p.company_name,
            'company_nit': p.company_nit,
            'contact_person': p.contact_person,
            'phone1': p.phone1,
            'phone2': p.phone2,
            'email': p.email,
            'supplier_type': p.supplier_type,
            'location': p.location,
            'address': p.address,
            'is_active': p.is_active
        }
        for p in proveedores
    ])


@app.route('/get-supplier/<int:supplier_id>', methods=['GET'])
def obtener_proveedor(supplier_id):
    proveedor = Supplier.query.filter_by(id=supplier_id).first()
    if proveedor:
        return jsonify({
            'id': proveedor.id,
            'company_name': proveedor.company_name,
            'company_nit': proveedor.company_nit,
            'contact_person': proveedor.contact_person,
            'phone1': proveedor.phone1,
            'phone2': proveedor.phone2,
            'email': proveedor.email,
            'supplier_type': proveedor.supplier_type,
            'location': proveedor.location,
            'address': proveedor.address,
            'is_active': proveedor.is_active
        }), 200
    else:
        return jsonify({'mensaje': 'Proveedor no encontrado'}), 404


@app.route('/update-supplier', methods=['POST'])
def actualizar_proveedor():
    data = request.json
    proveedor = Supplier.query.filter_by(id=data['id']).first()
    if not proveedor:
        return jsonify({'mensaje': 'Proveedor no encontrado'}), 404

    if 'company_name' in data:
        proveedor.company_name = data['company_name']
    if 'company_nit' in data:
        proveedor.company_nit = data['company_nit']
    if 'contact_person' in data:
        proveedor.contact_person = data['contact_person']
    if 'phone1' in data:
        proveedor.phone1 = data['phone1']
    if 'phone2' in data:
        proveedor.phone2 = data['phone2']
    if 'email' in data:
        proveedor.email = data['email']
    if 'supplier_type' in data:
        proveedor.supplier_type = data['supplier_type']
    if 'location' in data:
        proveedor.location = data['location']
    if 'address' in data:
        proveedor.address = data['address']
    if 'is_active' in data:
        proveedor.is_active = data['is_active']

    db.session.commit()
    return jsonify({'mensaje': 'Proveedor actualizado'}), 200


@app.route('/delete-supplier', methods=['POST'])
def eliminar_proveedor():
    data = request.json
    proveedor = Supplier.query.filter_by(id=data['id']).first()
    if proveedor:
        db.session.delete(proveedor)
        db.session.commit()
        return jsonify({'mensaje': 'Proveedor eliminado'}), 200
    else:
        return jsonify({'mensaje': 'Proveedor no encontrado'}), 404

# Manejo de las Órdenes


@app.route('/create-order', methods=['POST'])
def crear_orden():
    data = request.json
    nueva = Order(
        order_number=data['order_number'],
        supplier_id=data['supplier_id'],
        order_date=data.get('order_date'),
        delivery_date=data.get('delivery_date'),
        total_amount=data['total_amount'],
        status=data.get('status', 'pending'),
        comments=data.get('comments')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({'mensaje': 'Orden creada'}), 201


@app.route('/list-orders', methods=['GET'])
def listar_ordenes():
    ordenes = Order.query.all()
    return jsonify([
        {
            'id': o.id,
            'order_number': o.order_number,
            'supplier_id': o.supplier_id,
            'supplier_name': o.supplier.company_name,
            'order_date': o.order_date,
            'delivery_date': o.delivery_date,
            'total_amount': o.total_amount,
            'status': o.status,
            'comments': o.comments
        }
        for o in ordenes
    ])


@app.route('/get-order/<int:order_id>', methods=['GET'])
def obtener_orden(order_id):
    orden = Order.query.filter_by(id=order_id).first()
    if orden:
        return jsonify({
            'id': orden.id,
            'order_number': orden.order_number,
            'supplier_id': orden.supplier_id,
            'supplier_name': orden.supplier.company_name,
            'order_date': orden.order_date,
            'delivery_date': orden.delivery_date,
            'total_amount': orden.total_amount,
            'status': orden.status,
            'comments': orden.comments
        }), 200
    else:
        return jsonify({'mensaje': 'Orden no encontrada'}), 404


@app.route('/update-order', methods=['POST'])
def actualizar_orden():
    data = request.json
    orden = Order.query.filter_by(id=data['id']).first()
    if not orden:
        return jsonify({'mensaje': 'Orden no encontrada'}), 404

    if 'order_number' in data:
        orden.order_number = data['order_number']
    if 'supplier_id' in data:
        orden.supplier_id = data['supplier_id']
    if 'order_date' in data:
        orden.order_date = data['order_date']
    if 'delivery_date' in data:
        orden.delivery_date = data['delivery_date']
    if 'total_amount' in data:
        orden.total_amount = data['total_amount']
    if 'status' in data:
        orden.status = data['status']
    if 'comments' in data:
        orden.comments = data['comments']

    db.session.commit()
    return jsonify({'mensaje': 'Orden actualizada'}), 200


@app.route('/delete-order', methods=['POST'])
def eliminar_orden():
    data = request.json
    orden = Order.query.filter_by(id=data['id']).first()
    if orden:
        db.session.delete(orden)
        db.session.commit()
        return jsonify({'mensaje': 'Orden eliminada'}), 200
    else:
        return jsonify({'mensaje': 'Orden no encontrada'}), 404

# Manejo de los Pagos


@app.route('/create-payment', methods=['POST'])
def crear_pago():
    data = request.json
    nuevo = Payment(
        order_id=data['order_id'],
        supplier_id=data['supplier_id'],
        payment_date=data.get('payment_date'),
        amount=data['amount'],
        payment_method=data.get('payment_method', 'transfer'),
        status=data.get('status', 'pending'),
        comments=data.get('comments')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Pago creado'}), 201


@app.route('/list-payments', methods=['GET'])
def listar_pagos():
    pagos = Payment.query.all()
    return jsonify([
        {
            'id': p.id,
            'order_id': p.order_id,
            'supplier_id': p.supplier_id,
            'supplier_name': p.supplier.company_name,
            'payment_date': p.payment_date,
            'amount': p.amount,
            'payment_method': p.payment_method,
            'status': p.status,
            'comments': p.comments
        }
        for p in pagos
    ])


@app.route('/get-payment/<int:payment_id>', methods=['GET'])
def obtener_pago(payment_id):
    pago = Payment.query.filter_by(id=payment_id).first()
    if pago:
        return jsonify({
            'id': pago.id,
            'order_id': pago.order_id,
            'supplier_id': pago.supplier_id,
            'supplier_name': pago.supplier.company_name,
            'payment_date': pago.payment_date,
            'amount': pago.amount,
            'payment_method': pago.payment_method,
            'status': pago.status,
            'comments': pago.comments
        }), 200
    else:
        return jsonify({'mensaje': 'Pago no encontrado'}), 404


@app.route('/update-payment', methods=['POST'])
def actualizar_pago():
    data = request.json
    pago = Payment.query.filter_by(id=data['id']).first()
    if not pago:
        return jsonify({'mensaje': 'Pago no encontrado'}), 404

    if 'order_id' in data:
        pago.order_id = data['order_id']
    if 'supplier_id' in data:
        pago.supplier_id = data['supplier_id']
    if 'payment_date' in data:
        pago.payment_date = data['payment_date']
    if 'amount' in data:
        pago.amount = data['amount']
    if 'payment_method' in data:
        pago.payment_method = data['payment_method']
    if 'status' in data:
        pago.status = data['status']
    if 'comments' in data:
        pago.comments = data['comments']

    db.session.commit()
    return jsonify({'mensaje': 'Pago actualizado'}), 200


@app.route('/delete-payment', methods=['POST'])
def eliminar_pago():
    data = request.json
    pago = Payment.query.filter_by(id=data['id']).first()
    if pago:
        db.session.delete(pago)
        db.session.commit()
        return jsonify({'mensaje': 'Pago eliminado'}), 200
    else:
        return jsonify({'mensaje': 'Pago no encontrado'}), 404

# Manejo de los Clientes


@app.route('/create-customer', methods=['POST'])
def crear_cliente():
    data = request.json
    nuevo = Customer(
        full_name=data['full_name'],
        phone=data.get('phone'),
        email=data.get('email'),
        address=data.get('address'),
        has_pending_balance=data.get('has_pending_balance', False),
        pending_balance_amount=data.get('pending_balance_amount'),
        pending_since=data.get('pending_since'),
        comments=data.get('comments')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Cliente creado'}), 201


@app.route('/list-customers', methods=['GET'])
def listar_clientes():
    clientes = Customer.query.all()
    return jsonify([
        {
            'id': c.id,
            'full_name': c.full_name,
            'phone': c.phone,
            'email': c.email,
            'address': c.address,
            'has_pending_balance': c.has_pending_balance,
            'pending_balance_amount': c.pending_balance_amount,
            'pending_since': c.pending_since,
            'comments': c.comments
        }
        for c in clientes
    ])


@app.route('/get-customer/<int:customer_id>', methods=['GET'])
def obtener_cliente(customer_id):
    cliente = Customer.query.filter_by(id=customer_id).first()
    if cliente:
        return jsonify({
            'id': cliente.id,
            'full_name': cliente.full_name,
            'phone': cliente.phone,
            'email': cliente.email,
            'address': cliente.address,
            'has_pending_balance': cliente.has_pending_balance,
            'pending_balance_amount': cliente.pending_balance_amount,
            'pending_since': cliente.pending_since,
            'comments': cliente.comments
        }), 200
    else:
        return jsonify({'mensaje': 'Cliente no encontrado'}), 404


@app.route('/update-customer', methods=['POST'])
def actualizar_cliente():
    data = request.json
    cliente = Customer.query.filter_by(id=data['id']).first()
    if not cliente:
        return jsonify({'mensaje': 'Cliente no encontrado'}), 404

    if 'full_name' in data:
        cliente.full_name = data['full_name']
    if 'phone' in data:
        cliente.phone = data['phone']
    if 'email' in data:
        cliente.email = data['email']
    if 'address' in data:
        cliente.address = data['address']
    if 'has_pending_balance' in data:
        cliente.has_pending_balance = data['has_pending_balance']
    if 'pending_balance_amount' in data:
        cliente.pending_balance_amount = data['pending_balance_amount']
    if 'pending_since' in data:
        cliente.pending_since = data['pending_since']
    if 'comments' in data:
        cliente.comments = data['comments']

    db.session.commit()
    return jsonify({'mensaje': 'Cliente actualizado'}), 200


@app.route('/delete-customer', methods=['POST'])
def eliminar_cliente():
    data = request.json
    cliente = Customer.query.filter_by(id=data['id']).first()
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({'mensaje': 'Cliente eliminado'}), 200
    else:
        return jsonify({'mensaje': 'Cliente no encontrado'}), 404


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    usuario = Credential.query.filter_by(username=username).first()
    if not usuario:
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404

    if usuario.password != password:
        return jsonify({'mensaje': 'Contraseña incorrecta'}), 401

    access_token = create_access_token(
        identity={"id": usuario.id, "role": usuario.role})
    return jsonify({
        'mensaje': 'Login exitoso',
        'role': usuario.role,
        'access_token': access_token
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
