import functools
from apollo_shared.rpc.auth import AuthRPC
from werkzeug import Request
from nameko.rpc import ServiceRpc
from gateway.utils import get_context
from apollo_shared.schema.auth import AuthenticateRPC


class AuthMiddleware(ServiceRpc):

    def __init__(self, **kwargs):
        super().__init__(AuthRPC.name, **kwargs)

    def auth(self, *parent_args, **parent_kwargs):
        def wrapper(func, *wrap_args):
            @functools.wraps(func)
            def decorator(svc, request, *args, **kwargs):
                context = get_context(request)

                if context['token'] is None:
                    raise Exception('no token')

                auth_rpc: AuthRPC = getattr(svc, self.attr_name)
                authenticate_response = auth_rpc.authenticate(AuthenticateRPC().load({
                    'token': context['token']
                }))

                context['user_id'] = authenticate_response['user_id']

                request.context = context

                return func(svc, request, *args, **kwargs)

            return decorator

        if parent_args and callable(parent_args[0]):
            return wrapper(parent_args[0])

        return wrapper

    def guest(self, *parent_args, **parent_kwargs):
        def wrapper(func, *wrap_args):
            @functools.wraps(func)
            def decorator(svc, request: Request, *args, **kwargs):
                context = get_context(request)

                if context.token is not None:
                    raise Exception('have token')

                return func(svc, request, *args, **kwargs)

            return decorator

        if parent_args and callable(parent_args[0]):
            return wrapper(parent_args[0])

        return wrapper
