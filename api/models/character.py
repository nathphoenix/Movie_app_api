from typing import Dict, Union
from requests import Response, post
from flask import request, url_for
from ..db import db
from ..libs.mailgun import Mailgun, GoogleMail
from ..models.confirmation import ConfirmationModel


#MAILGUN SMTP
# MAILGUN_API_KEY = "b6e10edf62abbad31b3b258a0cfc674a-1df6ec32-12e4661b"
# MAILGUN_DOMAIN = "sandbox34d90c59e46f47fea6769287f3b64536.mailgun.org"
# #MAILGUN 
# FROM_EMAIL = 'postmaster@sandbox34d90c59e46f47fea6769287f3b64536.mailgun.org'
# FROM_TITLE = "Stores Rest API"

UserJSON = Dict[str, Union[int, str]]


class CharacterModel(db.Model):
    __tablename__ = "moviecharacter"

    id = db.Column(db.Integer, primary_key=True)
    _id = db.Column(db.String(200), nullable=False, unique=False)
    height = db.Column(db.String(200), nullable=False, unique=False)
    race = db.Column(db.String(500), nullable=False, unique=False)
    gender = db.Column(db.String(500), nullable=False, unique=False)
    birth = db.Column(db.String(500), nullable=False, unique=False)
    spouse = db.Column(db.String(500), nullable=False, unique=False)
    death = db.Column(db.String(500), nullable=False, unique=False)
    realm = db.Column(db.String(500), nullable=False, unique=False)
    hair = db.Column(db.String(500), nullable=False, unique=False)
    name = db.Column(db.String(500), nullable=False, unique=True)
    wikiUrl = db.Column(db.String(500), nullable=False, unique=False)


    """
    METHODS
    """

    @classmethod
    def find_by_name(cls, name: str) -> "CharacterModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "CharacterModel": 
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_mongo_id(cls, _id: str) -> "CharacterModel":
        return cls.query.filter_by(_id=_id).first()
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
