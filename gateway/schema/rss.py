from apollo_shared.schema.base import Schema
from marshmallow import fields


class _RSSResponse(Schema):
    id = fields.Str(required=True)
    url = fields.Str(required=True)


class SubscribeRSSSchemaRequest(Schema):
    url = fields.Str(required=True)


class SubscribeRSSSchemaResponse(_RSSResponse):
    pass


class GetRSSesSchemaResponse(_RSSResponse):
    pass


class GetRSSSchemaResponse(_RSSResponse):
    pass


class _FeedResponse(Schema):
    id = fields.Str(required=True)
    data = fields.Dict(required=True)


class GetFeedsOfSubscribedRSSSchemaResponse(_FeedResponse):
    pass


class GetFeedSchemaRequest(Schema):
    id = fields.Str(required=True)


class GetFeedSchemaResponse(_FeedResponse):
    pass


class _BookmarksSchema(Schema):
    id = fields.Str(required=True)
    feed_id = fields.Str(required=True)


class GetBookmarksSchemaResponse(_BookmarksSchema):
    pass


class GetBookmarkSchemaResponse(_BookmarksSchema):
    pass


class AddToBookmarksSchemaRequest(Schema):
    feed_id = fields.Str(required=True)


class AddToBookmarksSchemaResponse(_BookmarksSchema):
    pass


class _CommentSchema(Schema):
    id = fields.Str(required=True)
    message = fields.Str(required=True)


class GetCommentsOnFeedSchemaResponse(_CommentSchema):
    pass


class GetCommentOnFeedSchemaResponse(_CommentSchema):
    pass


class AddCommentSchemaRequest(Schema):
    message = fields.Str(required=True)


class AddCommentSchemaResponse(Schema):
    id = fields.Str(required=True)
    message = fields.Str(required=True)
