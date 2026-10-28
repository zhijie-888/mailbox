"""
数据模型（Model）：定义“信件”在数据库里长什么样。
一张表 = 一个 Python 类；表里的字段 = 类的属性。
"""
from django.db import models


class Letter(models.Model):
    # to_id：收信人“识别码”。公开信固定存为字符串 "public"。
    to_id = models.CharField(max_length=64, db_index=True, verbose_name="收信人识别码")

    # from_id：发信人称呼，可选（不填就是“匿名”）。
    from_id = models.CharField(
        max_length=64, blank=True, null=True, verbose_name="发信人"
    )

    # content：信件正文。
    content = models.TextField(verbose_name="信件内容")

    # is_public：是否为公开信。True=所有人可见，False=仅指定收信人可见。
    is_public = models.BooleanField(default=False, verbose_name="是否公开")

    # created_at：发送时间，自动记录。
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")

    class Meta:
        ordering = ["-created_at"]  # 查询时默认按时间倒序（最新的在最前）
        verbose_name = "信件"
        verbose_name_plural = "信件"

    def __str__(self):
        return f"{(self.from_id or '匿名')} -> {self.to_id}"
