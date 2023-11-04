from apollo_shared.utils import Context
from nameko.rpc import RpcProxy
from apollo_shared.rpc.rss import RssRPC as BaseRssRPC
from apollo_shared.schema import rss as rss_schema


class RssRPC(RpcProxy, BaseRssRPC):

    def __init__(self, **kwargs):
        super(RssRPC, self).__init__(self.name, **kwargs)
        self.rpc = None

    def setup(self, **kwargs):
        self.rpc = super(RssRPC, self).setup()
        self.rpc = None

    def get_dependency(self, worker_ctx):
        self.rpc = super(RssRPC, self).get_dependency(worker_ctx)

        return self.rpc

    def subscribe_rss(self,
                      context: Context,
                      data: rss_schema.SubscribeRSSSchemaRPC
                      ) -> rss_schema.SubscribeRSSSchemaRPCResponse:
        return self.rpc.subscribe_rss(context, data)

    def get_rsses(self,
                  context: Context,
                  data: rss_schema.GetRSSesSchemaRPC
                  ) -> rss_schema.GetRSSesSchemaRPCResponse:
        return self.rpc.get_rsses(context, data)

    def get_rss(self,
                context: Context,
                data: rss_schema.GetRSSSchemaRPC
                ) -> rss_schema.GetRSSSchemaRPCResponse:
        return self.rpc.get_rss(context, data)

    def unsubscribe_rss(self,
                        context: Context,
                        data: rss_schema.UnsubscribeRSSSchemaRPC
                        ) -> rss_schema.UnsubscribeRSSSchemaRPCResponse:
        return self.rpc.unsubscribe_rss(context, data)

    def get_feed_of_subscribed_rss(self,
                                   context: Context,
                                   data: rss_schema.GetFeedOfSubscribedRSSSchemaRPC
                                   ) -> rss_schema.GetFeedOfSubscribedRSSSchemaRPCResponse:
        return self.rpc.get_feed_of_subscribed_rss(context, data)

    def get_feeds_of_subscribed_rsses(self,
                                      context: Context,
                                      data: rss_schema.GetFeedsOfSubscribedRSSesSchemaRPC
                                      ) -> rss_schema.GetFeedsOfSubscribedRSSesSchemaRPCResponse:
        return self.rpc.get_feeds_of_subscribed_rsses(context, data)

    def get_feeds_of_subscribed_rss(self,
                                    context: Context,
                                    data: rss_schema.GetFeedsOfSubscribedRSSSchemaRPC
                                    ) -> rss_schema.GetFeedsOfSubscribedRSSSchemaRPCResponse:
        return self.rpc.get_feeds_of_subscribed_rss(context, data)

    def add_comment_on_feed(self,
                            context: Context,
                            data: rss_schema.AddCommentOnFeedSchemaRPC
                            ) -> rss_schema.AddCommentOnFeedSchemaRPCResponse:
        return self.rpc.add_comment_on_feed(context, data)

    def get_comments_on_feed(self,
                             context: Context,
                             data: rss_schema.GetCommentsOnFeedSchemaRPC
                             ) -> rss_schema.GetCommentsOnFeedSchemaRPCResponse:
        return self.rpc.get_comments_on_feed(context, data)

    def get_comment_on_feed(self,
                            context: Context,
                            data: rss_schema.GetCommentOnFeedSchemaRPC
                            ) -> rss_schema.GetCommentOnFeedSchemaRPCResponse:
        return self.rpc.get_comment_on_feed(context, data)

    def delete_comment_on_feed(self,
                               context: Context,
                               data: rss_schema.DeleteCommentOnFeedSchemaRPC
                               ) -> rss_schema.DeleteCommentOnFeedSchemaRPCResponse:
        return self.rpc.delete_comment_on_feed(context, data)

    def add_to_bookmarks(self,
                         context: Context,
                         data: rss_schema.AddToBookmarksSchemaRPC
                         ) -> rss_schema.AddToBookmarksSchemaRPCResponse:
        return self.rpc.add_to_bookmarks(context, data)

    def get_bookmarks(self,
                      context: Context,
                      data: rss_schema.GetBookmarksSchemaRPC
                      ) -> rss_schema.GetBookmarksSchemaRPCResponse:
        return self.rpc.get_bookmarks(context, data)

    def get_bookmark(self,
                     context: Context,
                     data: rss_schema.GetBookmarkSchemaRPC
                     ) -> rss_schema.GetBookmarkSchemaRPCResponse:
        return self.rpc.get_bookmark(context, data)

    def delete_from_bookmarks(self,
                              context: Context,
                              data: rss_schema.DeleteFromBookmarksSchemaRPC
                              ) -> rss_schema.DeleteFromBookmarksSchemaRPCResponse:
        return self.rpc.delete_from_bookmarks(context, data)
