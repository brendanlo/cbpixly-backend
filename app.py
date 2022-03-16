from flask import Flask, jsonify
import os
import boto3
from models import db, connect_db


app = Flask(__name__)
app.config["SECRET_KEY"]= os.environ["SECRET_KEY"]

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///pixly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bucket_name=os.environ["BUCKET_NAME"]
s3 = boto3.client('s3')

connect_db(app)
db.create_all()


@app.get("/photos")
def get_all_photos():
    """Get all photos"""

    photos = Photo.query.all()
    serialized = [photo.serialize() for photo in photos]
    return jsonify(photos=serialized)


@app.post("/photos")
def create_photo():
    """Add new photo"""
    
    
    data = open('test.jpg', 'rb')

    # upload to s3 bucket
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html



    return 