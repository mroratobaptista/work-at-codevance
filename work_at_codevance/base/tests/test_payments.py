from datetime import datetime

from django.test import Client

from work_at_codevance.base.utils import calculate_discount


def test_status_code(client: Client):
    resp = client.get('/pagamentos/')
    assert resp.status_code == 200


def test_calculate_discount():
    date_due = '2019-10-01'
    date_anticipation = '2019-09-15'
    value_original = 1000

    date_due = datetime.strptime(date_due, '%Y-%m-%d').date()
    date_anticipation = datetime.strptime(date_anticipation, '%Y-%m-%d').date()

    value_with_discount = calculate_discount(date_due=date_due, date_anticipation=date_anticipation,
                                             value_original=value_original)

    assert value_with_discount == 984
