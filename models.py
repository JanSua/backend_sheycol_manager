from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Credential(db.Model):
    __tablename__ = 'credentials'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # 'admin', 'employee', etc.
    role = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return (
            f"<Credential {self.id} | User: {self.username} | Role: {self.role}>"
        )


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # 'pending', 'in progress', etc.
    status = db.Column(db.String(50), nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    created_date = db.Column(db.DateTime, nullable=False,
                             server_default=db.func.now())
    priority = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.String(50), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return (
            f"<Task {self.id}: {self.name} | Status: {self.status} | "
            f"Priority: {self.priority} | Completed: {self.completed}>"
        )


class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False, unique=True)
    company_nit = db.Column(db.String(20), nullable=False, unique=True)
    contact_person = db.Column(db.String(80), nullable=True)
    phone1 = db.Column(db.String(20), nullable=True)
    phone2 = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    # watches, jewelry, etc.
    supplier_type = db.Column(db.String(20), nullable=False, default="other")
    location = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    comments = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return (
            f"<Supplier {self.id}: {self.company_name} | NIT: {self.company_nit} | "
            f"Type: {self.supplier_type} | Active: {self.is_active}>"
        )


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), nullable=False, unique=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey(
        'suppliers.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False,
                           server_default=db.func.now())
    delivery_date = db.Column(db.DateTime, nullable=True)
    total_amount = db.Column(db.Float, nullable=False)
    # pending, received, etc.
    status = db.Column(db.String(50), nullable=False, default="pending")
    comments = db.Column(db.Text, nullable=True)

    supplier = db.relationship(
        'Supplier', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return (
            f"<Order {self.id}: {self.order_number} | Supplier: {self.supplier_id} | "
            f"Status: {self.status} | Total: {self.total_amount}>"
        )


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey(
        'suppliers.id'), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False,
                             server_default=db.func.now())
    amount = db.Column(db.Float, nullable=False)
    # cash, card, etc.
    payment_method = db.Column(
        db.String(50), nullable=False, default="transfer")
    status = db.Column(db.String(50), nullable=False,
                       default="pending")  # pending, completed
    comments = db.Column(db.Text, nullable=True)

    order = db.relationship('Order', backref=db.backref('payments', lazy=True))
    supplier = db.relationship(
        'Supplier', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return (
            f"<Payment {self.id}: Order {self.order_id} | Supplier: {self.supplier_id} | "
            f"Amount: {self.amount} | Status: {self.status}>"
        )


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(200), nullable=True)

    # Información de deuda
    has_pending_balance = db.Column(db.Boolean, default=False)
    pending_balance_amount = db.Column(db.Float, nullable=True)
    pending_since = db.Column(db.Date, nullable=True)

    comments = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return (
            f"<Customer {self.id}: {self.full_name} | Pending: {self.has_pending_balance} | "
            f"Amount: {self.pending_balance_amount}>"
        )
