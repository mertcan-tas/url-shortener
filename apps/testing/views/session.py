from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.http import HttpResponse
from testing.views import NoAuthTokenView

def AutoLoginAdmin(request):
    user = get_user_model().objects.filter(is_superuser=True).first()
    if user:
        login(request, user)
        return redirect('/admin/')
    return HttpResponse("Admin kullanıcı bulunamadı.")