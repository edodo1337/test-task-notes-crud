from dataclasses import asdict
from typing import Callable
from rest_framework.serializers import ValidationError

from notes.serializers import NoteCreateErrorResposne
from rest_framework.response import Response
from functools import wraps


def catch_exception_factory(get_error_code: Callable, get_status_code_by_error: Callable):
    def catch_exception(view: Callable):
        @wraps(view)
        def wrapper(*args, **kwargs):
            try:
                return view(*args, **kwargs)
            except ValidationError as ex:
                raise ex
            except Exception as ex:
                error_code = get_error_code(ex)
                status_code = get_status_code_by_error(error_code)

                return Response(
                    data=asdict(NoteCreateErrorResposne(error_msg=str(ex), error_code=error_code)),
                    status=status_code,
                )

        return wrapper

    return catch_exception
