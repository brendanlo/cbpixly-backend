from flask import Flask
import os

from models import db, connect_db


app = Flask(__name__)
app.config["SECRET_KEY"]= os.environ["SECRET_KEY"]

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///pixly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()




@app.get("/photos")
def get_all_photos():
    """Get all photos"""

    return jsonify([photos])


@app.post("/photos")
def create_photo():
    """Add new photo"""

    return 