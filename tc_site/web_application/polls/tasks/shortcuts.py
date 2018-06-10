from django.shortcuts import redirect
from time_candle.exceptions import AppException
from time_candle.enums.status import Status
from time_candle.model.time_formatter import get_datetime


def task_card_post_form(request, controller, redirect_link):
    if request.method == 'POST':
        if 'delete' in request.POST:
            try:
                controller.remove_task(request.POST['delete'])
                return redirect(redirect_link)
            except AppException:
                pass

        elif 'check' in request.POST:
            try:
                controller.change_task(
                    request.POST['check'], status=Status.DONE)
                return redirect(redirect_link)
            except AppException as e:
                print(e.errors)


def init_tasks(request, controller, tasks_list):
    for task in tasks_list:
        task.pid = 1
        if task.deadline is not None:
            task.deadline = get_datetime(task.deadline)
        else:
            task.deadline = None

        if task.pid is not None:
            task.project_name = controller.get_project(task.pid).title
            if task.uid == request.user.id:
                task.receiver_name = 'You'
            else:
                task.receiver_name = controller.get_user(task.uid).login