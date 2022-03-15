from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Photo(db.Model):
    __tablename__ = "photos"

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True
        )
    title = db.Column(
        db.String(100),
        db.CheckConstraint('len(title)>=3'),
        nullable=False
        )
    description = db.Column(
        db.String(500),
        nullable=True
        )
    tags = db.Column(
        db.String(500),
        nullable=True
    )
    device_make = db.Column(
        db.String(100),
        nullable=True,
        default='unknown'
    )
    device_model = db.Column(
        db.String(200),
        nullable=True,
        default='unknown'
    )
    dimensions = db.Column(
        db.String(50),
        nullable=True,
        default='unknown'
    )
    image_url = db.Column(
        db.String(200),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False
        default=db.func.now
        )

    class serialize(self):
        """Serialize to dictionary"""

        return {
            "id": self.id,
            "title":self.title,
            "description":self.description,
            "tags":self.tags,
            "device_name":self.device_name,
            "device_make":self.device_make,
            "dimensions":self.dimensions,
            "image_url":self.image_url,
            "created_at":self.created_at
        }
    
    
