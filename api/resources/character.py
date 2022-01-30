from importlib.resources import Resource
from flask import request
import requests
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
)
from ..models.character import CharacterModel
from ..models.favourite import FavouriteModel
from ..schemas.favourite import FavouriteSchema, FavouriteItemSchema
from ..schemas.character import CharacterSchema
from ..libs.strings import gettext
import os

schema = CharacterSchema()
schema_favourite = FavouriteSchema()
favourite_items_schema = FavouriteItemSchema(many=True)


class Book(Resource):
  """
  This returns all book from the API which doesn't require authentication
  """
  @classmethod
  @jwt_required
  def get(cls):
    try:
      one_api_url = os.environ.get("ONE_API_URL")
      url = one_api_url + "/book"
      response = requests.get(url)
      return response.json(), 200
    except Exception as e:
      return f'Error: {e}', 400
    


class Character(Resource):

  """
  This method fetch all characters from the API
  """
  
  @classmethod
  @jwt_required
  def get(cls):
    try:
      access_token = os.environ.get('ONE_API_ACCESS')
      headers = {'Authorization': 'Bearer {}'.format(access_token)}
      one_api_url = os.environ.get("ONE_API_URL")
      url = one_api_url + "/character"
      response = requests.get(url, headers= headers)
      return response.json(), 200
    except Exception as e:
      return f'Error: {e}', 400



class Character_quotes(Resource):
    @classmethod
    @jwt_required
    def get(cls):
      payload = request.get_json() if request.get_json() else dict(request.form)
      try:
        access_token = os.environ.get('ONE_API_ACCESS')
        headers = {'Authorization': 'Bearer {}'.format(access_token)}
        one_api_url = os.environ.get("ONE_API_URL")
        url = one_api_url + "/character"
        response = requests.get(url, payload,  headers= headers)
        return response.json(), 200
      except Exception as e:
        return f'Error: {e}', 400

class CharacterName(Resource):
    """
    This method returns the characters details by providing the characters name
    """
    @classmethod
    @jwt_required
    def get(cls):
        payload = request.get_json() if request.get_json() else dict(request.form)
        try:
          access_token = os.environ.get('ONE_API_ACCESS')
          headers = {'Authorization': 'Bearer {}'.format(access_token)}
          one_api_url = os.environ.get("ONE_API_URL")
          url = one_api_url + "/character"
          response = requests.get(url, payload,  headers= headers)
          texted = 'we get result'
          return response.json(), 200
        except Exception as e:
          return f'Error: {e}', 400
        
class CharacterId(Resource):
    """
    This method returns the characters details by providing the characters id
    """
    @classmethod
    @jwt_required
    def get(cls):
        payload = request.get_json() if request.get_json() else dict(request.form)
        try:
          access_token = os.environ.get('ONE_API_ACCESS')
          headers = {'Authorization': 'Bearer {}'.format(access_token)}
          one_api_url = os.environ.get("ONE_API_URL")
          url = one_api_url + "/character"
          response = requests.get(url, payload,  headers= headers)
          response = response.json()
          response_details = response['docs'][0]
          return response_details, 200
        except Exception as e:
          return f'Error: {e}', 400
        
        
class Quotes(Resource):
  
  """
    This returns all the quotes from the API
  """
  @classmethod
  @jwt_required
  def get(cls):
    try:
      access_token = os.environ.get('ONE_API_ACCESS')
      headers = {'Authorization': 'Bearer {}'.format(access_token)}
      one_api_url = os.environ.get("ONE_API_URL")
      url = one_api_url + "/quote"
      response = requests.get(url, headers= headers)
      return response.json(), 200
    except Exception as e:
      return f'Error: {e}', 400

class CharacterQuotes(Resource):
  
  
  """
  Methond to get all the quotes from a particular character by providing the character id 
  """
  @classmethod
  @jwt_required
  def get(cls):
    payload = request.get_json() if request.get_json() else dict(request.form)
    try:
      access_token = os.environ.get('ONE_API_ACCESS')
      headers = {'Authorization': 'Bearer {}'.format(access_token)}
      one_api_url = os.environ.get("ONE_API_URL")
      url = one_api_url + "/quote"
      response = requests.get(url, payload, headers= headers)
      #print(response)
      return response.json(), 200
    except Exception as e:
      return f'Error: {e}', 400
    
"""
This method made a get request and return the details of our favourite character
"""
class FavouriteCharacter(Resource):
  @classmethod
  @jwt_required
  def get(cls):
    payload = request.get_json() if request.get_json() else dict(request.form)
    try:
      access_token = os.environ.get('ONE_API_ACCESS')
      headers = {'Authorization': 'Bearer {}'.format(access_token)}
      one_api_url = os.environ.get("ONE_API_URL")
      url = one_api_url + "/character"
      response = requests.get(url, payload, headers= headers)
      response = response.json()
      character_details = response['docs'][0]
      return character_details, 200
    except Exception as e:
      return f'Error: {e}', 400
    
class FavouriteCharacterId(Resource):
  
  """
  This method allows a user favorite a specific character by 
  accepting character id and then save their details to the databse 
  """
  
  @classmethod
  @jwt_required
  def post(cls):
    payload = request.get_json() if request.get_json() else dict(request.form)
    try:
      access_token = os.environ.get('ONE_API_ACCESS')
      headers = {'Authorization': 'Bearer {}'.format(access_token)}
      one_api_url = os.environ.get("ONE_API_URL")
      url = one_api_url + "/character"
      response = requests.get(url, payload, headers= headers)
      response = response.json()
      character_details = response['docs'][0]
      print(character_details)
      character_name = character_details['name']
      check_name = CharacterModel.find_by_name(character_name)
      if check_name:
          return {"message": gettext("character_name_exists")}, 400
      serialize_details = schema.dump(character_details)
      print('serialize', serialize_details)
      serialize_and_save = schema.load(serialize_details)
      serialize_and_save.save_to_db()
      return serialize_details, 200
    except Exception as e:
      return f'Error: {e}', 400



"""
This class and function allows us to add our favourite quote with the 
character details and then save to the database by accepting the quote 
we liked most.
"""
class FavouriteQuotes(Resource):
  @classmethod
  @jwt_required
  def get(cls):
    payload = request.get_json() if request.get_json() else dict(request.form)
    try:
      access_token = os.environ.get('ONE_API_ACCESS')
      headers = {'Authorization': 'Bearer {}'.format(access_token)}
      one_api_url = os.environ.get("ONE_API_URL")
      url = one_api_url + "/quote"
      response = requests.get(url, payload, headers= headers)
      response = response.json()
      quote_details = response['docs'][0]
      actual_quote = quote_details['dialog']
      actual_quote = {'dialog': actual_quote}
      character_id = quote_details['character']
      print(character_id)
      #character_id = {'_id': character_id}
      character_details = CharacterModel.find_by_mongo_id(character_id)
      if not character_details:
        return {"message": gettext("character_quote_not_found")}, 400
      character_details = schema.dump(character_details)
      character_quote_with_details = {**character_details, ** actual_quote}
      print('character_quote_with_details', character_quote_with_details)
      name = character_quote_with_details['name']
      favourite_data = schema_favourite.load(character_quote_with_details)
      print('fav', favourite_data)
      if FavouriteModel.find_by_name(name):
        data_response = [
              {
                'Status': 'Favourite quote already exist'
              },
              {
                "data": f'name {name} already exist'
              }
            ]
        return data_response, 200
      favourite_data.save_to_db()
      data_response = [
        {
          'Status': 'Favourite quote saved successfully'
        },
        {
          "data": character_quote_with_details
        }
      ]
      return  data_response, 200
    except Exception as e:
      return f'Error: {e}', 400


class FavouriteItems(Resource):
    @classmethod
    @jwt_required
    def get(cls):
      records = favourite_items_schema.dump(FavouriteModel.find_all())
      if not records:
        return 'No records found', 400
      return records, 200