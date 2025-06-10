import functools
import exceptions


def normal_response(code):
    def decorator_func(func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            retval = func(*args, **kwargs)
            if isinstance(retval, tuple):
                return retval
            return retval, code

        return wrapper_func

    return decorator_func


def expected_errors(*errors):
    def decorator_func(func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            try:
                rv = func(*args, **kwargs)
                return rv
            except exceptions.MyBaseException as exc:
                if exc.code not in errors:
                    msg = f'Unexpected error code {exc.code} {exc.final_message()}!!!'
                    print(msg)
                    # LOG.exception(msg)
                    return {"message": msg}, 500
                # LOG.error(exc.message)
                return exc.final_message(), exc.code
            except Exception as exc:  # pylint: disable=W0718
                msg = f'Unexpected error code {str(exc)}!!!'
                print(msg)
                # LOG.exception(msg)
                return {"message": msg}, 500

        return wrapper_func

    return decorator_func
