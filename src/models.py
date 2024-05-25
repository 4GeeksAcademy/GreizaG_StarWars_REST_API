from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

last_id_users = 0
last_id_people = 0
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
