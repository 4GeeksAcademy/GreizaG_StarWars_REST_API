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
from models import db, Users, Characters, Starships, Planets, FavoriteCharacters, FavoriteStarships, FavoritePlanets
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
        return jsonify({"msg": "You should send info in body"}), 400
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

# Traer todos los planetas
@app.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets = Planets.query.all()
    planets_serialized = []
    for planet in all_planets:
        planets_serialized.append(planet.serialize())
    print(planets_serialized)
    return jsonify({"data": planets_serialized}), 200

# Traer sólo un planeta
@app.route('/planets/<int:id>', methods=['GET'])
def get_single_planet(id):
    single_planet = Planets.query.get(id)
    if single_planet is None:
        return jsonify({"msg": "Planet with id: {}, not found".format(id)}), 400
    return jsonify({"data": single_planet.serialize()}), 200

# Crear nuevo planeta
@app.route('/planet', methods=['POST'])
def new_planet():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "You should send info in body"}), 400
    if "name" not in body:
        return jsonify({"msg": "Name is needed"}), 400
    if "diameter" not in body:
        return jsonify({"msg": "Diameter is needed"}), 400
    if "gravity" not in body:
        return jsonify({"msg": "Gravity is needed"}), 400
    if "population" not in body:
        return jsonify({"msg": "Population is needed"}), 400
    if "climate" not in body:
        return jsonify({"msg": "Climate is needed"}), 400
    if "terrain" not in body:
        return jsonify({"msg": "Terrain is needed"}), 400
    if "surface_water" not in body:
        return jsonify({"msg": "Surface water is needed"}), 400
    
    new_planet = Planets()
    new_planet.id = body.get("id", Planets.generateId())
    new_planet.name = body["name"]
    new_planet.diameter = body["diameter"]
    new_planet.gravity = body["gravity"]
    new_planet.population = body["population"]
    new_planet.climate = body["climate"]
    new_planet.terrain = body["terrain"]
    new_planet.surface_water = body["surface_water"]
    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"data": new_planet.serialize()}), 201

# Traer todos los favoritos de un usuario
@app.route('/users/<int:id>/favorites')
def user_favorite_list(id):
    favorite_characters = db.session.query(FavoriteCharacters, Characters).join(Characters).filter(FavoriteCharacters.user_id == id).all()
    favorite_characters_serialized = []
    for favorite_character, character in favorite_characters:
        favorite_characters_serialized.append(character.serialize()["name"])
    
    favorite_starships = db.session.query(FavoriteStarships, Starships).join(Starships).filter(FavoriteStarships.user_id == id).all()
    favorite_starships_serialized = []
    for favorite_starship, starship in favorite_starships:
        favorite_starships_serialized.append(starship.serialize()["name"])

    favorite_planets = db.session.query(FavoritePlanets, Planets).join(Planets).filter(FavoritePlanets.user_id == id).all()
    favorite_planets_serialized = []
    for favorite_planet, planet in favorite_planets:
        favorite_planets_serialized.append(planet.serialize()["name"])
    
    return jsonify({"favorites": {"characters": favorite_characters_serialized, "starships": favorite_starships_serialized, "planets": favorite_planets_serialized}}), 200

# Editar usuario
@app.route('/users/<int:id>', methods=['PUT'])
def edit_user(id):
    body = request.get_json(silent=True)
    user_to_edit = Users.query.get(id)
    if user_to_edit is None:
        return jsonify({"msg": "User not found"}), 404
    if "name" in body:
        user_to_edit.name = body["name"]
    if "last_name" in body:
        user_to_edit.last_name = body["last_name"]
    db.session.commit()
    return jsonify({"user edited": user_to_edit.serialize()})

# Editar personaje
@app.route('/characters/<int:id>', methods=['PUT'])
def edit_character(id):
    body = request.get_json(silent=True)
    character_to_edit = Characters.query.get(id)
    if character_to_edit is None:
        return jsonify({"msg": "Character not found"}), 404
    if "name" in body:
        character_to_edit.name = body["name"]
    if "heigth" in body:
        character_to_edit.heigth = body["heigth"]
    if "mass" in body:
        character_to_edit.mass = body["mass"]
    if "hair_color" in body:
        character_to_edit.hair_color = body["hair_color"]
    if "eye_color" in body:
        character_to_edit.eye_color = body["eye_color"]
    if "skin_color" in body:
        character_to_edit.skin_color = body["skin_color"]
    if "birth_year" in body:
        character_to_edit.birth_year = body["birth_year"]
    if "gender" in body:
        character_to_edit.gender = body["gender"]

    db.session.commit()
    return jsonify({"character edited": character_to_edit.serialize()})

# Editar nave
@app.route('/starships/<int:id>', methods=['PUT'])
def edit_starship(id):
    body = request.get_json(silent=True)
    starship_to_edit = Starships.query.get(id)
    if starship_to_edit is None:
        return jsonify({"msg": "Starship not found"}), 404
    if "name" in body:
        starship_to_edit.name = body["name"]
    if "model" in body:
        starship_to_edit.model = body["model"]
    if "starship_class" in body:
        starship_to_edit.starship_class = body["starship_class"]
    if "length" in body:
        starship_to_edit.length = body["length"]
    if "crew" in body:
        starship_to_edit.crew = body["crew"]
    if "passengers" in body:
        starship_to_edit.passengers = body["passengers"]

    db.session.commit()
    return jsonify({"starship edited": starship_to_edit.serialize()})

# Editar planeta
@app.route('/planets/<int:id>', methods=['PUT'])
def edit_planet(id):
    body = request.get_json(silent=True)
    planet_to_edit = Planets.query.get(id)
    if planet_to_edit is None:
        return jsonify({"msg": "Planet not found"}), 404
    if "name" in body:
        planet_to_edit.name = body["name"]
    if "diameter" in body:
        planet_to_edit.diameter = body["diameter"]
    if "gravity" in body:
        planet_to_edit.gravity = body["gravity"]
    if "population" in body:
        planet_to_edit.population = body["population"]
    if "climate" in body:
        planet_to_edit.climate = body["climate"]
    if "terrain" in body:
        planet_to_edit.terrain = body["terrain"]
    if "surface_water" in body:
        planet_to_edit.surface_water = body["surface_water"]

    db.session.commit()
    return jsonify({"planet edited": planet_to_edit.serialize()})