from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from work_at_codevance.base.models import Payment
from work_at_codevance.base.utils import is_member


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
