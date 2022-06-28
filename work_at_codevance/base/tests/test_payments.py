from datetime import datetime

import pytest
from django.contrib.auth.models import Group
from model_mommy import mommy

from work_at_codevance.base.models import Payment, User, Provider
from work_at_codevance.base.tests.django_assertions import assert_contains, assert_not_contains
from work_at_codevance.base.utils import calculate_discount


@pytest.mark.parametrize(
    'date_due,'
    'date_anticipation,'
    'value_original,'
    'value_expected',
    [
        ('2019-10-01', '2019-09-15', 1000, 984),
        ('2022-05-31', '2022-05-01', 1550, 1503.5),
        ('2022-06-27', '2022-06-26', 10, 9.99),
    ]
)
def test_calculate_discount(date_due, date_anticipation, value_original, value_expected):
    date_due = datetime.strptime(date_due, '%Y-%m-%d').date()
    date_anticipation = datetime.strptime(date_anticipation, '%Y-%m-%d').date()

    value_with_discount = calculate_discount(date_due=date_due, date_anticipation=date_anticipation,
                                             value_original=value_original)

    assert value_with_discount == value_expected


@pytest.fixture
def provider_group(db):
    provider_group = Group(id=1, name='Fornecedor')
    provider_group.save()
    return provider_group


@pytest.fixture
def operator_group(db):
    provider_group = Group(id=1, name='Operador')
    provider_group.save()
    return provider_group


@pytest.fixture
def user_1_with_provider_group(provider_group):
    user = User(id=1, email='f1@bar.com', password='123456')
    user.save()
    provider_group.user_set.add(user)
    provider = Provider(cnpj=1, user_id=1)
    provider.save()
    return user


@pytest.fixture
def user_2_with_provider_group(provider_group):
    user = User(id=2, email='f2@bar.com', password='123456')
    user.save()
    provider_group.user_set.add(user)
    provider = Provider(cnpj=2, user_id=2)
    provider.save()
    return user


@pytest.fixture
def users_with_provider_group(user_1_with_provider_group, user_2_with_provider_group):
    return user_1_with_provider_group, user_2_with_provider_group


@pytest.fixture
def create_payments_user_1(user_1_with_provider_group, client):
    mommy.make(Payment, provider_id=1, status='DISPO', _quantity=123)

    client.force_login(user_1_with_provider_group)
    resp = client.get('/pagamentos/')
    payments_available_user_1 = resp.context.get('payments_available')

    return payments_available_user_1


@pytest.fixture
def create_payments_user_2(user_2_with_provider_group, client):
    mommy.make(Payment, provider_id=2, status='DISPO', _quantity=50)

    client.force_login(user_2_with_provider_group)
    resp = client.get('/pagamentos/')
    payments_available_user_2 = resp.context.get('payments_available')

    return payments_available_user_2


@pytest.fixture
def create_payments(create_payments_user_1, create_payments_user_2):
    return create_payments_user_1, create_payments_user_2


def test_amount_payments_user_1(create_payments):
    payments_available_user_1, payments_available_user_2 = create_payments
    assert len(payments_available_user_1) == 123


def test_amount_payments_user_2(create_payments):
    payments_available_user_1, payments_available_user_2 = create_payments
    assert len(payments_available_user_2) == 50


@pytest.fixture
def user_operator(operator_group):
    user_operator = User(id=1, email='f1@bar.com', password='123456')
    user_operator.save()
    operator_group.user_set.add(user_operator)
    return user_operator


@pytest.fixture
def client_user_operator_logged(user_operator, client):
    client.force_login(user_operator)
    return client


def test_amount_payments_user_operator(create_payments, client_user_operator_logged):
    resp = client_user_operator_logged.get('/pagamentos/')
    payments_available = resp.context.get('payments_available')
    assert len(payments_available) == 123 + 50


def test_contains_button_approve_payment_user_operator(create_payments, client_user_operator_logged):
    mommy.make(Payment, provider_id=1, status='AGUAR')
    resp = client_user_operator_logged.get('/pagamentos/')
    assert_contains(resp, '<button class="btn btn-success">Liberar</button>')


def test_contains_button_deny_payment_user_operator(create_payments, client_user_operator_logged):
    mommy.make(Payment, provider_id=1, status='AGUAR')
    resp = client_user_operator_logged.get('/pagamentos/')
    assert_contains(resp, '<button class="btn btn-danger">Negar</button>')


@pytest.fixture
def client_user_1_provider_logged(user_1_with_provider_group, client):
    client.force_login(user_1_with_provider_group)
    return client


@pytest.fixture
def client_user_2_provider_logged(user_2_with_provider_group, client):
    client.force_login(user_2_with_provider_group)
    return client


def test_not_contains_button_allow_payment_user_provider(create_payments, client_user_1_provider_logged):
    mommy.make(Payment, provider_id=1, status='AGUAR')
    resp = client_user_1_provider_logged.get('/pagamentos/')
    assert_not_contains(resp, '<button class="btn btn-success">Liberar</button>')


def test_not_contains_button_deny_payment_user_provider(create_payments, client_user_2_provider_logged):
    mommy.make(Payment, provider_id=1, status='AGUAR')
    resp = client_user_2_provider_logged.get('/pagamentos/')
    assert_not_contains(resp, '<button class="btn btn-danger">Negar</button>')


def test_contains_button_anticipation_user_operator(create_payments, client_user_operator_logged):
    resp = client_user_operator_logged.get('/pagamentos/')
    assert_contains(resp, '<button type="button" class="btn btn-success">Adiantar</button>')


def test_contains_button_anticipation_user_provider(create_payments, client_user_1_provider_logged):
    resp = client_user_1_provider_logged.get('/pagamentos/')
    assert_contains(resp, '<button type="button" class="btn btn-success">Adiantar</button>')


def test_if_payment_no_belongs_to_provider_user_logged(create_payments, client_user_1_provider_logged):
    mommy.make(Payment, id=8000, provider_id=2, status='DISPO')
    resp = client_user_1_provider_logged.get('/pagamentos/8000/')
    assert resp.status_code == 404


def test_if_payment_no_belongs_to_operator_user_logged(create_payments, client_user_operator_logged):
    mommy.make(Payment, id=8000, provider_id=2, status='DISPO')
    resp = client_user_operator_logged.get('/pagamentos/8000/')
    assert resp.status_code == 200
