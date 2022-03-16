from flask import Flask, jsonify
from flask_cors import CORS
import os
import boto3
from models import db, connect_db, Photo


app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"]= os.environ["SECRET_KEY"]

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///pixly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

BUCKET_NAME=os.environ["BUCKET_NAME"]
s3 = boto3.client('s3')

connect_db(app)
db.create_all()


@app.get("/api/photos")
def get_all_photos():
    """Get all photos"""

    photos = Photo.query.all()
    serialized = [photo.serialize() for photo in photos]
    return jsonify(photos=serialized)


@app.post("/api/photos")
def create_photo():
    """Add new photo
       
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
    """

    # set input values for file upload
    file = request.files['file']
    file_name = secure_filename(file.filename)
    if object_name is None:
        object_name = os.path.basename(file_name)
    #TODO add metadata here

    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, BUCKET_NAME, object_name)
    except ClientError as e:
        logging.error(e)
        return False

    #TODO add file location to DB
    return True
