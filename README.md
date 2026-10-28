# 密信 · Mailbox

一个**无需登录**的在线信箱网站：

- 📨 **指定收信**：输入一个「识别码」（例如 `alice-2026`），信件只发给这个码对应的人；对方在「收信」里输入同样的码即可读取。
- 🌐 **公开信板**：发公开信，所有人都能在「公开信板」看到，每 5 秒自动刷新（类实时）。
- 🎨 **高端界面**：深蓝主调 + 玻璃拟态卡片，响应式适配手机/电脑。
- 🧱 **技术栈**：后端 **Django**（Python），前端 **HTML + CSS + 原生 JS**。没有登录系统，结构清晰，适合学习。

> 思路：识别码就相当于一个「信箱编号」。没有账号体系，谁知道这个码、谁就能收信——所以请把私密识别码私下告诉对方。

---

## 目录结构

```
mailbox/
├── manage.py                 # Django 命令行入口
├── requirements.txt          # Python 依赖
├── runtime.txt               # 指定 Python 版本（Render 用）
├── render.yaml               # Render 一键部署配置
├── .gitignore
├── mailbox_project/          # 项目配置包（settings / urls / wsgi）
├── letters/                  # 我们的应用：模型、接口、路由
│   ├── models.py             # 信件的数据结构
│   ├── views.py              # 发信 / 收信 / 公开信 的接口
│   └── urls.py               # 网址路由
├── templates/
│   └── index.html            # 单页界面
└── static/
    ├── css/style.css         # 样式
    └── js/app.js             # 前端交互
```

---

## 一、本地运行（先看效果）

> 需要先安装 [Python 3.10+](https://www.python.org/downloads/)。

打开终端（推荐 Git Bash / PowerShell），进入本项目目录：

```bash
# 1. 创建虚拟环境（把依赖隔离，不污染系统）
python -m venv venv

# 2. 激活虚拟环境
#    Git Bash 用：   source venv/Scripts/activate
#    PowerShell 用： venv\Scripts\Activate.ps1
#    cmd 用：        venv\Scripts\activate.bat

# 3. 安装依赖
pip install -r requirements.txt

# 4. 生成数据库表
python manage.py migrate

# 5. 启动开发服务器
python manage.py runserver
```

浏览器打开 **http://127.0.0.1:8000** 就能使用了。

可选：创建一个后台账号，去 `http://127.0.0.1:8000/admin/` 查看 / 删除信件：

```bash
python manage.py createsuperuser
```

---

## 二、上传到 GitHub

```bash
# 在项目根目录执行
git init
git add .
git commit -m "初始提交：密信信箱（Django + 纯前端）"

# 在 github.com 新建一个仓库（不要勾选 README），然后关联并推送：
git branch -M main
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

---

## 三、部署上线（让别人也能实时访问）

最简单的方式是 **Render**（有免费额度，原生支持 Django + Python）。

### 方式 A：一键蓝图部署（推荐）

1. 把代码推到 GitHub（见上一步）。
2. 打开 [render.com](https://render.com)，用 GitHub 登录。
3. 点 **New** → **Blueprint** → 选择你的仓库。
4. Render 会自动读取本项目的 `render.yaml`，创建「Web 服务 + 免费 Postgres 数据库」。
5. 点 **Apply** 开始部署，等 1~2 分钟，会得到一个 `https://xxxx.onrender.com` 的网址——这就是别人能实时访问的站点。

### 方式 B：手动创建 Web Service

1. **New** → **Web Service** → 连接 GitHub 仓库。
2. 设置：
   - **Build Command**：`pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**：`gunicorn mailbox_project.wsgi:application`
3. 在 **Environment** 里添加变量：
   - `DEBUG` = `False`
   - `DJANGO_SECRET_KEY` = 任意一长串随机字符（可用密码生成器）
   - 再创建一个 **Postgres** 数据库，把它的 **Internal Database URL** 填到 `DATABASE_URL`
4. 部署完成后即可访问。

> 部署后第一次需要建表：在 Render 的 Shell 里执行 `python manage.py migrate`，或在 Build Command 里已经包含（如上配置已包含）。

---

## 四、关于数据持久化（重要）

- **本地**：用 SQLite（`db.sqlite3`），数据存在你电脑上，方便调试。
- **Render 免费版**：默认硬盘是临时的，部署/重启后 SQLite 数据会被清空。
  本项目已内置 `DATABASE_URL` 支持——只要按上面步骤配置了 Postgres 数据库，数据就会**永久保存**，不受重启影响。

---

## 五、想继续学习？可以试试

- 给「发信」加一层浏览器端加密（你之前的密码信箱思路），让服务器也读不到内容。
- 把每 5 秒轮询换成 **WebSocket（Django Channels）**，做到真正的毫秒级实时推送。
- 加一个「阅后即焚」：信件被读取一次后自动删除。
- 用 Django 后台给信件加审核，避免公开板出现垃圾内容。

祝你玩得开心，有问题随时问 🙂
