from graphql import GraphQLError



def permissions(*permission_functions, error_message='User not authorized'):
    def decorator(function):
        def wrapper(*args, **kwargs):
            for permission_function in permission_functions:
                if args[1] and hasattr(args[1], 'context'):
                    param = args[1].context
                else:
                    param = args[2].context

                if permission_function(param):
                    return function(*args, **kwargs)
            raise GraphQLError(error_message, extensions={'status_code': 403})

        return wrapper

    return decorator


def is_logged(context):
    return context is not None and context.user.is_authenticated

