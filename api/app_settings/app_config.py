from api.app import app
from flask import jsonify, render_template
from marshmallow import ValidationError
from api.db import db
from sqlalchemy_utils import database_exists, create_database


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
if not database_exists(db_uri):
    create_database(db_uri)

@app.before_first_request
def create_tables():
    db.create_all()

# setting app level error handlers
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')
