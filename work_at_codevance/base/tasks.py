import logging
from datetime import datetime

from celery import current_app
from celery import shared_task
from django.core import mail
from django.template.loader import render_to_string

from work_at_codevance.base.models import Payment
from work_at_codevance.settings import DEFAULT_FROM_EMAIL


@current_app.task
def check_payments_due_today():
    status = 'DISPO AGUAR'.split()
    payments = Payment.objects.filter(date_due=datetime.today(), status__in=status)
    for p in payments:
        p.status = 'INDIS'
        p.save()

        logger = logging.getLogger('db')
        msg = f'ID Pagamento: {p.id} ficou indisponível para adiantamento, pois a data de vencimento é hoje.'
        logger.info(msg)


@shared_task
def send_mail(subject, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, DEFAULT_FROM_EMAIL, [to])
