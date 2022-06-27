from datetime import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from work_at_codevance.base.models import Payment
from work_at_codevance.base.utils import is_member, calculate_discount


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

            value_with_discount = float(value_with_discount_str.replace(',', '.'))
            payment.value_with_discount = float(value_with_discount_str.replace(',', '.'))

            discount = payment.value_original - value_with_discount
            payment.discount = discount

            payment.save()

            return redirect(payments)

        elif date_anticipation_str:
            date_anticipation = datetime.strptime(date_anticipation_str, '%Y-%m-%d').date()
            value_with_discount = calculate_discount(payment.date_due, date_anticipation, payment.value_original)
            context['value_with_discount'] = value_with_discount
            context['date_anticipation'] = date_anticipation_str

    return render(request, 'detail_payment.html', context=context)
