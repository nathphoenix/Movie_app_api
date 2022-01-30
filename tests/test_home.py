def test_home_endpoint(client):
    response = client.get('/')
    #response_body = response.get_json()
    assert response.get_data() == b"WELCOME TO MOVIE WORLD"
    assert response.status_code == 200
    assert response.status_code == 200


def test_v1_home_endpoint(client):
    response = client.get('/v1')
    response_body = response.get_json()
    print(response_body)

    assert response.status_code == 200
    assert response_body.get('message') == "Welcome to DS Movie v1 API!"
