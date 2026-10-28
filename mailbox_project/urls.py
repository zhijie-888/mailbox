"""
总路由表：把不同的网址分配给对应的处理函数（视图）。
- 后台：/admin/
- 其余网址（首页、发信、收信、公开信）都交给 letters 应用处理
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),        # Django 自带的后台
    path("", include("letters.urls")),       # 把根路径下的所有路由交给 letters 应用
]
