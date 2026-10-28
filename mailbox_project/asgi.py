"""
ASGI 配置：用于支持 WebSocket / 异步（本项目用不到，保留默认即可）。
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mailbox_project.settings")

application = get_asgi_application()
