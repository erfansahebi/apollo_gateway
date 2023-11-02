from apollo_shared.schema.base import Schema
from marshmallow import fields, validates_schema


class _AuthenticateSchemaResponse(Schema):
    user_id = fields.Str(required=True)
    username = fields.Str(required=True)
    token = fields.Str(required=True)


class RegisterSchemaRequest(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    confirm_password = fields.Str(required=True)

    @validates_schema
    def validate_confirm_password(self, data, **kwargs):
        if data['password'] != data['confirm_password']:
            raise Exception('Your password and confirmation password do not match.')


class RegisterSchemaResponse(_AuthenticateSchemaResponse):
    pass


class LoginSchemaRequest(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class LoginSchemaResponse(_AuthenticateSchemaResponse):
    pass
