from channels.routing import route_class
from channels.generic.websockets import WebsocketDemultiplexer

from lukask_app.bindings import PublicationBinding
from lukask_app.bindings import MultimediaBinding
from lukask_app.bindings import ActionPublicationBinding
from lukask_app.bindings import NotificationReceivedBinding


class ChannelApiAppDemultiplexer(WebsocketDemultiplexer):
    consumers = {
        'publication': PublicationBinding.consumer,
        'multimedia' : MultimediaBinding.consumer,
        'comments'   : ActionPublicationBinding.consumer,
        'notification_received' : NotificationReceivedBinding
    }

channel_routing = [
    route_class(ChannelApiAppDemultiplexer),
]