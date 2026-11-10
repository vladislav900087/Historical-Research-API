
def test_health_endpoint(client):

    response = client.get('/health')

    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'

def test_database_persistence_isolation(db_session, client):
    pass