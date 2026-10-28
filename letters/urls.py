"""
letters 应用的路由表：把具体网址映射到 views.py 里的函数。
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),                 # 首页（单页应用）
    path("api/send/", views.send_letter, name="send"),    # 发信
    path("api/inbox/", views.get_inbox, name="inbox"),    # 收私信
    path("api/public/", views.get_public, name="public"), # 取公开信
]
