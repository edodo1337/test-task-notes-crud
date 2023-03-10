# domain specific exceptions


class ProfileNotFound(Exception):
    ...


class PasswordDoesNotMatch(Exception):
    ...


class UserAlreadyExists(Exception):
    ...
