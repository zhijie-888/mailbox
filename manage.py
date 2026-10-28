#!/usr/bin/env python
"""Django 的命令行入口：用来执行 migrate / runserver / createsuperuser 等命令。"""
import os
import sys


def main():
    # 告诉 Django 用哪个设置文件（mailbox_project/settings.py）
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mailbox_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "找不到 Django。请确认已安装（pip install -r requirements.txt），"
            "并且当前在虚拟环境中。"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
