from urllib.parse import parse_qs

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .realtime import ORDERS_GLOBAL_GROUP, table_group_name


class OrderUpdatesConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.subscribed_groups: set[str] = set()

        await self.channel_layer.group_add(ORDERS_GLOBAL_GROUP, self.channel_name)
        self.subscribed_groups.add(ORDERS_GLOBAL_GROUP)

        raw_query = self.scope.get('query_string', b'').decode()
        query_params = parse_qs(raw_query)
        table_param = (query_params.get('table') or [None])[0]

        if table_param and table_param.isdigit():
            table_group = table_group_name(int(table_param))
            await self.channel_layer.group_add(table_group, self.channel_name)
            self.subscribed_groups.add(table_group)

        await self.accept()
        await self.send_json(
            {
                'event': 'socket_connected',
                'data': {
                    'groups': sorted(self.subscribed_groups),
                },
            }
        )

    async def disconnect(self, _close_code):
        for group_name in self.subscribed_groups:
            await self.channel_layer.group_discard(group_name, self.channel_name)

    async def receive_json(self, content, **_kwargs):
        action = str(content.get('action', '')).strip().lower()
        table_id = content.get('table_id')

        if action not in {'subscribe_table', 'unsubscribe_table'}:
            await self.send_json(
                {
                    'event': 'socket_error',
                    'data': {'detail': 'Accion no soportada.'},
                }
            )
            return

        if not str(table_id).isdigit():
            await self.send_json(
                {
                    'event': 'socket_error',
                    'data': {'detail': 'table_id invalido.'},
                }
            )
            return

        table_group = table_group_name(int(table_id))

        if action == 'subscribe_table':
            await self.channel_layer.group_add(table_group, self.channel_name)
            self.subscribed_groups.add(table_group)
            await self.send_json(
                {
                    'event': 'subscribed_table',
                    'data': {'table_id': int(table_id)},
                }
            )
            return

        await self.channel_layer.group_discard(table_group, self.channel_name)
        self.subscribed_groups.discard(table_group)
        await self.send_json(
            {
                'event': 'unsubscribed_table',
                'data': {'table_id': int(table_id)},
            }
        )

    async def order_event(self, event):
        await self.send_json(
            {
                'event': event.get('event', 'unknown_event'),
                'data': event.get('data', {}),
            }
        )
