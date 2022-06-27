"""work_at_codevance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from work_at_codevance.base.views import home, login_view, logout_view, payments, detail_payment, \
    approve_deny_anticipation, return_user_payments, request_payment_anticipation
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home),

    path('login/', login_view),
    path('logout/', logout_view),

    path('pagamentos/', payments),
    path('pagamentos/<int:payment_id>/', detail_payment),
    path('pagamentos/<int:payment_id>/<str:do>/', approve_deny_anticipation),

    # API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/pagamentos/', return_user_payments),
    path('api/pagamentos/<str:status>/', return_user_payments),
    path('api/solicitar-adiantamento/<int:payment_id>/', request_payment_anticipation),
]

