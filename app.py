import uuid
import unicodedata
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt


# =========================
# Page config
# =========================
st.set_page_config(
    page_title="Bảng Điều Khiển - Thước Cân Bằng",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================
# CSS
# =========================
CSS = """
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

section[data-testid="stSidebar"] { display: none !important; }
/* Tránh display:none quá mạnh vì đôi khi làm layout wrapper “lệch” */
div[data-testid="collapsedControl"] { visibility: hidden !important; width: 0 !important; height: 0 !important; }

[data-testid="stAppViewContainer"] { background:#f5f6f8; }
.block-container { padding-top: 1.1rem; padding-bottom: 6rem; } /* chừa chỗ cho chat nổi */
h1 { font-weight: 900; letter-spacing: -0.02em; }

/* LEFT NAV */
.leftNav {
  background: #0b0f19;
  color: #e5e7eb;
  border-radius: 14px;
  padding: 14px 12px;
  height: calc(100vh - 2.2rem);
  position: sticky;
  top: 1.1rem;
  overflow: auto;
  border: 1px solid rgba(255,255,255,0.06);
}
.leftNav .brand { font-weight: 900; font-size: 18px; margin-bottom: 12px; }
.leftNav .navItem {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  padding: 10px 10px;
  margin: 8px 0;
  font-weight: 800;
}
.leftNav .navItem.muted { background: transparent; border: 1px solid rgba(255,255,255,0.06); }
.leftNav small { opacity: 0.85; font-weight: 600; }

/* SUBJECT CARDS */
.course-card {
  border-radius: 12px;
  overflow: hidden;
  background: #fff;
  border: 1px solid rgba(17,24,39,0.10);
  box-shadow: 0 1px 0 rgba(17,24,39,0.04);
}
.course-top { height: 120px; position: relative; }
.course-dots {
  position:absolute;
  right: 10px; top: 10px;
  color: rgba(255,255,255,0.95);
  font-size: 22px;
  font-weight: 900;
}
.course-body { padding: 12px 14px 10px 14px; }
.course-slug { font-weight: 900; font-size: 16px; margin-bottom: 2px; text-transform: lowercase; }
.course-code { color:#6b7280; font-size: 13px; line-height: 1.25; }
.course-icons { margin-top: 10px; color:#6b7280; font-size: 16px; }
.course-icons span { margin-right: 14px; }

/* RIGHT PANEL */
.rightPanel {
  background: #ffffff;
  border: 1px solid rgba(17,24,39,0.10);
  border-radius: 14px;
  padding: 14px 14px;
  box-shadow: 0 1px 0 rgba(17,24,39,0.04);
  position: sticky;
  top: 1.1rem;
  max-height: calc(100vh - 2.2rem);
  overflow: auto;
}
.todo-title { font-size: 18px; font-weight: 900; margin: 0 0 10px 0; }
.todo-item {
  display: grid;
  grid-template-columns: 18px 1fr 14px;
  gap: 10px;
  padding: 10px 10px;
  border-radius: 12px;
  border: 1px solid rgba(17,24,39,0.08);
  background: #fafafa;
  margin-bottom: 10px;
}
.todo-item b { display:block; font-size: 13px; line-height: 1.25; }
.todo-item small { color:#6b7280; display:block; margin-top: 4px; }
.todo-x { color:#9ca3af; font-weight: 900; }

/* MID PANEL */
.midPanel {
  background: #ffffff;
  border: 1px solid rgba(17,24,39,0.10);
  border-radius: 14px;
  padding: 14px 14px;
  box-shadow: 0 1px 0 rgba(17,24,39,0.04);
  margin-top: 14px;
}

/* Hide widget labels */
label[data-testid="stWidgetLabel"] { display:none !important; }

/* CHATBOX UI */
.chat-shell {
  background: #fff;
  border: 1px solid rgba(17,24,39,0.12);
  border-radius: 16px;
  box-shadow: 0 18px 40px rgba(0,0,0,0.20);
  overflow: hidden;
}
.chat-head {
  background: #0b0f19;
  color: #e5e7eb;
  padding: 10px 12px;
  display:flex;
  justify-content: space-between;
  align-items:center;
  font-weight: 900;
}
.chat-hint { font-size: 12px; opacity: .9; font-weight: 800; }
.chat-body {
  background: #f8fafc;
  padding: 10px 10px;
  overflow-y: auto;
}
.bubble {
  background: #fff;
  border: 1px solid rgba(17,24,39,0.08);
  border-radius: 12px;
  padding: 8px 10px;
  margin: 8px 0;
}
.bubble.user { border-left: 4px solid #2563eb; }
.bubble.ai { border-left: 4px solid #10b981; }
.bname { font-weight: 900; margin-bottom: 2px; }

.chat-foot {
  background: #fff;
  border-top: 1px solid rgba(17,24,39,0.10);
  padding: 10px 10px;
}

/* Minimized pill */
.chat-pill {
  background: #2563eb;
  color: #fff;
  border-radius: 999px;
  padding: 10px 14px;
  display:flex;
  align-items:center;
  gap: 10px;
  box-shadow: 0 12px 28px rgba(0,0,0,0.18);
  border: 1px solid rgba(17,24,39,0.12);
  font-weight: 900;
}
.chat-pill .dot {
  width: 10px; height: 10px; border-radius: 999px;
  background: rgba(255,255,255,0.9);
}
.chat-pill .miniBtn button {
  height: 34px !important;
  border-radius: 999px !important;
  background: rgba(255,255,255,0.15) !important;
  color: #fff !important;
  border: 1px solid rgba(255,255,255,0.22) !important;
  font-weight: 900 !important;
  padding: 0 12px !important;
}
.chat-pill .miniBtn button:hover { filter: brightness(1.05); }

/* Responsive tweak */
@media (max-width: 520px) {
  .block-container { padding-bottom: 9rem; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# =========================
# Floating helper (không phụ thuộc streamlit-float)
# =========================
def st_float_container(key: str, css: str):
    anchor_id = f"float-anchor-{key}-{uuid.uuid4().hex}"
    st.markdown(f'<div id="{anchor_id}"></div>', unsafe_allow_html=True)

    components.html(
        f"""
        <script>
        (function() {{
          const run = () => {{
            const doc = window.parent.document;
            const anchor = doc.getElementById("{anchor_id}");
            if (!anchor) return;

            let target =
              anchor.closest('div[data-testid="stVerticalBlock"]') ||
              anchor.closest('div[data-testid="stHorizontalBlock"]');

            if (!target) {{
              let el = anchor;
              for (let i = 0; i < 60; i++) {{
                if (!el) break;
                const dt = el.getAttribute && el.getAttribute("data-testid");
                if (dt === "stVerticalBlock" || dt === "stHorizontalBlock") {{
                  target = el;
                  break;
                }}
                el = el.parentElement;
              }}
            }}

            if (!target) return;

            target.style.cssText += `{css}`;
            target.style.zIndex = "999999";
            target.style.pointerEvents = "auto";
            target.style.margin = "0";
          }};

          setTimeout(run, 50);
          setTimeout(run, 250);
        }})();
        </script>
        """,
        height=0,
        width=0,
    )


# =========================
# Data
# =========================
SUBJECT_CARDS = [
    {"name": "Toán",       "slug": "math",       "code": "THCS.GP-MATH-8", "year": "2025-2026", "color": "#1f77b4"},
    {"name": "Khoa học",   "slug": "science",    "code": "THCS.GP-SCI-8",  "year": "2025-2026", "color": "#8e44ad"},
    {"name": "Tin học",    "slug": "computer",   "code": "THCS.GP-IT-8",   "year": "2025-2026", "color": "#9a7421"},
    {"name": "Tiếng Anh",  "slug": "english",    "code": "THCS.GP-ENG-8",  "year": "2025-2026", "color": "#0f7a2b"},
    {"name": "Văn",        "slug": "literature", "code": "THCS.GP-VNS-8",  "year": "2025-2026", "color": "#ff5c00"},
    {"name": "Lịch Sử",    "slug": "history",    "code": "THCS.GP-HIS-8",  "year": "2025-2026", "color": "#2c3e50"},
]

EXERCISES = {
    "Văn": [
        "Đọc 1 đoạn 250–400 chữ, gạch chân 5 từ khóa và viết 3 câu tóm tắt.",
        "Viết 1 đoạn văn 120–150 chữ theo cấu trúc: Mở–Thân–Kết (1 ý chính).",
        "Làm 5 câu hỏi đọc hiểu (ý chính, chi tiết, suy luận, từ vựng, thông điệp).",
    ],
    "Anh": [
        "Ôn 15 từ vựng theo chủ đề + viết 5 câu dùng từ mới.",
        "Làm 10 câu ngữ pháp (thì/so sánh/mệnh đề quan hệ) + chữa lỗi.",
        "Nghe 3–5 phút (video ngắn) rồi ghi 5 ý chính bằng tiếng Anh.",
    ],
    "Sử": [
        "Vẽ timeline 6 mốc sự kiện của 1 bài học + 1 câu giải thích/mốc.",
        "Làm 8 câu trắc nghiệm + ghi lại 3 câu sai và lý do sai.",
        "Viết 5 flashcards: Sự kiện – Nguyên nhân – Kết quả.",
    ],
    "Toán": [
        "Làm 10 bài mức cơ bản theo 1 dạng + ghi 2 lỗi hay gặp.",
        "Làm 5 bài vận dụng nhẹ + viết 1 lời giải mẫu ngắn gọn.",
        "Chữa 3 bài sai gần nhất: ghi 'sai ở đâu – sửa thế nào'.",
    ],
    "Khoa học": [
        "Làm 8 câu hỏi khái niệm + 2 bài tính đơn giản (nếu có).",
        "Tóm tắt 1 trang kiến thức bằng sơ đồ (mindmap) ~10 nhánh.",
        "Quan sát/thí nghiệm mô phỏng đơn giản và viết 5 dòng kết luận.",
    ],
    "Tin": [
        "Làm 1 bài thuật toán cơ bản (điều kiện/vòng lặp) và thử 3 test case.",
        "Sửa 1 đoạn code lỗi (tự tạo hoặc bài cũ): ghi lỗi và cách sửa.",
        "Tạo 1 chương trình nhỏ 20–30 dòng (tính TB/ phân loại).",
    ],
}


# =========================
# Rules (NEW) ✅
# =========================
PASS_THRESHOLD = 6.5     # chỉ cần < 6.5 là phải improve
FOCUS_K = 3              # ưu tiên tối đa 3 môn thấp nhất
ALL_SUBJECTS = ["Toán", "Khoa học", "Tin", "Văn", "Sử", "Anh"]
DISPLAY_NAME = {"Anh": "Tiếng Anh", "Sử": "Lịch Sử"}


# =========================
# Helpers
# =========================
def normalize_text(text: str) -> str:
    t = (text or "").lower().strip()
    t = unicodedata.normalize("NFD", t)
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")  # remove accents
    t = "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in t)  # remove punctuation
    return " ".join(t.split())

def pick_exercises(subject: str, n: int = 2):
    items = EXERCISES.get(subject, [])
    return items[:n] if len(items) >= n else items

def compute_scores(row):
    math = float(row.get("Toán", 0))
    sci  = float(row.get("Khoa học", 0))
    it   = float(row.get("Tin", 0))
    lit  = float(row.get("Văn", 0))
    hist = float(row.get("Sử", 0))
    eng  = float(row.get("Anh", 0))

    logic_avg = round((math + sci + it) / 3, 2)
    lang_avg = round((lit + hist + eng) / 3, 2)
    diff = round(abs(logic_avg - lang_avg), 2)

    if diff < 1:
        level = "Cân bằng tốt"
    elif diff < 2:
        level = "Lệch vừa"
    else:
        level = "Lệch rõ"
    return logic_avg, lang_avg, diff, level

def student_label(s):
    return f'{s["ID"]} | {s["Lớp"]} | {s["Tên"]}'

def weakest_subjects(scores_dict, group: str, k: int = 2):
    subs = ["Toán", "Khoa học", "Tin"] if group == "Logic" else ["Văn", "Sử", "Anh"]
    scored = sorted([(s, scores_dict[s]) for s in subs], key=lambda x: x[1])
    return [s for s, _ in scored[:k]]

def get_low_subjects(scores: dict, threshold: float = PASS_THRESHOLD):
    low = []
    for s in ALL_SUBJECTS:
        v = float(scores.get(s, 0))
        if v < threshold:
            low.append((s, v))
    low.sort(key=lambda x: x[1])
    return low

def hk2_revision_plan(n_each: int = 3) -> str:
    out = []
    out.append("📚 ÔN TẬP HỌC KỲ 2 - BÀI TẬP GỢI Ý (TẤT CẢ CÁC MÔN)")
    out.append(f"(Mỗi môn {n_each} bài)")
    out.append("")
    for subj in ALL_SUBJECTS:
        disp = DISPLAY_NAME.get(subj, subj)
        out.append(f"{disp}:")
        items = EXERCISES.get(subj, [])
        if not items:
            out.append("• (Chưa có bài tập gợi ý)")
        else:
            for item in items[:n_each]:
                out.append(f"• {item}")
        out.append("")
    out.append("Gợi ý lịch ôn (mẫu 2 tuần):")
    out.append("• T2: Toán + Văn")
    out.append("• T3: Khoa học + Tiếng Anh")
    out.append("• T4: Tin + Lịch Sử")
    out.append("• T5: Toán + Tiếng Anh")
    out.append("• T6: Văn + Khoa học")
    out.append("• Cuối tuần: làm 1 mini-test + chữa lỗi + tổng kết")
    return "\n".join(out)

def full_recommendation(current, input_row) -> str:
    logic_avg, lang_avg, diff, level = compute_scores({**current, **input_row})

    scores_for_pick = {
        "Toán": float(input_row["Toán"]),
        "Khoa học": float(input_row["Khoa học"]),
        "Tin": float(input_row["Tin"]),
        "Văn": float(input_row["Văn"]),
        "Sử": float(input_row["Sử"]),
        "Anh": float(input_row["Anh"]),
    }
    low = get_low_subjects(scores_for_pick, threshold=PASS_THRESHOLD)

    out = []
    out.append(f"Kết quả: TB Logic={logic_avg} | TB Ngôn ngữ={lang_avg} | Δ={diff}")
    out.append(f"Cân bằng nhóm: {level}")
    out.append("")

    # ✅ RULE MỚI: có môn dưới 6.5 => luôn ưu tiên improve
    if low:
        out.append(f"🛑 CẢNH BÁO: Có {len(low)} môn dưới {PASS_THRESHOLD} → cần ưu tiên cải thiện.")
        focus = low[:min(FOCUS_K, len(low))]
        out.append("")
        out.append("Môn ưu tiên (thấp nhất trước):")
        out.append("• " + ", ".join([f"{DISPLAY_NAME.get(s, s)} ({v})" for s, v in focus]))

        if len(low) > len(focus):
            rest = ", ".join([f"{DISPLAY_NAME.get(s, s)} ({v})" for s, v in low[len(focus):]])
            out.append(f"• Các môn dưới ngưỡng khác: {rest}")

        out.append("")
        out.append("Bài tập gợi ý (mỗi môn 2 task):")
        for subj, _v in focus:
            disp = DISPLAY_NAME.get(subj, subj)
            out.append(f"{disp}:")
            for item in pick_exercises(subj, n=2):
                out.append(f"• {item}")

        out.append("")
        out.append("Kế hoạch 2 tuần (mẫu):")
        out.append("• 5 buổi/tuần (T2–T6).")
        if len(focus) >= 2:
            out.append(f"• Mỗi buổi: 20 phút {DISPLAY_NAME.get(focus[0][0], focus[0][0])} + 20 phút {DISPLAY_NAME.get(focus[1][0], focus[1][0])}.")
        else:
            out.append(f"• Mỗi buổi: 30–40 phút {DISPLAY_NAME.get(focus[0][0], focus[0][0])}.")
        out.append("• Cuối tuần: mini test 20 phút + cập nhật điểm → hỏi lại assistant.")
        return "\n".join(out)

    # Không có môn dưới 6.5 => áp logic cũ theo Δ
    if level == "Cân bằng tốt":
        out += [
            "✅ Gợi ý (2–3 tuần):",
            "• Duy trì nhịp học hiện tại.",
            "• Tăng thử thách nhẹ ở môn mạnh (mỗi tuần 1 nhiệm vụ khó hơn).",
            "• Theo dõi lại sau 2 tuần.",
        ]
        return "\n".join(out)

    if level == "Lệch vừa":
        out += [
            "⚠️ Gợi ý (2–3 tuần):",
            "• Giữ thử thách ở nhóm mạnh.",
            "• Tăng 15–20 phút/ngày cho nhóm yếu.",
            "• Chia nội dung khó thành phần nhỏ (2–3 phần/buổi).",
            "• Theo dõi lại sau 2 tuần.",
        ]
        return "\n".join(out)

    weak_group = "Ngôn ngữ" if logic_avg > lang_avg else "Logic"
    out += [
        "🛑 Gợi ý ưu tiên (Lệch rõ):",
        f"• Nhóm yếu hiện tại: {weak_group}",
        "• Trong 2 tuần: ưu tiên kéo Δ xuống mức 'Lệch vừa'.",
        "• Nhóm mạnh: giữ mức vừa phải (không tăng thêm).",
        "",
    ]

    weak2 = weakest_subjects(scores_for_pick, "Logic" if weak_group == "Logic" else "Ngôn ngữ", k=2)
    out.append("2 môn yếu nhất & bài tập gợi ý:")
    for subj in weak2:
        disp = DISPLAY_NAME.get(subj, subj)
        out.append(f"{disp}:")
        for item in pick_exercises(subj, n=2):
            out.append(f"• {item}")

    out += [
        "",
        "Kế hoạch 2 tuần (mẫu):",
        "• 5 buổi/tuần (T2–T6).",
        f"• Mỗi buổi: 15–20 phút {DISPLAY_NAME.get(weak2[0], weak2[0])} + 15–20 phút {DISPLAY_NAME.get(weak2[1], weak2[1])}.",
        "• Cuối tuần: kiểm tra nhanh 20 phút + cập nhật điểm → hỏi lại assistant.",
    ]
    return "\n".join(out)

def html_safe(text: str) -> str:
    if text is None:
        return ""
    text = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return text.replace("\n", "<br>")

def ai_chat_answer(user_text: str, current, input_row) -> str:
    tn = normalize_text(user_text)

    # hello
    if tn in ["hi", "hello", "hey", "xin chao", "chao", "alo", "yo", "hiii", "helo"]:
        return (
            "Chào bạn 👋\n\n"
            "Bạn thử hỏi:\n"
            "• Mình đang yếu môn nào?\n"
            "• Cho recommendation giúp mình\n"
            "• Kế hoạch 2 tuần\n"
            "• Tôi cần ôn các bài tập gì?"
        )

    # ✅ NEW: ôn tập tất cả môn HK2
    if (
        "toi can on cac bai tap gi" in tn
        or "toi can on bai tap gi" in tn
        or "on cac bai tap gi" in tn
        or ("on" in tn and "bai tap" in tn and ("hoc ky 2" in tn or "hoc ki 2" in tn or "hk2" in tn))
    ):
        return hk2_revision_plan(n_each=3)

    # recommendation theo điểm
    trigger = any(k in tn for k in [
        "yeu", "mon nao", "mon yeu", "yeu mon", "diem thap", "lech", "can bang",
        "goi y", "recommend", "recommendation", "tom tat", "tong hop", "ke hoach",
        "improve", "cai thien", "duoi", "thap"
    ])
    if trigger:
        return full_recommendation(current, input_row)

    return (
        "Bạn hỏi thử kiểu:\n"
        "• Mình đang yếu môn nào?\n"
        "• Cho recommendation giúp mình\n"
        "• Kế hoạch 2 tuần\n"
        "• Tôi cần ôn các bài tập gì?"
    )


# =========================
# Session state init
# =========================
if "students" not in st.session_state:
    st.session_state.students = [
        {"ID": "A01", "Lớp": "8A", "Tên": "Học sinh A",
         "Toán": 9.0, "Khoa học": 8.0, "Tin": 7.5, "Văn": 5.5, "Sử": 7.0, "Anh": 6.0},
        {"ID": "B02", "Lớp": "8A", "Tên": "Học sinh B",
         "Toán": 7.5, "Khoa học": 7.2, "Tin": 7.0, "Văn": 7.0, "Sử": 6.8, "Anh": 7.1},
        {"ID": "C03", "Lớp": "8B", "Tên": "Học sinh C",
         "Toán": 9.5, "Khoa học": 9.0, "Tin": 9.0, "Văn": 5.0, "Sử": 5.5, "Anh": 5.0},
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Xin chào! Bạn hỏi “mình đang yếu môn nào?” hoặc “Tôi cần ôn các bài tập gì?” là mình gợi ý luôn."}
    ]

if "ai_question" not in st.session_state:
    st.session_state.ai_question = ""

if "current_student" not in st.session_state:
    st.session_state.current_student = None
if "current_input_row" not in st.session_state:
    st.session_state.current_input_row = None

if "chat_minimized" not in st.session_state:
    st.session_state.chat_minimized = False

if "chat_autoscroll" not in st.session_state:
    st.session_state.chat_autoscroll = True

if "chat_body_id" not in st.session_state:
    st.session_state.chat_body_id = f"chat-body-{uuid.uuid4().hex}"


def send_ai_message():
    q = st.session_state.get("ai_question", "").strip()
    if not q:
        return
    cur = st.session_state.get("current_student")
    row = st.session_state.get("current_input_row")
    if cur is None or row is None:
        return
    st.session_state.chat_history.append({"role": "user", "content": q})
    st.session_state.chat_history.append({"role": "assistant", "content": ai_chat_answer(q, cur, row)})
    st.session_state.ai_question = ""
    st.session_state.chat_autoscroll = True
    st.session_state.chat_minimized = False


def clear_ai_chat():
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Chat đã xoá. Bạn hỏi “mình đang yếu môn nào?” hoặc “Tôi cần ôn các bài tập gì?” là mình trả lời luôn."}
    ]
    st.session_state.ai_question = ""
    st.session_state.chat_autoscroll = True


def toggle_minimize():
    st.session_state.chat_minimized = not st.session_state.chat_minimized


# =========================
# Main layout
# =========================
left_col, mid_col, right_col = st.columns([0.70, 3.10, 1.40])

# LEFT NAV
with left_col:
    st.markdown(
        """
        <div class="leftNav">
          <div class="brand">VINSCHOOL</div>
          <div class="navItem">👤 Tài Khoản<br><small>Account</small></div>
          <div class="navItem muted">📊 Bảng Điều Khiển<br><small>Dashboard</small></div>
          <div class="navItem">📚 Khóa Học<br><small>Courses</small></div>
          <div class="navItem">👥 Các nhóm<br><small>Groups</small></div>
          <div class="navItem">📅 Lịch<br><small>Calendar</small></div>
          <div class="navItem">📥 Hộp thư đến<br><small>Inbox</small></div>
          <div class="navItem">🕘 Lịch sử<br><small>History</small></div>
          <div style="margin-top:14px; opacity:0.75; font-size:12px;">Replica UI để demo</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# MIDDLE
with mid_col:
    st.markdown("# Bảng Điều Khiển")

    r1 = st.columns(3)
    r2 = st.columns(3)
    for i, subj in enumerate(SUBJECT_CARDS):
        target = r1[i] if i < 3 else r2[i - 3]
        with target:
            st.markdown(
                f"""
                <div class="course-card">
                  <div class="course-top" style="background:{subj["color"]};">
                    <div class="course-dots">⋮</div>
                  </div>
                  <div class="course-body">
                    <div class="course-slug">{subj["slug"]}</div>
                    <div class="course-code">{subj["name"]}<br>{subj["code"]}<br>{subj["year"]}</div>
                    <div class="course-icons"><span>📝</span><span>💬</span><span>📁</span></div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Balance tool under cards
    st.markdown('<div class="midPanel">', unsafe_allow_html=True)
    st.markdown("## Thước Cân Bằng Học Tập")
    st.caption(f"Rule: Nếu có bất kỳ môn nào < {PASS_THRESHOLD} → báo cần cải thiện + gợi ý bài tập.")

    labels = [student_label(s) for s in st.session_state.students]
    selected = st.selectbox("Chọn học sinh", labels, key="selected_student")
    current = next(s for s in st.session_state.students if student_label(s) == selected)

    # load student scores into widget keys when switching student
    if st.session_state.get("loaded_student_id") != current["ID"]:
        st.session_state.loaded_student_id = current["ID"]
        st.session_state.score_math = float(current["Toán"])
        st.session_state.score_science = float(current["Khoa học"])
        st.session_state.score_it = float(current["Tin"])
        st.session_state.score_lit = float(current["Văn"])
        st.session_state.score_history = float(current["Sử"])
        st.session_state.score_english = float(current["Anh"])

    colA, colB = st.columns(2)
    with colA:
        st.markdown("**Logic – STEM**")
        math = st.number_input("Toán", 0.0, 10.0, step=0.1, key="score_math")
        sci = st.number_input("Khoa học", 0.0, 10.0, step=0.1, key="score_science")
        it = st.number_input("Tin", 0.0, 10.0, step=0.1, key="score_it")
    with colB:
        st.markdown("**Ngôn ngữ – Xã hội**")
        lit = st.number_input("Văn", 0.0, 10.0, step=0.1, key="score_lit")
        hist = st.number_input("Sử", 0.0, 10.0, step=0.1, key="score_history")
        eng = st.number_input("Anh", 0.0, 10.0, step=0.1, key="score_english")

    input_row = {"Toán": math, "Khoa học": sci, "Tin": it, "Văn": lit, "Sử": hist, "Anh": eng}
    st.session_state.current_student = current
    st.session_state.current_input_row = input_row

    logic_avg, lang_avg, diff, level = compute_scores({**current, **input_row})

    low_ui = get_low_subjects(input_row, threshold=PASS_THRESHOLD)

    k1, k2, k3 = st.columns(3)
    k1.metric("TB Logic", logic_avg)
    k2.metric("TB Ngôn ngữ", lang_avg)
    k3.metric("Δ", diff)

    if low_ui:
        preview = ", ".join([f"{DISPLAY_NAME.get(s, s)}({v})" for s, v in low_ui[:3]]) + ("..." if len(low_ui) > 3 else "")
        st.error(f"Cần cải thiện: Có {len(low_ui)} môn dưới {PASS_THRESHOLD}: {preview}")
    else:
        if level == "Cân bằng tốt":
            st.success(level)
        elif level == "Lệch vừa":
            st.warning(level)
        else:
            st.error(level)

    st.progress(min(diff / 3, 1.0))
    st.caption("Ngưỡng cân bằng theo Δ: Δ < 1 (tốt), 1 ≤ Δ < 2 (vừa), Δ ≥ 2 (rõ)")

    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.bar(["Logic", "Ngôn ngữ"], [logic_avg, lang_avg])
    ax.set_ylim(0, 10)
    ax.set_ylabel("Điểm TB")
    st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT: Todo
with right_col:
    st.markdown('<div class="rightPanel">', unsafe_allow_html=True)
    st.markdown('<div class="todo-title">Cần làm</div>', unsafe_allow_html=True)

    def todo(icon, title, course, due, points=None):
        pts = f"<small><b>{points} điểm</b></small><br>" if points is not None else ""
        st.markdown(
            f"""
            <div class="todo-item">
              <div>{icon}</div>
              <div>
                <b>{title}</b>
                <small>{course}</small>
                {pts}
                <small>{due}</small>
              </div>
              <div class="todo-x">×</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    todo("💬", "4. Hướng dẫn về nhà tuần 22", "geography", "ThO2 13 tại 11:59")
    todo("📝", "4. NỘP BÀI THI GIỮA KÌ 2 TẠI ĐÂY - DEADLINE 13/2/2026", "geography", "ThO2 13 tại 23:59", points=10)
    todo("📌", "4. Quiz củng cố trước tiết học tuần 26 CÓ LẤY ĐIỂM KIỂM TRA 15 PHÚT LẦN 2 HK2", "geography", "ThO2 16 tại 23:59", points=10)
    todo("💬", "2. Thảo luận trước tiết học tuần 26 - BẮT BUỘC LÀM - CÔ CHECK BÀI TRÊN LỚP", "geography", "ThO3 13 tại 23:59")
    todo("📌", "3. Quiz củng cố bài học tuần 26 + 27", "geography", "ThO3 20 tại 11:59", points=10)

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# FLOATING AI CHAT (BOTTOM-RIGHT + MINIMIZE) ✅
# =========================
chat_container = st.container()

with chat_container:
    st_float_container(
        key="ai-chat",
        css="""
          position: fixed !important;
          right: 20px !important;
          bottom: 20px !important;
          width: min(380px, 95vw) !important;
          max-height: 85vh !important;
        """
    )

    if st.session_state.chat_minimized:
        pill_cols = st.columns([3, 1])
        with pill_cols[0]:
            st.markdown(
                """
                <div class="chat-pill">
                  <div class="dot"></div>
                  <div>AI Assistant</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with pill_cols[1]:
            st.markdown('<div class="miniBtn">', unsafe_allow_html=True)
            st.button("Mở", on_click=toggle_minimize, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        bubbles = []
        for msg in st.session_state.chat_history:
            role = msg.get("role", "assistant")
            content = html_safe(msg.get("content", ""))
            if role == "user":
                bubbles.append(f'<div class="bubble user"><div class="bname">Bạn</div>{content}</div>')
            else:
                bubbles.append(f'<div class="bubble ai"><div class="bname">AI</div>{content}</div>')

        st.markdown(
            f"""
            <div class="chat-shell" style="display:flex; flex-direction:column; height:min(520px, 80vh);">
              <div class="chat-head">
                <div>AI Assistant</div>
                <div class="chat-hint">Gõ: “Tôi cần ôn các bài tập gì?”</div>
              </div>

              <div class="chat-body" id="{st.session_state.chat_body_id}" style="flex:1; overflow-y:auto;">
                {''.join(bubbles)}
              </div>

              <div class="chat-foot">
            """,
            unsafe_allow_html=True
        )

        st.text_input(
            "AI",
            key="ai_question",
            placeholder="Nhập câu hỏi…",
            label_visibility="collapsed",
        )

        a, b, c = st.columns([1, 1, 1])
        with a:
            st.button("Gửi", on_click=send_ai_message, use_container_width=True)
        with b:
            st.button("Xoá", on_click=clear_ai_chat, use_container_width=True)
        with c:
            st.button("Thu nhỏ", on_click=toggle_minimize, use_container_width=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        if st.session_state.chat_autoscroll:
            components.html(
                f"""
                <script>
                  (function(){{
                    const el = window.parent.document.getElementById("{st.session_state.chat_body_id}");
                    if (el) el.scrollTop = el.scrollHeight;
                  }})();
                </script>
                """,
                height=0,
                width=0,
            )
            st.session_state.chat_autoscroll = False
