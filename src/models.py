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

