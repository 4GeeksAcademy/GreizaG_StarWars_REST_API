from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

last_id_users = 0
last_id_characters = 0
last_id_starships = 0
last_id_planets = 0

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    
    def generateId():
        global last_id_users
        last_id_users += 1
        return last_id_users

    def __repr__(self):
        return f"User name: {self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    heigth = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(20))
    eye_color = db.Column(db.String(20))
    skin_color = db.Column(db.String(20))
    birth_year = db.Column(db.String(20))
    gender = db.Column(db.String(20))

    def generateId():
        global last_id_characters
        last_id_characters += 1
        return last_id_characters

    def __repr__(self):
        return f"Character name: {self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "heigth": self.heigth,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "birth_year": self.birth_year,
            "gender": self.gender
        }

class Starships(db.Model):
    __tablename__ = 'starships'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    model = db.Column(db.String(50))
    starship_class = db.Column(db.String(50))
    length = db.Column(db.Integer)
    crew = db.Column(db.String(20))
    passengers = db.Column(db.String(20))

    def generateId():
        global last_id_starships
        last_id_starships += 1
        return last_id_starships

    def __repr__(self):
        return f"Starship name: {self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "starship_class": self.starship_class,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    diameter = db.Column(db.Integer)
    gravity = db.Column(db.String(50))
    population = db.Column(db.String(20))
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    surface_water = db.Column(db.String(20))

    def generateId():
        global last_id_planets
        last_id_planets += 1
        return last_id_planets

    def __repr__(self):
        return f"Planet name: {self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }

class FavoriteCharacters(db.Model):
    __tablename__ = 'favorite_characters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_id_relationship = db.relationship(Users)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    character_id_relationship = db.relationship(Characters)

    def __repr__(self):
        return f"User: {self.user_id} -> likes character {self.character_id}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }
    
class FavoriteStarships(db.Model):
    __tablename__ = 'favorite_starships'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_id_relationship = db.relationship(Users)
    starship_id = db.Column(db.Integer, db.ForeignKey('starships.id'))
    starship_id_relationship = db.relationship(Starships)

    def __repr__(self):
        return f"User: {self.user_id} -> likes starship: {self.starship_id}"
    
    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "starship_id": self.starship_id
        }