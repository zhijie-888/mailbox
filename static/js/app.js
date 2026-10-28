/* ============================================================
   密信 Mailbox — 前端交互逻辑（纯原生 JS，无框架，方便学习）
   主要做三件事：
   1) 切换“写信 / 收信 / 公开信板”三个面板
   2) 调用后端 JSON 接口发送 / 读取信件
   3) 每 5 秒自动刷新，让新信件“即时”出现（类实时效果）
   ============================================================ */

// 后端接口地址（对应 letters/urls.py 里配置的路由）
const API = {
  send: "/api/send/",
  inbox: "/api/inbox/",
  public: "/api/public/",
};

/* ---------- 1. 标签切换 ---------- */
document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => showTab(btn.dataset.tab));
});

function showTab(tab) {
  // 高亮当前标签
  document.querySelectorAll(".tab-btn").forEach((b) =>
    b.classList.toggle("active", b.dataset.tab === tab)
  );
  // 显示对应面板
  document.querySelectorAll(".panel").forEach((p) =>
    p.classList.toggle("active", p.id === "panel-" + tab)
  );
  // 切到公开板时立即刷新一次
  if (tab === "public") loadPublic();
}

/* ---------- 2. 轻提示 toast ---------- */
let toastTimer = null;
function toast(msg, type = "info") {
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.className = "toast show" + (type === "error" ? " error" : "");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (el.className = "toast"), 2600);
}

/* ---------- 3. 写信：公开/指定 切换 ---------- */
document.querySelectorAll('input[name="scope"]').forEach((r) => {
  r.addEventListener("change", () => {
    const isPublic = r.value === "public";
    // 选了公开就隐藏“收信人识别码”输入框
    document.getElementById("toIdField").style.display = isPublic ? "none" : "block";
  });
});

/* 字数统计 */
const contentEl = document.getElementById("content");
const charCount = document.getElementById("charCount");
contentEl.addEventListener("input", () => {
  charCount.textContent = contentEl.value.length;
});

/* ---------- 4. 发送信件 ---------- */
document.getElementById("sendBtn").addEventListener("click", sendLetter);

async function sendLetter() {
  const scope = document.querySelector('input[name="scope"]:checked').value;
  const isPublic = scope === "public";
  const toId = document.getElementById("toId").value.trim();
  const fromId = document.getElementById("fromId").value.trim();
  const content = contentEl.value.trim();

  if (!content) {
    toast("请先写点内容～", "error");
    return;
  }
  if (!isPublic && !toId) {
    toast("请填写收信人识别码", "error");
    return;
  }

  // 把数据打包成 JSON 发给后端
  const payload = { content, from_id: fromId, is_public: isPublic };
  if (!isPublic) payload.to_id = toId;

  try {
    const res = await fetch(API.send, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "发送失败");

    toast("✅ 发送成功！");
    // 清空输入框
    contentEl.value = "";
    charCount.textContent = "0";
    // 如果当前在公开板，顺手刷新一下
    if (document.getElementById("panel-public").classList.contains("active")) {
      loadPublic();
    }
  } catch (err) {
    toast(err.message, "error");
  }
}

/* ---------- 5. 读取收件箱 ---------- */
document.getElementById("loadInboxBtn").addEventListener("click", loadInbox);

async function loadInbox() {
  const myId = document.getElementById("myId").value.trim();
  const list = document.getElementById("inboxList");
  if (!myId) {
    toast("请先输入你的识别码", "error");
    return;
  }
  try {
    const res = await fetch(API.inbox + "?to_id=" + encodeURIComponent(myId));
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "读取失败");
    renderLetters(list, data.letters, "还没有人给你写信呢～");
  } catch (err) {
    toast(err.message, "error");
  }
}

/* ---------- 6. 读取公开信板 ---------- */
async function loadPublic() {
  const list = document.getElementById("publicList");
  try {
    const res = await fetch(API.public);
    const data = await res.json();
    renderLetters(list, data.letters, "还没有公开信。去“写信”里发一封公开信吧。");
  } catch (err) {
    // 公开板出错不弹 toast，避免刷屏
    console.error(err);
  }
}

/* ---------- 7. 把信件数组渲染成 HTML ---------- */
function renderLetters(container, letters, emptyText) {
  if (!letters || letters.length === 0) {
    container.innerHTML = '<div class="empty">' + emptyText + "</div>";
    return;
  }
  container.innerHTML = letters
    .map(
      (l) => `
      <div class="letter">
        <div class="meta">
          <span class="who">${escapeHtml(l.from_id)}</span>
          <span class="when">${l.created_at}</span>
        </div>
        <div class="body">${escapeHtml(l.content)}</div>
      </div>`
    )
    .join("");
}

/* 防止内容里的特殊字符破坏页面（安全：HTML 转义） */
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

/* ---------- 8. 自动刷新（类“实时”） ---------- */
setInterval(() => {
  // 公开板一直刷新
  if (document.getElementById("panel-public").classList.contains("active")) {
    loadPublic();
  }
  // 收信面板：如果已经输入过识别码，也持续刷新
  const myId = document.getElementById("myId").value.trim();
  if (
    document.getElementById("panel-receive").classList.contains("active") &&
    myId
  ) {
    loadInbox();
  }
}, 5000);

/* ---------- 9. 页面加载时先拉一次公开信 ---------- */
loadPublic();
