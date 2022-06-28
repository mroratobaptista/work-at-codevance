import pytest
from django.test import Client
from model_mommy import mommy

from work_at_codevance.base.tests.django_assertions import assert_contains


def test_redirect_to_page_login_status_code(client: Client):
    resp = client.get('/')
    assert resp.status_code == 302


def test_redirect_to_page_login_url(client: Client):
    resp = client.get('/')
    assert '/login' in resp.url


@pytest.fixture
def user_logged(db, django_user_model):
    user_model = mommy.make(django_user_model)
    return user_model


@pytest.fixture
def client_with_user_logged(user_logged, client):
    client.force_login(user_logged)
    return client


def test_status_code_with_user_logged(client_with_user_logged):
    resp = client_with_user_logged.get('/')
    assert resp.status_code == 200


def test_button_payments(client_with_user_logged):
    resp = client_with_user_logged.get('/')
    assert_contains(resp, '<a href="/pagamentos" class="nav-link px-2 text-white">Pagamentos</a>')


def test_button_logout(client_with_user_logged):
    resp = client_with_user_logged.get('/')
    assert_contains(resp, '<a href="/logout">')
