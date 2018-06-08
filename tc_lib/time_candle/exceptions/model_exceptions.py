from enum import Enum
from . import AppException


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
    TIME_SHIFT = 'You cannot create tasks in the past'
    NOT_VALID_PERIOD = 'Yor period is too big in general or too small for ' \
                       'deadline'
    NO_DEADLINE = 'You must specify first deadline for period task'


# Status related things
class InvalidStatusError(AppException):
    def __init__(self, errors=None, message='The status is invalid! {}'):
        super().__init__(errors, message)


class StatusMessages(Enum):
    # This is pre defined messages that will be associated with password all
    # over the project
    EXPIRED_NOT_VALID = 'You cannot make done task as expired. First you have' \
                        ' to make task undone'
