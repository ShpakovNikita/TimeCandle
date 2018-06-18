from copy import copy
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from django.http import Http404
from time_candle.controller.commands import Controller
from tc_web import config


# merge to object's fields and return one merged object
def merge_instances(obj_1, obj_2):
    buff_obj = copy(obj_1)
    for key, value in obj_2.__dict__.items():
        setattr(buff_obj, key, value)

    return buff_obj


# initialize form for user search
def search_user_forms(request, search_field='search', redirect_flag=True):
    if request.method == "GET":
        if search_field in request.GET:
            try:
                profile_uid = User.objects.get(
                    username=request.GET[search_field]).id
            except User.DoesNotExist:
                raise Http404

            if redirect_flag:
                return redirect(reverse('tc_web:profile', args=(profile_uid,)))
            else:
                return profile_uid


def get_controller(request):
    if config.DATABASE_CONFIG:
        controller = Controller(uid=request.user.id,
                                psql_config=config.DATABASE_CONFIG)
    else:
        controller = Controller(uid=request.user.id,
                                connect_url=config.DATABASE_URL)

    return controller
