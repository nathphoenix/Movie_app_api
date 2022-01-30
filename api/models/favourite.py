from ..db import db
from ..libs.mailgun import Mailgun, GoogleMail
from ..models.confirmation import ConfirmationModel
from typing import Dict, List, Union



class FavouriteModel(db.Model):
    __tablename__ = "favourite"

    id = db.Column(db.Integer, primary_key=True)
    _id = db.Column(db.String(200), nullable=False, unique=False)
    height = db.Column(db.String(200), nullable=True, unique=False)
    race = db.Column(db.String(500), nullable=True, unique=False)
    gender = db.Column(db.String(500), nullable=True, unique=False)
    birth = db.Column(db.String(500), nullable=True, unique=False)
    spouse = db.Column(db.String(500), nullable=True, unique=False)
    death = db.Column(db.String(500), nullable=True, unique=False)
    realm = db.Column(db.String(500), nullable=True, unique=False)
    hair = db.Column(db.String(500), nullable=True, unique=False)
    name = db.Column(db.String(500), nullable=True, unique=True)
    wikiUrl = db.Column(db.String(500), nullable=True, unique=False)
    dialog = db.Column(db.String(2500), nullable=True, unique=True)


    """
    METHODS
    """

    @classmethod
    def find_by_name(cls, name: str) -> "FavouriteModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "FavouriteModel": 
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_mongo_id(cls, _id: str) -> "FavouriteModel":
        return cls.query.filter_by(_id=_id).first()
    
    @classmethod
    def find_all(cls) -> List["FavouriteModel"]:
        return cls.query.all()
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
