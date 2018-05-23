from enums.priority import priority_dict
from enums.status import status_dict
import model.time_formatter


def print_tasks(tasks):
    for task in tasks:
        print_task(task)


def print_task(task):
    if task.deadline is not None:
        deadline_time = model.time_formatter.get_datetime(task.deadline)
    else:
        deadline_time = 'unlimited'

    if task.realization_time is not None:
        realization_time = model.\
            time_formatter.get_datetime(task.realization_time)
    else:
        realization_time = 'undone'

    print('Task: {}, \t tid: {}, \t creator: {}, \t receiver: {}, deadline: {}, status: '
          '{}, realization time: {}, priority: {}, project id: {}'.
          format(task.title, task.tid, task.creator_uid, task.uid,
                 deadline_time, status_dict[task.status], realization_time,
                 priority_dict[task.priority], task.pid))


def print_users(users):
    for user in users:
        print_user(user)


def print_user(user):
    print('login: {}, nickname: {}, about: {}, mail: {}, id: {}'.
          format(user.login, user.nickname, user.about, user.mail, user.uid))


def print_projects(projects):
    for project in projects:
        print_project(project)


def print_project(project):
    print('id: {}, title: {}, admin id: {}, description: {}'.
          format(project.pid, project.title, project.admin_uid,
                 project.description))
