from typing import Dict, Union
from requests import Response, post
from flask import request, url_for
from ..db import db
from ..libs.mailgun import Mailgun, GoogleMail
from ..models.confirmation import ConfirmationModel


UserJSON = Dict[str, Union[int, str]]


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(200), nullable=False, unique=False)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    #address = db.Column(db.String(500), nullable=False, unique=False)
    # activated = db.Column(db.Boolean, default=False)  # we are setting it to false till after we activated it
    confirmation = db.relationship(
        "ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan" #the cascade works for postgres, whenever you delete a user, will go over to the confirmations and delete all the confirmations that are related to the user
    )
    # we are no longer using activated as we have created everything in our userconfirmation maodel
    # we include nullable=False because we set the field that was deleted to be required in the schemas.py for
    # deserialization

    # Since this functions indicated that we are expecting username and password to be passed ,
    # which is the same benefit that the nullable=False ids doing  then we can comment this function out
    # def __init__(self, username: str, password: str):
    #     self.username = username
    #     self.password = password

    # We are no longer using json method which has been replace by the deserialization
    # def json(self) -> UserJSON:
    #     return {"id": self.id, "username": self.username}

    @property
    def most_recent_confirmation(self) -> "ConfirmationModel": #if a user has multiple confirmation, this will pick the most recent confirmation
        # it goes to the above confirmation variable and then ordered by expiration time (in descending order)
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()
 

    @classmethod
    def find_by_name(cls, name: str) -> "UserModel":
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def send_confirmation_email(self) -> Response:
        # string[:-1] means copying from start (inclusive) to the last index (exclusive), a more detailed link below:
        # from `http://127.0.0.1:5000/` to `http://127.0.0.1:5000`, since the url_for() would also contain a `/`
        # https://stackoverflow.com/questions/509211/understanding-pythons-slice-notation
        # url_root = `http://127.0.0.1:5000/`
        # -1 is for string slicing which get all the characters from the zero to the one before the last
        # the userconfirm is calling UserConfirm method that was use to create endpoint for confirmation page on app.py
        # "userconfirm", user_id=self.id is equivalent to  /user_confirm/1 as we have it on the endpoint in postman
        # in summary,


        link = request.url_root[:-1] + url_for("confirmation", confirmation_id=self.most_recent_confirmation.id)  #change this from the user_id to confirmation_id in other to secure the id of the user #the link for user to click
        # if '/user_confirm' in link:
        #     final_link = link.replace('/user_confirm', '/v1/user_confirm')

        subject = "Registration Confirmation"
        text = f"Please click the link to confirm your registration: {link}"
        html = f"<html>Please click the link to confirm your registration: <a href={link}>link</a></html>"
        GoogleMail.send_mail(self.username, self.email, text)
    
    def resend_confirmation_email(self) -> Response:


        link = request.url_root[:-1] + url_for("confirmation", confirmation_id=id)  #change this from the user_id to confirmation_id in other to secure the id of the user #the link for user to click
        # if '/user_confirm' in link:
        #     final_link = link.replace('/user_confirm', '/v1/user_confirm')

        subject = "Email Confirmation"
        text = f"Please click the link to confirm your registration: {link}"
        html = f"<html>Please click the link to confirm your registration: <a href={link}>link</a></html>"
        return GoogleMail.send_mail(self.username, self.email, text)


    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
