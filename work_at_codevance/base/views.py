from django.http import HttpResponse


def home(request):
    return HttpResponse('Work At Codevance')
