from enum import Enum
from time_candle.exceptions import AppException


class InvalidLoginException(AppException):
    def __init__(self, errors=None, message='The login is invalid! {}'):
        super().__init__(errors, message)


# Validators exceptions
class InvalidArgumentFormat(AppException):
    def __init__(self, errors=None, message='The argument is invalid! {}'):
        super().__init__(errors, message)


# Password related things
class InvalidTimeError(AppException):
    def __init__(self, errors=None, message='The time is invalid! {}'):
        super().__init__(errors, message)


class TimeMessages(Enum):
    # This is pre defined messages that will be associated with password all
    # over the project
    TIME_SHIFT = 'You cannot make tasks in the past'
    NOT_VALID_PERIOD = 'Yor period is too big in general or too small for ' \
                       'deadline'
    NO_DEADLINE = 'You must specify first deadline for this task'
    TIME_FORMAT = 'Time must be in YYYY-MM-DD H:M:S format'
    TIME_EPOCH = 'Time cannot create time below 1970\'s'
    NEGATIVE_PERIOD = 'Period cannot be negative'


# Status related things
class InvalidStatusError(AppException):
    def __init__(self, errors=None, message='The status is invalid! {}'):
        super().__init__(errors, message)


class StatusMessages(Enum):
    # This is pre defined messages that will be associated with password all
    # over the project
    EXPIRED_NOT_VALID = 'You cannot make done task as expired. First you have' \
                        ' to make task undone'
    ADD_EXPIRED = 'You cannot make expired tasks'
    CHILD_STATUS_UNEXPECTED = 'Not all child tasks were done. Please, check ' \
                              'them'
    CHANGE_PARENT_STATUS_DONE = 'Parent status is done, you cannot change ' \
                                'child to undone'
    MAKE_PARENT_STATUS_DONE = 'Parent status is done, you cannot make new ' \
                              'childs while it\'s true'


# Login related things
class InvalidLoginError(AppException):
    def __init__(self, errors=None, message='The login is invalid! {}'):
        super().__init__(errors, message)


class ProjectMessages(Enum):
    # This is pre defined messages that will be associated with projects all
    # over the project
    DO_NOT_HAVE_RIGHTS = 'You don\'t have rights to modify this project'


# Login related things
class InvalidParentError(AppException):
    def __init__(self, errors=None, message='The parent is invalid! {}'):
        super().__init__(errors, message)


class ParentMessages(Enum):
    # This is pre defined messages that will be associated with parent tasks all
    # over the project
    PARENT_HAS_PERIOD = 'You cannot create child task for the period task'
