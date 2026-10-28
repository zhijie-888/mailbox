"""
WSGI 配置：线上服务器（如 gunicorn）通过它来运行你的网站。
一般不用改。
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mailbox_project.settings")

application = get_wsgi_application()
