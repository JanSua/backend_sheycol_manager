from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Credenciales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return (
            f'<Id: {self.id}>'
            f'<Usuario: {self.user}> | <Contraseña: {self.password[0]}...{self.password[len(self.password)-1]}>'
            f'<Rol: {self.role}>'
        )


class Tareas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=True)
    date = db.Column(db.Date, nullable=True)
    created_date = db.Column(db.DateTime, nullable=False)
    prior = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.String(50), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return (
            f"<Tarea {self.id}: {self.name} | Estado: {self.status} | "
            f"Prioridad: {self.prior}"
            f"Completada: {self.completed}>"
        )
