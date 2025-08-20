def test_login_user(client, db_session):
    user_data = {
        'username': 'loginuser',
        'email': 'loginuser@example.com',
        'password': 'testpass'
    }
    response = client.post('/auth/register', json=user_data)
    assert response.status_code == 200

    login_data = {
        'username': user_data['email'],  
        'password': user_data['password']
    }

    response = client.post('/auth/login', data=login_data)
    assert response.status_code == 200

    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'
