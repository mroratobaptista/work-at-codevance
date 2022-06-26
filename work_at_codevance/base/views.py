from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


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
    return render(request, 'payments.html')
