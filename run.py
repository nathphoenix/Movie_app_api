from app import app
from api.db import db
from api.ma import ma
from api.oa import oauth
#this run.py is created for heroku platform
db.init_app(app)
    # this runs in the background and it tell that marshmallow object what flask app it should be talking to
ma.init_app(app)
oauth.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()