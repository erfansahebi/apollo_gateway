from nameko.rpc import RpcProxy
from apollo_shared.rpc.auth import AuthRPC as BaseAuthRPC
from apollo_shared.schema import auth as auth_schema


class AuthRPC(RpcProxy, BaseAuthRPC):

    def __init__(self, **kwargs):
        super(AuthRPC, self).__init__(self.name, **kwargs)
        self.rpc = None

    def setup(self, **kwargs):
        self.rpc = super(AuthRPC, self).setup()

    def get_dependency(self, worker_ctx):
        self.rpc = super(AuthRPC, self).get_dependency(worker_ctx)

        return self.rpc

    def register(self, data: auth_schema.RegisterSchemaRPC) -> auth_schema.RegisterSchemaRPCResponse:
        return self.rpc.register(data)

    def login(self, data: auth_schema.LoginSchemaRPC) -> auth_schema.LoginSchemaRPCResponse:
        return self.rpc.login(data)

    def logout(self, data: auth_schema.LogoutRPC) -> None:
        self.rpc.logout(data)

    def authenticate(self, data: auth_schema.AuthenticateRPC) -> auth_schema.AuthenticateRPCResponse:
        return self.rpc.authenticate(data)
