from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import boto3
from models import db, connect_db, Photo
from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError
import requests
from PIL import Image
from PIL.ExifTags import TAGS




app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"]= os.environ["SECRET_KEY"]

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///pixly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


BUCKET_NAME=os.environ["BUCKET_NAME"]
s3 = boto3.client(
    's3', 
    aws_access_key_id=os.environ['aws_access_key_id'],
    aws_secret_access_key=os.environ['aws_secret_access_key']
    )

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

    new_file = request.files['file']
    file_name = secure_filename(new_file.filename)
    object_name = os.path.basename(file_name)
    form_data = request.form

    #get exif data
    img = Image.open(new_file)
    exif_table={}
    for k, v in img.getexif().items():
        tag=TAGS.get(k)
        exif_table[tag]=v
    new_file.seek(0)
    print("exif data: ", exif_table)
    
   
    # breakpoint()
    device_make = "unknown"
    device_model = "unknown"
    dimensions = "unknown"

    try:
        device_make = exif_table['Make']
    except:
        device_make = "unknown"

    try:
        device_model = exif_table['Model']
    except:
        device_model = "unknown"

    try:
        dimensions = f'{img.width}x{img.height}'
    except:
        dimensions = "unknown"
    
    try:
        response = s3.upload_fileobj(new_file, BUCKET_NAME, object_name, ExtraArgs= {
            'ContentDisposition': 'inline',
            'ContentType': new_file.mimetype})
        # file_url = s3.generate_presigned_url(
        #         ClientMethod="get_object",
        #         Params={
        #             # "Body":new_file,
        #             "Bucket":BUCKET_NAME,
        #             "Key":object_name,
        #             # 'ContentDisposition': 'inline',
        #             # 'ContentType': new_file.mimetype
        #             })
        # # response = requests.put(file_url, data=new_file)

        new_photo = Photo(
            title=form_data['title'],
            description=form_data['description'],
            tags=form_data['tags'],
            device_make=device_make,
            device_model=device_model,
            dimensions=dimensions,
            image_url=object_name
        )
        print("new_photo: ", new_photo)

        db.session.add(new_photo)
        db.session.commit()

    
        # find the AWS URL > DB
    except ClientError as e:
        logging.error(e)
        return False
    print("request.files['file'] is: ", request.files['file'])
    
    return "Hello"


@app.get("/api/photos/imageurl")
def get_photo_url():
    print(request.args)
    file_url = s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    # "Body":new_file,
                    "Bucket":BUCKET_NAME,
                    "Key":request.args["key"]
                    # 'ContentDisposition': 'inline',
                    # 'ContentType': new_file.mimetype
                    })

    return file_url


@app.get("/api/photos/search")
def search_photos():
    [ make, model ] = request.args

    searched_photos = Photo.query.filter(Photo.device_make.ilike(f"%{make.lower()}%")).filter(Photo.device_model.ilike(f"%{model.lower()}%"))

    return searched_photos

    
    
