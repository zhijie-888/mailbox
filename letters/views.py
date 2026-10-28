"""
视图（View）：处理网页请求、和数据库打交道、返回结果。

页面相关：
- index：返回我们的单页 HTML。

接口（给前端 JS 调用的 JSON 接口）：
- send_letter：发信（公开 / 指定收信人）
- get_inbox：按识别码取私信
- get_public：取所有公开信
"""
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Letter


# ===== 主页：渲染单页 HTML =====
def index(request):
    return render(request, "index.html")


# ===== 发信接口 =====
# 说明：这里用了 @csrf_exempt 关闭 CSRF 校验，因为本项目没有登录，
# 任何人都可发信，属于公开的演示接口。如果你以后加了登录，
# 应去掉这行，并在前端 fetch 时带上 CSRF Token（可参考 Django 官方文档）。
@csrf_exempt
def send_letter(request):
    if request.method != "POST":
        return JsonResponse({"error": "请使用 POST 请求发信"}, status=405)

    # 解析前端传来的 JSON 数据
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "数据格式错误"}, status=400)

    content = (data.get("content") or "").strip()
    if not content:
        return JsonResponse({"error": "信件内容不能为空"}, status=400)

    is_public = bool(data.get("is_public", False))

    if is_public:
        to_id = "public"  # 公开信统一用 "public" 作为收信人
    else:
        to_id = (data.get("to_id") or "").strip()
        if not to_id:
            return JsonResponse({"error": "请填写收信人识别码"}, status=400)
        if to_id.lower() == "public":
            return JsonResponse({"error": "识别码不能使用保留字 public"}, status=400)

    from_id = (data.get("from_id") or "").strip() or None

    letter = Letter.objects.create(
        to_id=to_id,
        from_id=from_id,
        content=content,
        is_public=is_public,
    )
    return JsonResponse({"ok": True, "id": letter.id, "message": "发送成功"})


# ===== 收信接口：GET /api/inbox/?to_id=你的识别码 =====
def get_inbox(request):
    to_id = request.GET.get("to_id", "").strip()
    if not to_id:
        return JsonResponse({"error": "请填写收信人识别码"}, status=400)

    # 只取“指定给这个识别码”的私信（is_public=False）
    letters = Letter.objects.filter(to_id=to_id, is_public=False)
    data = [
        {
            "id": l.id,
            "from_id": l.from_id or "匿名",
            "content": l.content,
            "created_at": l.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        for l in letters
    ]
    return JsonResponse({"count": len(data), "letters": data})


# ===== 公开信板接口：GET /api/public/ =====
def get_public(request):
    letters = Letter.objects.filter(is_public=True)
    data = [
        {
            "id": l.id,
            "from_id": l.from_id or "匿名",
            "content": l.content,
            "created_at": l.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        for l in letters
    ]
    return JsonResponse({"count": len(data), "letters": data})
