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

    # if request.method == 'POST':
    #
    #     errors = {}
    #
    #     username = request.POST.get("username", "").strip()
    #     if not username:
    #         errors["username"] = "Логін є обов'язковим"
    #     else:
    #         if not User.objects.filter(username=username).exists():
    #             errors["username"] = "Такого користувача не існує"
    #             return render(request, 'items/login.html', {'errors': errors})
    #
    #     password = request.POST.get("password", "").strip()
    #     if not password:
    #         errors["password"] = "Пароль є обов'язковим"
    #     else:
    #         user = authenticate(username=username, password=password)
    #         if user is not None:
    #             login_user(request, user)
    #             return redirect('item_list')
    #         else:
    #             errors["password"] = "Неправильний пароль"
    #
    #     if errors:
    #         return render(request, 'items/login.html', {'errors': errors})
    #
    # return render(request, 'items/login.html', {})


@login_required(login_url='/login/')
def logout(request):
    logout_user(request)
    return redirect('login')
