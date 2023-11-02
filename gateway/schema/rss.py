from apollo_shared.schema.base import Schema
from marshmallow import fields


class _RSSResponse(Schema):
    id = fields.Str(required=True)
    url = fields.Str(required=True)


class SubscribeRSSSchemaRequest(Schema):
    url = fields.Str(required=True)


class SubscribeRSSSchemaResponse(_RSSResponse):
    pass


class GetRSSesResponse(_RSSResponse):
    pass


class GetRSSResponse(_RSSResponse):
    pass


class _FeedResponse(Schema):
    id = fields.Str(required=True)
    data = fields.Dict(required=True)


class GetFeedsOfSubscribedRSSResponse(_FeedResponse):
    pass


class GetFeedResponse(_FeedResponse):
    pass
