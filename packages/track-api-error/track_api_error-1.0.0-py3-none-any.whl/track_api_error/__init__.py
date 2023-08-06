from rest_framework.response import Response
from rest_framework import status


def track_error(view_func):
    """
    This decorator is used to track errors that occur in the API views.
    It wraps around the view function and catches any exceptions that occur during execution.
    In case of an exception, the error is logged with the class name of the API and the request data.
    The function then returns a 406 NOT ACCEPTABLE response with the error message.
    """

    def wrapper(self, request, *args, **kwargs):
        try:
            return view_func(self, request, *args, **kwargs)
        except Exception as e:
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    "error": True,
                    "data": [],
                    "message": str(e),
                },
            )

    return wrapper