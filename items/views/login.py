from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required

from ..forms import LoginForm


def login(request):

    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login_user(request, user)
            return redirect('item_list')

    return render(request, 'items/login.html', {'form': form})


@login_required(login_url='/login/')
def logout(request):
    logout_user(request)
    return redirect('login')
