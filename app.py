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
    """Returns JSON {'cupcakes': [{id, flavor, size, rating, image}, ...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get('/api/cupcakes/<int:cupcake_id>')
def get_cupcake_info(cupcake_id):
    """Returns JSON {'cupcake': [{id, flavor, size, rating, image}]}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()
    return jsonify(cupcake=serialized)


@app.post('/api/cupcakes')
def create_cupcake():
    """Create cupcake from form data & return it.

    Returns JSON {'cupcake': [{id, flavor, size, rating, image}]}"""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] or None

    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image=image
    )

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    # Return w/status code 201 --- return tuple (json, status)
    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake_info(cupcake_id):
    """Updates cupcake with new data

    Returns JSON for changed data {'cupcake': [{id, flavor, size, rating, image}]}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json["flavor"] or cupcake.flavor
    cupcake.size = request.json["size"] or cupcake.size
    cupcake.rating = request.json["rating"] or cupcake.rating
    cupcake.image = request.json["image"] or cupcake.image

    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 200)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Deletes cupcake
    
    Returns id of deleted cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify(deleted=cupcake_id), 200)
