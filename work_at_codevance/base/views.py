import logging
from datetime import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from work_at_codevance.base.models import Payment
from work_at_codevance.base.tasks import send_mail
from work_at_codevance.base.utils import is_member, calculate_discount, check_if_payment_belongs_to_the_user


@login_required
def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect(home)

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(home)

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', context={'form': form, 'login': True})


@login_required
def logout_view(request):
    logout(request)
    return redirect(home)


@login_required
def payments(request):
    operator = is_member(request.user, 'Operador')
    provider = is_member(request.user, 'Fornecedor')

    payments_available = []
    payments_unavailable = []
    payments_waiting_confirmation = []
    payments_approved = []
    payments_denied = []

    if provider:

        user = request.user
        provider = user.provider_set.get()
        payments = provider.payment_set.all()

        for p in payments:
            if p.status == 'DISPO':
                payments_available.append(p)
            elif p.status == 'INDIS':
                payments_unavailable.append(p)
            elif p.status == 'AGUAR':
                payments_waiting_confirmation.append(p)
            elif p.status == 'APROV':
                payments_approved.append(p)
            elif p.status == 'NEGAD':
                payments_denied.append(p)

    elif operator:

        payments_available = Payment.objects.filter(status='DISPO')
        payments_unavailable = Payment.objects.filter(status='INDIS')
        payments_waiting_confirmation = Payment.objects.filter(status='AGUAR')
        payments_approved = Payment.objects.filter(status='APROV')
        payments_denied = Payment.objects.filter(status='NEGAD')

    context = {
        'payments_available': payments_available,
        'payments_unavailable': payments_unavailable,
        'payments_waiting_confirmation': payments_waiting_confirmation,
        'payments_approved': payments_approved,
        'payments_denied': payments_denied,
        'operador': operator,
        'fornecedor': provider
    }

    return render(request, 'payments.html', context=context)


@login_required
def detail_payment(request, payment_id):
    payment = Payment.objects.get(id=payment_id)

    context = {
        'payment': payment
    }

    if request.method == 'POST':
        date_anticipation_str = request.POST.get('date_anticipation')
        value_with_discount_str = request.POST.get('value_with_discount')

        if value_with_discount_str:
            payment.status = 'AGUAR'
            payment.date_anticipation = date_anticipation_str

            value_with_discount = round(float(value_with_discount_str.replace(',', '.')), 2)
            payment.value_with_discount = round(float(value_with_discount_str.replace(',', '.')), 2)

            discount = payment.value_original - value_with_discount
            payment.discount = round(discount, 2)

            payment.save()

            logger = logging.getLogger('db')
            msg = f'ID Pagamento: {payment.id} foi enviado para análise pelo usuário {request.user}.'
            logger.info(msg)
            send_mail.delay(f'Houve alteração no status do pagamento {payment_id} para {payment.status}', f'{request.user}', 'template_email.txt', {'msg': msg})

            return redirect(payments)

        elif date_anticipation_str:
            date_anticipation = datetime.strptime(date_anticipation_str, '%Y-%m-%d').date()
            value_with_discount = calculate_discount(payment.date_due, date_anticipation, payment.value_original)
            context['value_with_discount'] = round(value_with_discount, 2)
            context['date_anticipation'] = date_anticipation_str

    return render(request, 'detail_payment.html', context=context)


@login_required
def approve_deny_anticipation(request, payment_id, do):
    payment = Payment.objects.get(id=payment_id)
    payment.status = do
    payment.save()
    logger = logging.getLogger('db')
    msg = f'ID Pagamento: {payment.id} foi enviado {do} pelo usuário {request.user}.'
    logger.info(msg)
    send_mail.delay(f'Houve alteração no status do pagamento {payment_id} para {payment.status}', f'{request.user}',
                    'template_email.txt', {'msg': msg})
    return redirect(payments)


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def return_user_payments(request, status=None):
    user = request.user
    provider = user.provider_set.get()
    payments = provider.payment_set.all()

    if status:
        payments = payments.filter(status=status)

    return Response(
        {
            'count': len(payments),
            'payments': payments.values(
                'provider',
                'date_issuance',
                'date_due',
                'date_anticipation',
                'value_original',
                'discount',
                'value_with_discount',
                'status',
                'created_at',
                'updated_at',
            )}
    )


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def request_payment_anticipation(request, payment_id):
    status = 'AGUAR'

    if check_if_payment_belongs_to_the_user(request.user, payment_id):
        payment = Payment.objects.get(id=payment_id)
        payment.status = status
        payment.save()
        logger = logging.getLogger('db')
        msg = f'ID Pagamento: {payment.id} foi enviado para análise pelo usuário {request.user}.'
        send_mail.delay(f'Houve alteração no status do pagamento {payment_id} para {payment.status}', f'{request.user}',
                        'template_email.txt', {'msg': msg})
        logger.info(msg)
    else:
        return Response({'msg': 'Pagamento não encontrado'})

    return Response(
        {
            'payment': {
                'id': payment.id,
                'provider': payment.provider.corporate_name,
                'date_issuance': payment.date_issuance,
                'date_due': payment.date_due,
                'date_anticipation': payment.date_anticipation,
                'value_original': payment.value_original,
                'discount': payment.discount,
                'value_with_discount': payment.value_with_discount,
                'status': payment.status,
                'created_at': payment.created_at,
                'updated_at': payment.updated_at,
            }}
    )
