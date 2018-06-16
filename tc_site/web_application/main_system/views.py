from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, reverse
from main_system import forms
from time_candle.controller.commands import Controller
from tc_web import config


def signup(request):
    if request.method == 'POST':
        controller = Controller(uid=request.user.id,
                                psql_config=config.DATABASE_CONFIG)

        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            print(user.id)
            controller.add_user(username, user.id)

            raw_password = form.cleaned_data.get('password1')

            # login and redirect our user to the main page for better user
            # experience
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/tc_web/')
    else:
        form = forms.SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


def index(request):
    return redirect(reverse('tc_web:index'))
