from model.main_instances.task import Task as TaskInstance
from storage import *
from model.session_control import Singleton, Adapters
import exceptions.model_exceptions as m_e
from model import logger
import model.tokenizer
import model.time_formatter
from enums.status import Status


def add_task(title, priority, status, deadline_time,
             parent_id, comment, pid, login):
    # add task to the database

    # This code is also checking is our parent tid exists in the database for
    # logged user. The max func needed to set tasks status and priority not
    # lower then parent's

    if parent_id is not None:
        parent_task = TaskInstance.make_task(
            Adapters.TASK_ADAPTER.get_task_by_id(parent_id, pid))
        status = max(status, parent_task.status)
        priority = max(priority, parent_task.priority)

    logger.debug('time in milliseconds %s' % deadline_time)

    # Check for rights and id's
    if login is None:
        task_uid = Singleton.GLOBAL_USER.uid
    else:
        Adapters.USER_ADAPTER.is_user_in_project(login, pid)
        task_uid = Adapters.USER_ADAPTER.get_id_by_login(login)

    if pid is not None:
        logger.debug('pid is not none')
        if task_uid != Singleton.GLOBAL_USER.uid:
            logger.debug('the receiver is not us')
            Adapters.PROJECT_ADAPTER.has_rights(pid)
        else:
            logger.debug('we are the receiver')
            Adapters.USER_ADAPTER.is_user_in_project(
                Singleton.GLOBAL_USER.login, pid)

    if deadline_time is not None and \
            model.time_formatter.time_stamp(deadline_time) < 0:
        raise m_e.InvalidTimeError(m_e.TimeMessages.TIME_STAMP)

    task = TaskInstance(task_uid,
                        Singleton.GLOBAL_USER.uid,
                        Adapters.TASK_ADAPTER.last_id() + 1,
                        deadline_time,
                        title,
                        pid,
                        status,
                        priority,
                        parent_id,
                        comment)

    logger.debug('task configured and ready to save , the task id is %s'
                 % task.tid)

    Adapters.TASK_ADAPTER.save(task)

    logger.debug('task added')


def remove_task(tid):
    # remove task from database
    Adapters.TASK_ADAPTER.remove_task_by_id(tid)


def change_task(tid, priority, status, time, comment):
    # change task in the database
    task = TaskInstance.make_task(Adapters.TASK_ADAPTER.get_task_by_id(tid))
    if priority is not None:
        task.priority = priority
    if status is not None:
        task.status = status
    if time is not None:
        task.deadline = time
    if comment is not None:
        task.comment = comment

    Adapters.TASK_ADAPTER.save(task)


def get_tasks(string_fil):
    # get tasks by filter
    fil = model.tokenizer.parse_string(string_fil)
    tasks = Adapters.TASK_ADAPTER.get_by_filter(fil)
    task_instances = [TaskInstance.make_task(task) for task in tasks]
    for task in task_instances:
        _update(task)
    print()
    # TODO: update query
    return task_instances


def _update(task):
    changed_flag = False
    if task.deadline is not None \
            and model.time_formatter.time_stamp(task.deadline) < 0 \
            and task.status == Status.IN_PROGRESS:
        task.status = Status.EXPIRED
        logger.debug('tasks status updated')
        changed_flag = True

    if changed_flag:
        Adapters.TASK_ADAPTER.save(task)
        logger.debug('task updated')
