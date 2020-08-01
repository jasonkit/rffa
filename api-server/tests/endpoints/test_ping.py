def test_ping(context):
    response = context.client.get('/ping')
    assert response.status_code == 200
    assert response.json() == {'result': 'pong'}
