"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Characters, Starships
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Traer todos los usuarios
@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = Users.query.all()
    users_serialized = []
    for user in all_users:
        users_serialized.append(user.serialize())
    print(users_serialized)
    return jsonify({"data": users_serialized}), 200

# Traer sólo un usuario
@app.route('/users/<int:id>', methods=['GET'])
def get_single_user(id):
    single_user = Users.query.get(id)
    if single_user is None:
        return jsonify({"msg": "User with id: {}, not found".format(id)}), 400
    return jsonify({"data": single_user.serialize()}), 200

# Crear nuevo usuario
@app.route('/user', methods=['POST'])
def new_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "You should send info in body"}), 400
    if "name" not in body:
        return jsonify({"msg": "Name is needed"}), 400
    if "last_name" not in body:
        return jsonify({"msg": "Last name is needed"}), 400
    if "email" not in body:
        return jsonify({"msg": "email is needed"}), 400
    if "password" not in body:
        return jsonify({"msg": "Password is needed"}), 400
    
    new_user = Users()
    new_user.id = body.get("id", Users.generateId())
    new_user.name = body["name"]
    new_user.last_name = body["last_name"]
    new_user.email = body["email"]
    new_user.password = body["password"]
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"data": new_user.serialize()}), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

# Traer todos los personajes
@app.route('/characters', methods=['GET'])
def get_all_characters():
    all_characters = Characters.query.all()
    characters_serialized = []
    for character in all_characters:
        characters_serialized.append(character.serialize())
    print(characters_serialized)
    return jsonify({"data": characters_serialized}), 200

# Traer un sólo personaje
@app.route('/characters/<int:id>', methods=['GET'])
def get_single_character(id):
    single_character = Characters.query.get(id)
    if single_character is None:
        return jsonify({"msg": "Character with id: {}, not found".format(id)}), 400
    return jsonify({"data": single_character.serialize()}), 200

# Crear nuevo personaje
@app.route('/character', methods=['POST'])
def new_character():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "You should send info in body"}), 400
    if  "name" not in body:
        return jsonify({"msg": "Name is needed"}), 400
    if "heigth" not in body:
        return jsonify({"msg": "Heigth is needed"}), 400
    if "mass" not in body:
        return jsonify({"msg": "Mass is needed"}), 400
    if "hair_color" not in body:
        return jsonify({"msg": "Hair color is needed"}), 400
    if "eye_color" not in body:
        return jsonify({"msg": "Eye color is needed"}), 400
    if "skin_color" not in body:
        return jsonify({"msg": "Skin color is needed"}), 400
    if "birth_year" not in body:
        return jsonify({"msg": "Birth year is needed"}), 400
    if "gender" not in body:
        return jsonify({"msg": "Gender is needed"}), 400
    
    new_character = Characters()
    new_character.id = body.get("id", Characters.generateId())
    new_character.name = body["name"]
    new_character.heigth = body["heigth"]
    new_character.mass = body["mass"]
    new_character.hair_color = body["hair_color"]
    new_character.eye_color = body["eye_color"]
    new_character.skin_color = body["skin_color"]
    new_character.birth_year = body["birth_year"]
    new_character.gender = body ["gender"]
    db.session.add(new_character)
    db.session.commit()
    
    return jsonify({"data": new_character.serialize()}), 201

# Traer todas las naves
@app.route('/starships', methods=['GET'])
def get_all_starships():
    all_starships = Starships.query.all()
    starships_serialized = []
    for starship in all_starships:
        starships_serialized.append(starship.serialize())
        print(starships_serialized)
        return jsonify({"data": starships_serialized}), 200
    
# Traer sólo una nave
@app.route('/starships/<int:id>', methods=['GET'])
def get_single_starship(id):
    single_starship = Starships.query.get(id)
    if single_starship is None:
        return jsonify({"msg": "Starship with id: {}, not found".format(id)}), 400
    return jsonify({"data": single_starship.serialize()}), 200

# Crear una nueva nave
@app.route('/starship/', methods=['POST'])
def new_starship():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "You should sen info in body"}), 400
    if "name" not in body:
        return jsonify({"msg": "Name is needed"}), 400
    if "model" not in body:
        return jsonify({"msg": "Model is needed"}), 400
    if "starship_class" not in body:
        return jsonify({"msg": "Starship class is needed"}), 400
    if "length" not in body:
        return jsonify({"msg": "Length is needed"}), 400
    if "crew" not in body:
        return jsonify({"msg": "Crew is needed"}), 400
    if "passengers" not in body:
        return jsonify({"msg": "Passengers is needed"}), 400
    
    new_starship = Starships()
    new_starship.id = body.get("id", Starships.generateId())
    new_starship.name = body["name"]
    new_starship.model = body["model"]
    new_starship.starship_class = body["starship_class"]
    new_starship.length = body["length"]
    new_starship.crew = body["crew"]
    new_starship.passengers = body["passengers"]
    db.session.add(new_starship)
    db.session.commit()
    
    return jsonify({"data": new_starship.serialize()}), 201
