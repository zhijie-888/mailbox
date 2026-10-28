"""
Django 设置文件（项目的“总开关”）。
这里集中配置：数据库、静态文件、允许访问的域名、安装的应用等。
注释用中文写，方便你之后对照学习。
"""
import os
from pathlib import Path

# 项目根目录（manage.py 所在的上一层）
BASE_DIR = Path(__file__).resolve().parent.parent

# ===== 安全密钥 =====
# 本地用一个占位密钥；上线时请在 Render 的环境变量里设置 DJANGO_SECRET_KEY。
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "dev-insecure-key-change-me-in-production-0123456789abcdef",
)

# ===== 调试开关 =====
# 本地开发设为 True（报错会显示详细页面）；上线务必设为 False。
DEBUG = os.getenv("DEBUG", "True") == "True"

# ===== 允许访问的域名 =====
# 本地是 127.0.0.1 / localhost；上线填你的网址。
# 默认 "*" 表示任意域名都能访问（方便部署），正式上线建议改成你自己的域名。
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# ===== 已安装的应用 =====
INSTALLED_APPS = [
    "django.contrib.admin",        # 后台管理
    "django.contrib.auth",         # 用户认证（本项目没用到登录，但 Django 需要它）
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",  # 静态文件（CSS/JS/图片）支持
    "letters",                     # 我们自己写的“信箱”应用
]

# ===== 中间件（请求处理管道）=====
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # 线上用它来托管静态文件，免配置
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",    # 防跨站请求伪造
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mailbox_project.urls"  # 路由文件位置

# ===== 模板（HTML 页面）配置 =====
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # 我们的 index.html 放在这里
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mailbox_project.wsgi.application"

# ===== 数据库 =====
# 如果设置了 DATABASE_URL 环境变量（线上 Postgres），就用它；否则用本地 SQLite。
# dj-database-url 负责把 "postgres://..." 这种网址自动转成 Django 配置。
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
    )
}

# ===== 密码强度校验（保留 Django 默认即可）=====
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ===== 语言与时区 =====
LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True

# ===== 静态文件配置 =====
STATIC_URL = "static/"                 # 浏览器访问静态文件的地址前缀
STATIC_ROOT = BASE_DIR / "staticfiles" # 上线时 collectstatic 把文件收集到这里
STATICFILES_DIRS = [BASE_DIR / "static"]  # 开发时从这里读取 CSS/JS

# 用 whitenoise 压缩并高效托管静态文件（上线推荐）
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
