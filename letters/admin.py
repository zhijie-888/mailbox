"""
后台配置：把 Letter 注册到 Django 自带的后台（/admin/），
方便你登录后查看 / 删除信件。
"""
from django.contrib import admin

from .models import Letter


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ("id", "from_id", "to_id", "is_public", "created_at")
    list_filter = ("is_public", "created_at")
    search_fields = ("from_id", "to_id", "content")
