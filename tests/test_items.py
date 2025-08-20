def test_create_item(client, db_session):
    user_data = {'username':'itemuser','email':'itemuser@example.com','password':'testpass'}
    client.post('/auth/register', json = user_data)
    login_response = client.post('/auth/login', data={'username': user_data['email'], 'password': user_data['password']})
    token = login_response.json()['access_token']


    item_data = {'title':'Test Item','description':'Test description'}
    response = client.post('/items/', json=item_data, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'Test Item'
    assert data['description'] == 'Test description'
    assert 'id' in data