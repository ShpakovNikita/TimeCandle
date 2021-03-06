from django.http import (
    HttpResponse,
    Http404,
)
from django.shortcuts import render, redirect
from django.urls import reverse
from time_candle.exceptions import AppException
from tc_web import (
    forms,
    logger,
)
from main_system import (
    shortcuts,
    decorators,
)
from django.contrib.auth.models import User
import json
from django.contrib.auth.decorators import login_required


def err404(request, exception):
    logger.debug('Http404 error raised')
    return render(
        request, 'tc_web/404.html', status=404)


def err500(request, exception):
    logger.debug('Http500 error raised')
    return render(
        request, 'tc_web/500.html', status=500)


@decorators.startup_page_init('search')
def index(request):
    return render(request, 'tc_web/index.html')


@decorators.startup_page_init('search')
def profile(request, user_id):
    controller = shortcuts.get_controller(request)
    context = {}

    try:
        django_user = User.objects.get(id=user_id)
        lib_user = controller.get_user(user_id)
    except (User.DoesNotExist, AppException):
        raise Http404

    # merge two user objects to get one full user info
    screen_user = shortcuts.merge_instances(django_user, lib_user)
    context['screen_user'] = screen_user

    if user_id == request.user.id:
        logger.debug('rendering delete button')

        if request.method == 'POST':
            logger.debug(request.POST)
            if 'delete' in request.POST:
                controller.remove_message(request.POST['delete'])
                return redirect(request.META.get('HTTP_REFERER'))

        logger.debug('getting our messages')
        messages = controller.get_messages()
        context['messages'] = messages

    return render(request, 'tc_web/profile.html', context)


# function for autocomplete user search
def get_users(request):
    logger.debug('ajax request to get all users has been sent')

    if request.is_ajax():
        q = request.GET.get('term', '')
        re = '^' + q + '+'
        users = User.objects.filter(username__regex=re)
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.id
            user_json['label'] = user.username
            user_json['value'] = user.username
            results.append(user_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'
    logger.debug('ajax request was accepted')
    return HttpResponse(data, mimetype)


# function for autocomplete project user search
def get_project_users(request, project_id):
    logger.debug('ajax request to get project users has been sent')
    controller = shortcuts.get_controller(request)
    logger.debug('users were taken from controller')

    if request.is_ajax():
        q = request.GET.get('term', '')
        users = controller.get_users(project_id)
        users = [user for user in users if user.login.startswith(q)]
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.uid
            user_json['label'] = user.login
            user_json['value'] = user.login
            results.append(user_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'
    logger.debug('ajax request was accepted')
    return HttpResponse(data, mimetype)


@login_required
@decorators.startup_page_init('search')
def change_profile(request, user_id):
    context = {}
    controller = shortcuts.get_controller(request)

    if request.method == 'POST':
        form = forms.ChangeProfileForm(request.POST)
        if form.is_valid():
            about = form.cleaned_data.get('about')
            nickname = form.cleaned_data.get('nickname')
            try:
                controller.change_user(user_id, nickname, about)
                logger.debug('user was changed')
                return redirect(reverse('tc_web:profile', args=(user_id,)))

            except AppException as e:
                context['errors'] = e.errors.value

    else:
        form = forms.ChangeProfileForm()
        user = controller.get_user(user_id)

        # init fields with default values
        form.fields['nickname'].widget.attrs.update({'value': user.nickname})
        form.fields['about'].widget.attrs.update({'value': user.about})

    context['form'] = form

    return render(request, 'tc_web/change_profile.html', context)
