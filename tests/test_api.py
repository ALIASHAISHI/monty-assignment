def test_publish_empty(client):
    response = client.post("/publish")
    assert response.status_code == 400
    

def test_publish(client):
    response = client.post("/publish", json={
        "message": "Flask"
    })
    assert response.status_code == 200

    
def test_consume_published(client):
    response = client.get("/consume")
    assert response.status_code == 200
    assert response.data == b'{"message":"Flask"}\n'

    
def test_consume(client):
    response = client.get("/consume")
    assert response.status_code == 200
    assert response.data == b'{"message":null}\n'