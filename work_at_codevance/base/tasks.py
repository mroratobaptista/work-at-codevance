from celery import shared_task
from django.core import mail
from django.template.loader import render_to_string

from work_at_codevance.settings import DEFAULT_FROM_EMAIL


@shared_task
def send_mail(subject, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, DEFAULT_FROM_EMAIL, [to])
