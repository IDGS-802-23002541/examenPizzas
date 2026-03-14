from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length, NumberRange

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre del Cliente', validators=[DataRequired(), Length(max=100)])
    direccion = StringField('Dirección', validators=[DataRequired(), Length(max=200)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(max=20)])

class PizzaForm(FlaskForm):
    tamanio = SelectField('Tamaño', choices=[
        ('Chica', 'Chica'), 
        ('Mediana', 'Mediana'), 
        ('Grande', 'Grande')
    ])
    ingredientes = StringField('Ingredientes', validators=[DataRequired(), Length(max=200)])
    precio = FloatField('Precio', validators=[DataRequired(), NumberRange(min=0)])

class PedidoForm(FlaskForm):
    id_cliente = SelectField('Cliente', validators=[DataRequired()])
    fecha=DateTimeField('Fecha Pedido', validators=[DataRequired()])
    total = FloatField('Total del Pedido')

class DetallePedidoForm(FlaskForm):
    id_pizza = SelectField('Pizza', coerce=int)
    id_pedido=SelectField('Pedido' )
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)], default=1)
    subtotal=FloatField('Subtotal', validators=[DataRequired()])