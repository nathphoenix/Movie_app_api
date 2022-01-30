import os
from api.ma import ma 
from api.db import db
#from api.oa import oauth
from api.app import app
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)





#These are commentend out for heroku deployment

db.init_app(app)
# this runs in the background and it tell that marshmallow object what flask app it should be talking to
ma.init_app(app)
#oauth.init_app(app)

if __name__ == "__main__":
    app.run()


