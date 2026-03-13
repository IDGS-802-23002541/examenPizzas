from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
from flask_migrate import Migrate

app = Flask(__name__)

@app.route('/')
def inicio():
	return render_template("index.html")

@app.errorhandler(404)
def page_not_fount(e):
	return render_template("404.html"), 404

if __name__ == '__main__':
	app.run(debug=True)

