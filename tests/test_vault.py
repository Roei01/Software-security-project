def login(client):
    client.post('/register', data={'username':'bob','password':'secret'}, follow_redirects=True)
    client.post('/login', data={'username':'bob','password':'secret'}, follow_redirects=True)

def test_crud(client):
    login(client)
    # add
    res = client.post('/vault/add', data={'site':'example.com','login':'bob','password':'p@ss'}, follow_redirects=True)
    assert b'example.com' in res.data
    # edit
    res = client.get('/vault/')
    assert b'p@ss' in res.data
