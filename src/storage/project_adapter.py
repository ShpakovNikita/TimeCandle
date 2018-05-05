import app_logger
from peewee import *
from storage.adapter_classes import Project
from singleton import Singleton
from main_instances.project import Project as ProjectInstance
import exceptions.db_exceptions as db_e


def save(project):
    """
    This function is used to store given project in database
    :param project: This is our task to save
    :type project: ProjectInstance
    :return: None
    """

    Project.create(admin=project.admin_uid,
                   decription=project.description,
                   title=project.title)
    app_logger.custom_logger('storage').debug('project saved to database')


def last_id():
    """
    This function gets last id to add project on it's place
    TODO:
    This function finds the first unused id in the table to add new project row
    on that place
    :return: Int
    """

    query = Project.select().order_by(Project.id.desc())
    app_logger.custom_logger('storage').debug('getting last id from query...{}'
                                              .format(query))

    try:
        return query.get().id

    except DoesNotExist:
        return 1


def get_project_by_id(pid):
    """
    This function finds project by id and current user in database and returns
    it or raise error due to incorrect request
    :param pid: Project id to find
    :type pid: Int
    :return: Project
    """
    # TODO: FIX (need relations)
    project = Project.select().\
        where((Project.id == pid) &
              ((Project.creator == Singleton.GLOBAL_USER.uid) |
               (Project.receiver == Singleton.GLOBAL_USER.uid)))
    try:
        return _storage_to_model(project.get())

    except DoesNotExist:
        app_logger.custom_logger('storage').info('There is no such pid %s in '
                                                 'the database for your user' %
                                                 pid)
        raise db_e.InvalidTidError(db_e.TaskMessages.TASK_DOES_NOT_EXISTS)


def _storage_to_model(storage_project):
    """
    This function converts storage project to model project
    :type storage_project: Project
    :return: ProjectInstance
    """
    app_logger.custom_logger('storage').\
        debug('convert storage to model project')

    model_project = ProjectInstance(storage_project.id,
                                    storage_project.admin.id)

    return model_project
