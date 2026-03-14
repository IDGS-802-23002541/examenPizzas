from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
from flask_migrate import Migrate
from pedidos.routes import pedidos_bp
from datetime import date

from models import db, Pedido

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(pedidos_bp)
db.init_app(app)
csrf=CSRFProtect()
migrate=Migrate(app, db)

@app.route('/')
def inicio():
	fecha_hoy = date.today()

	total_dia = db.session.query(
        db.func.sum(Pedido.total)
    ).filter(
        db.func.date(Pedido.fecha) == fecha_hoy
    ).scalar() or 0

	total_mes = db.session.query(
        db.func.sum(Pedido.total)
    ).filter(
        db.func.month(Pedido.fecha) == fecha_hoy.month,
        db.func.year(Pedido.fecha) == fecha_hoy.year
    ).scalar() or 0

	return render_template("index.html", total_dia=total_dia, total_mes=total_mes)

@app.errorhandler(404)
def page_not_fount(e):
	return render_template("404.html"), 404

if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():
		db.create_all()
	app.run(debug=True)
