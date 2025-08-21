from typing import Dict
from fastapi.testclient import TestClient


def register_and_login(client: TestClient, *, email: str, username: str, password: str) -> Dict[str, str]:
    r = client.post('/auth/register', json={'username': username, 'email': email, 'password': password})
    assert r.status_code == 200, r.text

    r = client.post('/auth/login', data={'username': email, 'password': password})
    assert r.status_code == 200, r.text
    token = r.json()['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_create_item_success(client: TestClient, db_session):

    headers = register_and_login(
        client, email='item_creator@example.com', username='item_creator', password='testpass'
    )

    payload = {'title': 'Test Item', 'description': 'Test description'}
    r = client.post('/items/', json=payload, headers=headers)
    assert r.status_code == 200, r.text

    data = r.json()
    assert data['title'] == payload['title']
    assert data['description'] == payload['description']
    assert 'id' in data and 'owner_id' in data
    assert 'create_at' in data and 'updated_at' in data


def test_create_item_unauthorized(client: TestClient, db_session):

    r = client.post('/items/', json={'title': 'NoAuth'})
    assert r.status_code == 401, r.text


def test_get_items_only_own(client: TestClient, db_session):
  
    headers_a = register_and_login(
        client, email='userA@example.com', username='userA', password='passA'
    )
    headers_b = register_and_login(
        client, email='userB@example.com', username='userB', password='passB'
    )

    client.post('/items/', json={'title': 'A1', 'description': 'd1'}, headers=headers_a)
    client.post('/items/', json={'title': 'A2', 'description': 'd2'}, headers=headers_a)

    client.post('/items/', json={'title': 'B1'}, headers=headers_b)

    r_a = client.get('/items/', headers=headers_a)
    r_b = client.get('/items/', headers=headers_b)
    assert r_a.status_code == 200 and r_b.status_code == 200
    items_a = r_a.json()
    items_b = r_b.json()
    assert len(items_a) == 2
    assert len(items_b) == 1
    assert {i['title'] for i in items_a} == {'A1', 'A2'}
    assert {i['title'] for i in items_b} == {'B1'}


def test_get_item_owner_only(client: TestClient, db_session):
    
    headers_a = register_and_login(
        client, email='owner@example.com', username='owner', password='pass'
    )
    headers_b = register_and_login(
        client, email='intruder@example.com', username='intruder', password='pass'
    )

    r_create = client.post('/items/', json={'title': 'Secret'}, headers=headers_a)
    item_id = r_create.json()['id']

    r_ok = client.get(f'/items/{item_id}', headers=headers_a)
    assert r_ok.status_code == 200

    
    r_forbidden = client.get(f'/items/{item_id}', headers=headers_b)
    assert r_forbidden.status_code == 404


def test_update_item_success(client: TestClient, db_session):
    headers = register_and_login(
        client, email='upd@example.com', username='upduser', password='pass'
    )
    r_create = client.post('/items/', json={'title': 'Old', 'description': 'old'}, headers=headers)
    item_id = r_create.json()['id']

    r_upd = client.put(
        f'/items/{item_id}',
        json={'title': 'New', 'description': 'new'},
        headers=headers,
    )
    assert r_upd.status_code == 200, r_upd.text
    data = r_upd.json()
    assert data['title'] == 'New'
    assert data['description'] == 'new'
    assert 'updated_at' in data


def test_update_item_not_owner(client: TestClient, db_session):
    headers_a = register_and_login(
        client, email='own@example.com', username='own', password='pass'
    )
    headers_b = register_and_login(
        client, email='notown@example.com', username='notown', password='pass'
    )

    r_create = client.post('/items/', json={'title': 'Mine'}, headers=headers_a)
    item_id = r_create.json()['id']

    r_upd = client.put(
        f'/items/{item_id}',
        json={'title': 'Hack', 'description': 'try'},
        headers=headers_b,
    )
    assert r_upd.status_code == 404


def test_delete_item_success(client: TestClient, db_session):
    headers = register_and_login(
        client, email='del@example.com', username='deluser', password='pass'
    )
    r_create = client.post('/items/', json={'title': 'ToDelete'}, headers=headers)
    item_id = r_create.json()['id']

    r_del = client.delete(f'/items/{item_id}', headers=headers)
    assert r_del.status_code == 204

    r_get = client.get(f'/items/{item_id}', headers=headers)
    assert r_get.status_code == 404


def test_delete_item_not_owner(client: TestClient, db_session):
   
    headers_a = register_and_login(
        client, email='owner2@example.com', username='owner2', password='pass'
    )
    headers_b = register_and_login(
        client, email='stranger2@example.com', username='stranger2', password='pass'
    )

    r_create = client.post('/items/', json={'title': 'Private'}, headers=headers_a)
    item_id = r_create.json()['id']

    r_del = client.delete(f'/items/{item_id}', headers=headers_b)
    assert r_del.status_code == 404
