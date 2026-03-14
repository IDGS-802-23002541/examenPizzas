from flask_sqlalchemy import SQLAlchemy
import datetime

db=SQLAlchemy()

class Pizza(db.Model):
    __tablename__='pizza'
    id=db.Column(db.Integer, primary_key=True)
    tamanio=db.Column(db.String(20))
    ingredientes=db.Column(db.String(200))
    precio=db.Column(db.Float)

    pedidos=db.relationship(
        'Pedido',
        secondary='detallepedido',
        back_populates='pizzas'
    )


class Cliente(db.Model):
    __tablename__='cliente'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100))
    direccion=db.Column(db.String(200))
    telefono=db.Column(db.String(20))

    pedidos=db.relationship(
        'Pedido',
        back_populates='cliente'
    )


class Pedido(db.Model):
    __tablename__='pedido'
    id=db.Column(db.Integer, primary_key=True)
    id_cliente=db.Column(
        db.Integer,
        db.ForeignKey('cliente.id'),
        nullable=False
    )
    fecha=db.Column(db.DateTime, server_default=db.func.now())
    total=db.Column(db.Float)

    cliente=db.relationship(
        'Cliente',
        back_populates='pedidos'
    )
    pizzas=db.relationship(
        'Pizza',
        secondary='detallepedido',
        back_populates='pedidos'
    )

class DetallePedido(db.Model):
    __tablename__='detallepedido'
    id=db.Column(db.Integer, primary_key=True)
    id_pedido=db.Column(
        db.Integer,
        db.ForeignKey('pedido.id'),
        nullable=True
    )
    id_pizza=db.Column(
        db.Integer,
        db.ForeignKey('pizza.id'),
        nullable=False
    )
    pizza = db.relationship('Pizza')
    cantidad=db.Column(db.Integer, default=1)
    subtotal=db.Column(db.Float)
