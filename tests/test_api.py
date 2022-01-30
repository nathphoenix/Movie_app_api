import os
from flask_jwt_extended import create_access_token


# def test_v1_sample_post_endpoint(client):
#     payload = {
#         'username': 'test',
#         'key': 4,
#         'time': '15-12-2020'
#     }

#     response = client.post('/v1/sample-func', json=payload)
#     response_body = response.get_json()

#     assert response.status_code == 201
#     assert response_body.get('message') == "The return message goes here."
    
    
#FUNCTION NAME MUST ALWAYS BEGIN WITH test_
def test_books_endpoint(client):
  access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDM1NTM0MzEsIm5iZiI6MTY0MzU1MzQzMSwianRpIjoiMzZmOTRjMTktZjY1ZS00NDQyLThlYWUtODZkZWYwZjc3YTQ1IiwiZXhwIjoxNjQzNTU3MDMxLCJpZGVudGl0eSI6MSwiZnJlc2giOnRydWUsInR5cGUiOiJhY2Nlc3MifQ.Rs0M57qMIP7qAAPQ07yMWWVM_SBbPjcz4rEx2WEuovM'
  headers = {
      'Authorization': 'Bearer {}'.format(access_token)
  }
  response = client.get('/book', headers=headers)
  response_body = response.get_data()
  assert response.status_code == 200
  assert response.status_code == 200




def test_charater_name_endpoint(client):
  payload = {
        "name": "Maedhros"
    }
  access_token = os.environ.get('ONE_API_ACCESS')
  headers = {'Authorization': 'Bearer {}'.format(access_token)}
  #response = client.get('https://movieoneapi.herokuapp.com/name', json=payload)
  response = client.get('/name', json=payload, headers=headers)
  response_body = response.get_data()
  assert response.status_code == 200
  assert response.status_code == 200
