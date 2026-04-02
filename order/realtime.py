from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

ORDERS_GLOBAL_GROUP = 'orders'


def table_group_name(table_id: int) -> str:
    return f'table_{table_id}'


def broadcast_order_event(event_name: str, data: dict, table_id: int | None = None) -> None:
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return

    payload = {
        'type': 'order.event',
        'event': event_name,
        'data': data,
    }

    async_to_sync(channel_layer.group_send)(ORDERS_GLOBAL_GROUP, payload)

    if table_id is not None:
        async_to_sync(channel_layer.group_send)(
            table_group_name(table_id), payload)
