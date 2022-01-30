

def test_square(client):
    rv = client.get("/square?number=8")
    assert b"64" == rv.data
    
    