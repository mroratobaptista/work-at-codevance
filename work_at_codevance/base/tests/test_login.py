from django.test import Client


def test_status_code_login(client: Client):
    resp = client.get('/login/')
    assert resp.status_code == 200


def test_status_code_logout(client: Client):
    resp = client.get('/logout/')
    assert resp.status_code == 302


def test_context_login(client: Client):
    resp = client.get('/login/')
    assert {'login': True} in resp.context[0].dicts
