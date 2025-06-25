import uuid

def test_register_and_login(client):
    username = f"user_{uuid.uuid4().hex[:6]}"
    password = "123"

    # register
    res = client.post('/register', data={'username': username, 'password': password}, follow_redirects=False)
    assert res.status_code == 302
    assert res.headers["Location"].endswith("/login")

    # login
    res = client.post('/login', data={'username': username, 'password': password}, follow_redirects=True)
    assert b'Manager Passwords' in res.data
