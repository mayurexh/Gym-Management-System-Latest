from django.urls import re_path
from . import consumers

ws_patterns=[
	re_path(r'ws/notifications/',consumers.NotificationConsumer.as_asgi()),
]