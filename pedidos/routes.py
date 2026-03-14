# Blueprint es para manejarlo como módulos
from . import pedidos_bp
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db
from models import Pizza, Cliente, Pedido, DetallePedido
from datetime import date, datetime

import forms

@pedidos_bp.route('/pedidos', methods=['GET'])
def pedidos():
    pedido_form = forms.PedidoForm(request.form)
    fecha_str=request.args.get('fecha', date.today().isoformat())
 
    try:
        fecha_filtro = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except:
        fecha_filtro = date.today()
 
    pedidos_lista = Pedido.query.filter(
        db.func.date(Pedido.fecha) == fecha_filtro
    ).join(Cliente).order_by(Pedido.fecha.desc()).all()
 
    total_dia = sum(p.total or 0 for p in pedidos_lista)
 
    return render_template('pedidos/pedidos.html',form= pedido_form,pedidos= pedidos_lista,fecha= fecha_str,total_dia = total_dia)
 

@pedidos_bp.route('/pedido/<int:pedido_id>', methods=['GET'])
def detallePedido(pedido_id):
    pedido   = Pedido.query.get_or_404(pedido_id)
    detalles = DetallePedido.query.filter_by(id_pedido=pedido_id).all()
 
    return render_template('pedidos/detallePedido.html',pedido= pedido,detalles = detalles)

@pedidos_bp.route('/nuevoPedido', methods=['GET', 'POST'])
def nuevoPedido():
    cliente_form = forms.ClienteForm(request.form)
    detalle_form = forms.DetallePedidoForm(request.form)
    pizzas       = Pizza.query.all()

    detalle_form.id_pizza.choices = [(p.id, f'{p.tamanio} — ${p.precio:.0f}') for p in pizzas]

    if request.method == 'POST' and request.form.get('action') == 'agregar':
        tamanio      = request.form.get('tamanio')
        cantidad     = int(request.form.get('cantidad', 1))
        extras       = request.form.getlist('extra_ing')

        precios      = {'Chica': 40, 'Mediana': 80, 'Grande': 120}
        precio_base  = precios.get(tamanio, 40)
        precio_extra = len(extras) * 10
        precio_total = precio_base + precio_extra
        subtotal     = precio_total * cantidad

        pizza = Pizza(
            tamanio      = tamanio,
            ingredientes = ', '.join(extras) if extras else 'Sin ingredientes',
            precio       = precio_total
        )
        db.session.add(pizza)
        db.session.flush()

        detalle = DetallePedido(
            id_pedido = None,
            id_pizza  = pizza.id,
            cantidad  = cantidad,
            subtotal  = subtotal
        )
        db.session.add(detalle)
        db.session.commit()

        if 'detalle_ids' not in session:
            session['detalle_ids'] = []
        session['detalle_ids'].append(detalle.id)
        session.modified = True

        return redirect(url_for('pedidos.nuevoPedido'))

    if request.method == 'POST' and request.form.get('action') == 'quitar':
        detalle_id = int(request.form.get('detalle_id'))
        detalle    = DetallePedido.query.get(detalle_id)
        if detalle and detalle.id_pedido is None:
            db.session.delete(detalle)
            db.session.commit()
            ids = session.get('detalle_ids', [])
            ids.remove(detalle_id)
            session['detalle_ids'] = ids
            session.modified = True

        return redirect(url_for('pedidos.nuevoPedido'))

    if request.method == 'POST' and request.form.get('action') == 'terminar':
        ids_actuales = session.get('detalle_ids', [])

        if not ids_actuales:
            flash('¡No hay pizzas en el pedido!', 'error')
            return redirect(url_for('pedidos.nuevoPedido'))

        fecha_str = request.form.get('fecha', '')
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        except:
            fecha = datetime.now()

        cliente = Cliente(
            nombre    = cliente_form.nombre.data,
            direccion = cliente_form.direccion.data,
            telefono  = cliente_form.telefono.data
        )
        db.session.add(cliente)
        db.session.flush()

        detalles = DetallePedido.query.filter(DetallePedido.id.in_(ids_actuales)).all()
        total    = sum(d.subtotal for d in detalles)

        pedido = Pedido(id_cliente=cliente.id, fecha=fecha, total=total)
        db.session.add(pedido)
        db.session.flush()

        for detalle in detalles:
            detalle.id_pedido = pedido.id

        db.session.commit()
        session['detalle_ids'] = []
        session.modified = True
        flash(f'¡Pedido registrado! Total a pagar: ${total:.2f}', 'success')
        return redirect(url_for('pedidos.nuevoPedido'))

    ids_actuales  = session.get('detalle_ids', [])
    carrito       = DetallePedido.query.filter(DetallePedido.id.in_(ids_actuales)).all() if ids_actuales else []
    total_carrito = sum(d.subtotal for d in carrito)

    return render_template('pedidos/nuevoPedido.html',
                           cliente_form  = cliente_form,
                           detalle_form  = detalle_form,
                           pizzas        = pizzas,
                           carrito       = carrito,
                           total_carrito = total_carrito,
                           today         = date.today().isoformat())