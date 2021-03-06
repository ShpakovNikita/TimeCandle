from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from time_candle.controller.commands import Controller
from main_system import (
    config,
    forms,
    logger,
    decorators,
)
from time_candle.exceptions import AppException


@decorators.startup_page_init('search')
def signup(request):
    print('signup')
    if request.method == 'POST':
        print('post form: %s', request.POST)
        if config.DATABASE_CONFIG:
            controller = Controller(uid=request.user.id,
                                    psql_config=config.DATABASE_CONFIG)
        elif config.DATABASE_PATH:
            print(config.DATABASE_PATH)
            controller = Controller(uid=request.user.id,
                                    db_file=config.DATABASE_PATH)
        else:
            controller = Controller(uid=request.user.id,
                                    connect_url=config.DATABASE_URL)

        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            print('Django user added')
            username = form.cleaned_data.get('username')

            try:
                controller.add_user(username, user.id)
                print('Time-candle user added')

            except AppException as e:
                # delete django user
                User.objects.get(username=username).delete()
                print(e.errors.value)
                return render(request, 'registration/signup.html',
                              {'form': form})

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
