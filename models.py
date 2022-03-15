from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Photo(db.Model):
    __tablename__ = "photos"