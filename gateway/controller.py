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

        response_data = auth_schema.RegisterSchemaResponse().dumps({
            **register_response,
            "username": validated_data['username'],
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

        response_data = auth_schema.LoginSchemaResponse().dumps({
            **login_response,
            'username': validated_data['username'],
        })

        return Response(
            response=response_data,
            mimetype='application/json',
        )

    @http('POST', '/auth/logout')
    @auth_middleware.auth
    def logout(self, request: Request) -> Response:
        context = get_context(request)
        validated_data = auth_service_schema.LogoutRPC(unknown=EXCLUDE).load({
            'token': context['token'],
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
        validated_data = rss_service_schema.GetRSSesSchemaRPC().load({})

        get_rsses_response = self.rss_rpc.get_rsses(context, validated_data)

        response_data = rss_schema.GetRSSesSchemaResponse(many=True).dumps(get_rsses_response)

        return Response(
            response=response_data,
            mimetype='application/json',
        )

    @http('POST', '/rsses')
    @auth_middleware.auth
    def subscribe_rss(self, request: Request) -> Response:
        rss_schema.SubscribeRSSSchemaRequest().validate(request.json)
        validated_data = rss_service_schema.SubscribeRSSSchemaRPC().load(request.json)

        context = get_context(request)

        subscribe_response = self.rss_rpc.subscribe_rss(context, validated_data)

        response_data = rss_schema.SubscribeRSSSchemaResponse().dumps(subscribe_response)

        return Response(
            response=response_data,
            mimetype='application/json',
        )

    @http('GET', '/rsses/<rss_id>')
    @auth_middleware.auth
    def get_rss(self, request: Request, rss_id) -> Response:
        validated_data = rss_service_schema.GetRSSSchemaRPC().load({
            'id': rss_id,
        })

        context = get_context(request)

        get_rss_response = self.rss_rpc.get_rss(context, validated_data)

        response_data = rss_schema.GetRSSSchemaResponse().dumps(get_rss_response)

        return Response(
            response=response_data,
            mimetype='application_json',
        )

    @http('DELETE', '/rsses/<rss_id>')
    @auth_middleware.auth
    def unsubscribe_rss(self, request: Request, rss_id) -> Response:
        validated_data = rss_service_schema.UnsubscribeRSSSchemaRPC().load({
            'id': rss_id,
        })

        context = get_context(request)

        self.rss_rpc.unsubscribe_rss(context, validated_data)

        return Response(
            response={},
            mimetype='application/json',
        )

    @http('GET', '/feeds')
    @auth_middleware.auth
    def get_feeds_of_subscribed_rsses(self, request: Request) -> Response:
        validated_data = rss_service_schema.GetFeedsOfSubscribedRSSesSchemaRPC().load({})
        context = get_context(request)

        feeds = self.rss_rpc.get_feeds_of_subscribed_rsses(context, validated_data)

        response_data = rss_schema.GetFeedSchemaResponse(many=True).dumps(feeds)

        return Response(
            response=response_data,
            mimetype='application/json',
        )

    @http('GET', '/feeds/<feed_id>')
    @auth_middleware.auth
    def get_feed_of_subscribed_rss(self, request: Request, feed_id) -> Response:
        validated_data = rss_service_schema.GetFeedOfSubscribedRSSSchemaRPC().load({
            'id': feed_id,
        })
        context = get_context(request)

        feed = self.rss_rpc.get_feed_of_subscribed_rss(context, validated_data)

        response_data = rss_schema.GetFeedSchemaResponse().dumps(feed)

        return Response(
            response=response_data,
            mimetype='application/json',
        )

    @http('GET', '/rsses/<rss_id>/feeds')
    @auth_middleware.auth
    def get_feeds_of_subscribed_rss(self, request: Request, rss_id) -> Response:
        validated_data = rss_service_schema.GetFeedsOfSubscribedRSSSchemaRPC().load({
            'rss_id': rss_id,
        })

        context = get_context(request)

        feeds = self.rss_rpc.get_feeds_of_subscribed_rss(context, validated_data)

        response_data = rss_schema.GetFeedsOfSubscribedRSSSchemaResponse(many=True).dumps(feeds)

        return Response(
            response=response_data,
            mimetype='application/json',
        )

    @http('GET', '/bookmarks')
    @auth_middleware.auth
    def get_bookmarks(self, request: Request) -> Response:
        validated_data = rss_service_schema.GetBookmarksSchemaRPC().load({})
        context = get_context(request)
        bookmarks = self.rss_rpc.get_bookmarks(context, validated_data)
        response_data = rss_schema.GetBookmarksSchemaResponse(many=True).dumps(bookmarks)

        return Response(
            response=response_data,
            mimetype='application/json',
        )

    @http('GET', '/bookmarks/<bookmark_id>')
    @auth_middleware.auth
    def get_bookmark(self, request: Request, bookmark_id) -> Response:
        validated_data = rss_service_schema.GetBookmarkSchemaRPC().load({
            'bookmark_id': bookmark_id,
        })
        context = get_context(request)
        bookmark = self.rss_rpc.get_bookmark(context, validated_data)
        response_data = rss_schema.GetBookmarkSchemaResponse().dumps(bookmark)

        return Response(
            response=response_data,
            mimetype='application/json',
        )

    @http('POST', '/bookmarks')
    @auth_middleware.auth
    def add_to_bookmarks(self, request: Request) -> Response:
        rss_schema.AddToBookmarksSchemaRequest().validate(request.json)
        validated_data = rss_service_schema.AddToBookmarksSchemaRPC().load(request.json)
        context = get_context(request)
        new_bookmark = self.rss_rpc.add_to_bookmarks(context, validated_data)

        response_data = rss_schema.AddToBookmarksSchemaResponse().dumps(new_bookmark)

        return Response(
            response=response_data,
            mimetype='application/json',
        )

    @http('DELETE', '/bookmarks/<bookmark_id>')
    @auth_middleware.auth
    def delete_from_bookmarks(self, request: Request, bookmark_id) -> Response:
        validated_data = rss_service_schema.DeleteFromBookmarksSchemaRPC().load({
            'bookmark_id': bookmark_id,
        })
        context = get_context(request)
        self.rss_rpc.delete_from_bookmarks(context, validated_data)
        return Response(
            response=json.dumps({}),
            mimetype='application/json',
        )

    @http('GET', '/feeds/<feed_id>/comments')
    @auth_middleware.auth
    def get_comments_on_feed(self, request: Request, feed_id) -> Response:
        validated_data = rss_service_schema.GetCommentsOnFeedSchemaRPC().load({
            'feed_id': feed_id,
        })
        context = get_context(request)
        comments = self.rss_rpc.get_comments_on_feed(context, validated_data)

        response_data = rss_schema.GetCommentsOnFeedSchemaResponse(many=True).dumps(comments)

        return Response(
            response=response_data,
            mimetype='application/json',
        )

    @http('GET', '/feeds/<feed_id>/comments/<comment_id>')
    @auth_middleware.auth
    def get_comment_on_feed(self, request: Request, feed_id, comment_id) -> Response:
        validated_data = rss_service_schema.GetCommentOnFeedSchemaRPC().load({
            'feed_id': feed_id,
            'comment_id': comment_id,
        })
        context = get_context(request)
        comments = self.rss_rpc.get_comment_on_feed(context, validated_data)

        response_data = rss_schema.GetCommentOnFeedSchemaResponse().dumps(comments)

        return Response(
            response=response_data,
            mimetype='application/json',
        )

    @http('POST', '/feeds/<feed_id>/comments')
    @auth_middleware.auth
    def add_comment_on_feed(self, request: Request, feed_id) -> Response:
        rss_schema.AddCommentSchemaRequest().validate(request.json)
        validated_data = rss_service_schema.AddCommentOnFeedSchemaRPC().load({
            **request.json,
            'feed_id': feed_id,
        })
        context = get_context(request)
        new_comment = self.rss_rpc.add_comment_on_feed(context, validated_data)

        response_data = rss_schema.AddCommentSchemaResponse().dumps(new_comment)

        return Response(
            response=response_data,
            mimetype='application/json',
        )

    @http('DELETE', '/feeds/<feed_id>/comments/<comment_id>')
    @auth_middleware.auth
    def delete_comment_from_feed(self, request: Request, feed_id, comment_id) -> Response:
        validated_data = rss_service_schema.DeleteCommentOnFeedSchemaRPC().load({
            'comment_id': comment_id,
        })
        context = get_context(request)
        self.rss_rpc.delete_comment_on_feed(context, validated_data)

        return Response(
            response=json.dumps({}),
            mimetype='application/json',
        )
