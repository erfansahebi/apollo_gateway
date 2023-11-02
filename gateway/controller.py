import json
from .utils import *
from apollo_shared.schema import auth as auth_service_schema
from apollo_shared.schema import rss as rss_service_schema
from gateway.schema import auth as auth_schema, rss as rss_schema
from gateway.entrypoint import http
from werkzeug import Request, Response
from marshmallow import EXCLUDE
from .service.auth import AuthRPC
from .service.rss import RssRPC
from .middleware.auth import AuthMiddleware


class GatewayController(object):
    name = 'gateway'

    auth_rpc = AuthRPC()
    rss_rpc = RssRPC()

    auth_middleware = AuthMiddleware()

    @http('POST', '/auth/register')
    @auth_middleware.guest
    def register(self, request: Request) -> Response:
        auth_schema.RegisterSchemaRequest().validate(request.json)
        validated_data = auth_service_schema.RegisterSchemaRPC(unknown=EXCLUDE).load(request.json)
        register_response = self.auth_rpc.register(validated_data)

        response_data = auth_schema.RegisterSchemaResponse().dump({
            'user_id': register_response['user_id'],
            'username': validated_data['username'],
            'token': register_response['token'],
        })

        return Response(
            response=response_data,
            mimetype='application/json',
        )

    @http('POST', '/auth/login')
    @auth_middleware.guest
    def login(self, request: Request) -> Response:
        auth_schema.LoginSchemaRequest().validate(request.json)
        validated_data = auth_service_schema.LoginSchemaRPC(unknown=EXCLUDE).load(request.json)
        login_response = self.auth_rpc.login(validated_data)

        response_data = auth_schema.LoginSchemaResponse().dump({
            'user_id': login_response['user_id'],
            'username': validated_data['username'],
            'token': login_response['token'],
        })

        return Response(
            response=response_data,
            mimetype='application/json',
        )

    @http('POST', '/auth/logout')
    @auth_middleware.auth
    def logout(self, request: Request) -> Response:
        validated_data = auth_service_schema.LogoutRPC(unknown=EXCLUDE).load({
            'token': get_context(request).token,
        })

        self.auth_rpc.logout(validated_data)

        return Response(
            response=json.dumps({}),
            mimetype='application/json',
        )

    @http('GET', '/rsses')
    @auth_middleware.auth
    def get_rsses(self, request: Request) -> Response:
        context = get_context(request)
        validated_data = rss_service_schema.GetRSSesSchemaRPC().load()

        get_rsses_response = self.rss_rpc.get_rsses(context, validated_data)

        response_data = rss_schema.GetRSSesResponse(many=True).dump(validated_data)

    @http('POST', '/rsses')
    @auth_middleware.auth
    def subscribe_rss(self, request: Request) -> Response:
        rss_schema.SubscribeRSSSchemaRequest().validate(request.json)
        context = get_context(request)
        validated_data = rss_service_schema.SubscribeRSSSchemaRPC().load(request.json)

        subscribe_response = self.rss_rpc.subscribe_rss(context, validated_data)

        response_data = rss_schema.SubscribeRSSSchemaResponse().dump({
            'id': subscribe_response['id'],
            'url': subscribe_response['url'],
        })

        return Response(
            response=response_data,
            mimetype='application/json',
        )

    @http('GET', '/rsses/<rss_id>')
    @auth_middleware.auth
    def get_rss(self, request: Request, rss_id) -> Response:
        pass

    @http('DELETE', '/rsses/<rss_id>')
    @auth_middleware.auth
    def unsubscribe_rss(self, request: Request, rss_id) -> Response:
        context = get_context(request)

        self.rss_rpc.unsubscribe_rss(context, rss_service_schema.UnsubscribeRSSSchemaRPC().load({
            "id": rss_id,
        }))

        return Response(
            response={},
            mimetype='application/json',
        )

    @http('GET', '/feeds')
    @auth_middleware.auth
    def get_feeds_of_subscribed_rss(self, request: Request) -> Response:
        pass

    @http('GET', '/feeds/<feed_id>')
    @auth_middleware.auth
    def get_feed_of_subscribed_rss(self, request: Request, feed_id) -> Response:
        pass
