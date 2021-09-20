"""Flask app for Cupcakes"""
from flask import Flask, request, flash, jsonify

from models import db, connect_db, Cupcake

DEFAULT_IMG_URL = "https://tinyurl.com/demo-cupcake"

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

@app.get('/api/cupcakes')
def list_cupcakes():
    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return  jsonify(cupcakes=serialized)

@app.get('/api/cupcakes/<int:cupcake_id>')
def get_cupcake_info(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()
    return jsonify(cupcake=serialized)

# @app.post('/api/cupcakes')
# def create_cupcake():
#     cupcake 