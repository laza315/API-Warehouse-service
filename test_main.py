from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_blog():
    response = client.get("/blog/all")
    assert response.status_code == 200


def test_auth_error():
    response = client.post('/token',
                           data={'username': "", 
                                 "password": ""})
    try:
        access_token = response.json().get("access_token")
    except AttributeError:
        # counters is not a dictionary, ignore and move on
        pass
    assert access_token == None
    try: 
        message = response.json().get("detail")[0].get("msg")
        assert message == "field required"
    except AttributeError:
        pass

def test_auth_success():
    response = client.post('/token',
                           data={'username': "doggo", 
                                 "password": "doggo"})
    try:
        access_token = response.json().get("access_token")
        assert access_token
    except AttributeError:
        pass

def test_post_Article():
    auth = client.post('/token',
                        data={'username': "doggo", 
                              "password": "doggo"})
    

    try:
        access_token = auth.json().get("access_token")
        assert access_token


        response = client.post(
            "/article/",
            json={
            "title": "string",
            "content": "string",
            "published": True,
            "creator_id": 2
            },
            headers={
                "Authorization": "bearer" + access_token
            }
            
        )
        print(response.headers.values)
        # assert response.headers == access_token
    except AttributeError:
        pass
