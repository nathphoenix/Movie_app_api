from importlib.abc import Loader
import os
from urllib import response
from flask import Flask, jsonify, Blueprint, request, abort
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required, fresh_jwt_required
from jinja2 import TemplateNotFound
from marshmallow import ValidationError
#flask upload can be use not only for images but some other things also
from flask_login import logout_user, LoginManager
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database
from flask_sieve import Sieve
#from .db import db
#This ensures the dotenv is loaded first before all our imported files 
 #we have to manually load the .env file now as we have our default_config file
#which the .env file depends upon

from datetime import timedelta

def create_app():
    load_dotenv(".env", verbose=True)
    from .blacklist import BLACKLIST
    from .resources.user import UserRegister, UserLogin, User, SetPassword, TokenRefresh, UserLogout
    from .resources.character import (Character, Book, CharacterName, CharacterId, Quotes, CharacterQuotes, FavouriteCharacter,
    FavouriteCharacterId, FavouriteQuotes, FavouriteItems)
    from .resources.confirmation import Confirmation, ConfirmationByUser
    


    app = Flask(__name__, instance_relative_config=True, static_url_path='', static_folder='static/')
    Sieve(app)

    app.url_map.strict_slashes = False
    #app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    #app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    #app.config["AWS_DEFAULT_REGION"] = os.environ['AWS_DEFAULT_REGION']


    #app.config.from_object("default_config")  # load default configs from default_config.py
    app.config.from_object("config.default_config")
    app.config.from_pyfile("config.default_config.py", silent=True)
    
    app.config.from_envvar(
        "APPLICATION_SETTINGS" #which is in the .env file
    )  # override with config.py (APPLICATION_SETTINGS points to config.py)


    jwt = JWTManager(app)
    #CORS(app)
    CORS(app, resources={r'/v1/*'})
    api = Api(app)



    # This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        return decrypted_token["jti"] in BLACKLIST


    '''
    ALL THE AVAILABLE ROUTES OR VIEWS
    '''
    api.add_resource(UserRegister, "/register", endpoint="register")

    api.add_resource(User, "/user/<int:user_id>")
    api.add_resource(UserLogin, "/login")
    api.add_resource(TokenRefresh, "/refresh")
    api.add_resource(Character, '/character')
    api.add_resource(CharacterName, '/name')
    api.add_resource(CharacterId, '/id')
    api.add_resource(Quotes, '/quotes')
    api.add_resource(CharacterQuotes, '/character_quotes')
    api.add_resource(FavouriteCharacter, '/char_name')
    api.add_resource(FavouriteCharacterId, '/char_id')
    api.add_resource(FavouriteQuotes, '/favourite_quotes')
    api.add_resource(FavouriteItems, '/all_favourites')
    
   
    api.add_resource(Book, '/book')
    api.add_resource(UserLogout, "/logout")

    api.add_resource(Confirmation, "/user_confirm/<string:confirmation_id>")  #this is for the html page
    api.add_resource(ConfirmationByUser, "/re_confirmation/user")
    

    @app.route("/square")
    def square():
        number = int(request.args.get("number", 0))
        return str(number ** 2)
    
    @app.route('/500')
    def error500():
        abort(500)


    @app.route('/')
    def home():
        welcome = 'WELCOME TO MOVIE WORLD'
        return welcome, 200

    @app.route('/v1')
    def v1_home():
        return jsonify({
            "message": "Welcome to DS Movie v1 API!"
        })


    
    api.add_resource(SetPassword, "/user/password") 
   
    return app

app = create_app()







from api.app_settings.app_config import *

