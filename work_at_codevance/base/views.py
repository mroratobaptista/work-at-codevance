from django.shortcuts import render, redirect


def home(request):
    return render(request, 'home.html')


def login(request):
    return render(request, 'login.html', context={'login': True})


def logout(request):
    return redirect(home)


def payments(request):
    return render(request, 'payments.html')
