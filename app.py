import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# Page
# =========================
st.set_page_config(page_title="Thước Cân Bằng Học Tập", layout="wide")

st.title("Thước Cân Bằng Học Tập")
st.caption(
    "Dashboard prototype: thêm học sinh (ID/Lớp/Tên) → nhập điểm → phân nhóm → mức lệch → gợi ý. "
    "Công cụ chỉ hỗ trợ ra quyết định, không thay thế giáo viên."
)

# =========================
# Exercise library (for Lệch rõ)
# =========================
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

def pick_exercises(subject: str, n: int = 2):
    items = EXERCISES.get(subject, [])
    return items[:n] if len(items) >= n else items

# =========================
# Helpers
# =========================
def compute_scores(row):
    logic_avg = round((row["Toán"] + row["Khoa học"] + row["Tin"]) / 3, 2)
    lang_avg = round((row["Văn"] + row["Sử"] + row["Anh"]) / 3, 2)
    diff = round(abs(logic_avg - lang_avg), 2)

    if diff < 1:
        level = "Cân bằng tốt"
    elif diff < 2:
        level = "Lệch vừa"
    else:
        level = "Lệch rõ"

    return logic_avg, lang_avg, diff, level

def badge(level: str):
    if level == "Cân bằng tốt":
        st.success(level)
    elif level == "Lệch vừa":
        st.warning(level)
    else:
        st.error(level)

def student_label(s):
    return f'{s["ID"]} | {s["Lớp"]} | {s["Tên"]}'

def weakest_subjects(scores_dict, group: str, k: int = 2):
    if group == "Logic":
        subs = ["Toán", "Khoa học", "Tin"]
    else:
        subs = ["Văn", "Sử", "Anh"]
    scored = sorted([(s, scores_dict[s]) for s in subs], key=lambda x: x[1])  # thấp -> cao
    return [s for s, _ in scored[:k]]

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

# =========================
# Sidebar: add student form + select student
# =========================
st.sidebar.header("Thêm học sinh")

with st.sidebar.form("add_student_form", clear_on_submit=True):
    new_id = st.text_input("ID học sinh (duy nhất)", placeholder="VD: VS095605")
    new_class = st.text_input("Lớp", placeholder="VD: 8A5")
    new_name = st.text_input("Họ và tên", placeholder="VD: Trần Vũ Quốc Huy")
    submitted = st.form_submit_button("➕ Thêm học sinh")

if submitted:
    new_id = new_id.strip()
    new_class = new_class.strip()
    new_name = new_name.strip()

    if not new_id or not new_class or not new_name:
        st.sidebar.error("Vui lòng nhập đủ ID, Lớp, Họ và tên.")
    else:
        existing_ids = {s["ID"] for s in st.session_state.students}
        if new_id in existing_ids:
            st.sidebar.error("ID đã tồn tại. Hãy dùng ID khác.")
        else:
            st.session_state.students.append({
                "ID": new_id, "Lớp": new_class, "Tên": new_name,
                "Toán": 0.0, "Khoa học": 0.0, "Tin": 0.0,
                "Văn": 0.0, "Sử": 0.0, "Anh": 0.0
            })
            st.sidebar.success("Đã thêm học sinh! Chọn ở danh sách bên dưới.")
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("Chọn học sinh")

labels = [student_label(s) for s in st.session_state.students]
selected_label = st.sidebar.selectbox("Danh sách", labels)

current = next(s for s in st.session_state.students if student_label(s) == selected_label)

st.sidebar.markdown("---")
st.sidebar.caption("Mẹo quay demo: chọn học sinh mẫu A/B/C để thấy đủ 3 mức cân bằng.")

# =========================
# Main layout
# =========================
left, right = st.columns([1.15, 1])

with left:
    st.subheader("1) Thông tin học sinh")
    st.write(f"**ID:** {current['ID']}")
    st.write(f"**Lớp:** {current['Lớp']}")
    st.write(f"**Họ và tên:** {current['Tên']}")

    st.subheader("2) Nhập / chỉnh điểm (0–10)")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Nhóm Logic – STEM")
        math = st.number_input("Toán", 0.0, 10.0, float(current["Toán"]), 0.1)
        science = st.number_input("Khoa học", 0.0, 10.0, float(current["Khoa học"]), 0.1)
        it = st.number_input("Tin", 0.0, 10.0, float(current["Tin"]), 0.1)

    with c2:
        st.markdown("### Nhóm Ngôn ngữ – Xã hội")
        lit = st.number_input("Văn", 0.0, 10.0, float(current["Văn"]), 0.1)
        history = st.number_input("Sử", 0.0, 10.0, float(current["Sử"]), 0.1)
        english = st.number_input("Anh", 0.0, 10.0, float(current["Anh"]), 0.1)

    btn1, btn2, btn3 = st.columns(3)
    analyze = btn1.button("Phân tích", type="primary")
    save_scores = btn2.button("💾 Lưu điểm")
    reset_scores = btn3.button("↩️ Reset về điểm đã lưu")

    # current input row
    input_row = {
        "Toán": math, "Khoa học": science, "Tin": it,
        "Văn": lit, "Sử": history, "Anh": english
    }

    if save_scores:
        for s in st.session_state.students:
            if s["ID"] == current["ID"]:
                s.update(input_row)
                break
        st.success("Đã lưu điểm cho học sinh.")
        st.rerun()

    if reset_scores:
        st.rerun()

with right:
    st.subheader("3) Dashboard kết quả")

    logic_avg, lang_avg, diff, level = compute_scores({**current, **input_row})

    k1, k2, k3 = st.columns(3)
    k1.metric("TB Logic", logic_avg)
    k2.metric("TB Ngôn ngữ", lang_avg)
    k3.metric("Chênh lệch (Δ)", diff)

    st.write("Mức cân bằng:")
    badge(level)

    st.markdown("### Thước cân bằng")
    st.progress(min(diff / 3, 1.0))
    st.caption("Ngưỡng: Δ < 1 (tốt), 1 ≤ Δ < 2 (vừa), Δ ≥ 2 (rõ)")

    st.markdown("### Biểu đồ 2 nhóm")
    fig, ax = plt.subplots()
    ax.bar(["Logic–STEM", "Ngôn ngữ–Xã hội"], [logic_avg, lang_avg])
    ax.set_ylim(0, 10)
    ax.set_ylabel("Điểm TB (0–10)")
    st.pyplot(fig)

# =========================
# Recommendations
# =========================
st.markdown("---")
st.subheader("4) Gợi ý điều chỉnh (áp dụng 2–3 tuần)")

if level == "Cân bằng tốt":
    st.write("✅ **Mục tiêu:** Duy trì ổn định và phát triển đều.")
    st.write("- Duy trì nhịp học hiện tại.")
    st.write("- Tăng thử thách nhẹ ở môn mạnh.")
    st.write("- Theo dõi định kỳ để đảm bảo cân bằng được giữ ổn định.")

elif level == "Lệch vừa":
    st.write("⚠️ **Mục tiêu:** Giảm chênh lệch mà không làm mất động lực ở nhóm mạnh.")
    st.write("- Giữ thử thách ở nhóm mạnh.")
    st.write("- Tăng 15–20 phút/ngày cho nhóm yếu.")
    st.write("- Chia nội dung khó thành phần nhỏ để tránh quá tải.")

else:
    st.write("🛑 **Mục tiêu:** Ưu tiên cải thiện nhóm yếu trong 2 tuần để kéo Δ xuống mức 'lệch vừa'.")
    st.write("- Giữ mức vừa phải ở nhóm mạnh (không tăng thêm).")
    st.write("- Đánh giá lại sau mỗi 2 tuần.")

    # Determine weaker group
    weak_group = "Ngôn ngữ" if logic_avg > lang_avg else "Logic"
    st.markdown(f"### Nhóm yếu hiện tại: **{weak_group}**")

    scores_for_pick = {
        "Toán": math, "Khoa học": science, "Tin": it,
        "Văn": lit, "Sử": history, "Anh": english
    }
    weak2 = weakest_subjects(scores_for_pick, "Logic" if weak_group == "Logic" else "Ngôn ngữ", k=2)

    st.markdown("### Bài tập cụ thể cho 2 môn yếu nhất (15–20 phút/môn)")
    for subj in weak2:
        st.markdown(f"**{subj}**")
        for item in pick_exercises(subj, n=2):
            st.write(f"- {item}")

    st.markdown("### Kế hoạch 2 tuần (mẫu)")
    st.write("- Mỗi tuần 5 buổi (Thứ 2–Thứ 6).")
    st.write("- Mỗi buổi: 1 nhiệm vụ môn yếu #1 + 1 nhiệm vụ môn yếu #2.")
    st.write("- Cuối tuần: làm bài kiểm tra ngắn 20 phút cho 2 môn yếu và cập nhật lại điểm.")

st.caption("Lưu ý: Prototype minh chứng ý tưởng, không thay thế giáo viên/học sinh.")

# =========================
# Table view
# =========================
st.markdown("---")
st.subheader("5) Bảng tổng hợp nhiều học sinh")

df = pd.DataFrame(st.session_state.students)

computed = df.apply(
    lambda r: pd.Series(compute_scores(r), index=["TB Logic", "TB Ngôn ngữ", "Δ", "Mức"]),
    axis=1
)
df2 = pd.concat([df, computed], axis=1)
df2 = df2[["ID", "Lớp", "Tên", "Toán", "Khoa học", "Tin", "Văn", "Sử", "Anh", "TB Logic", "TB Ngôn ngữ", "Δ", "Mức"]]
df2 = df2.sort_values(by="Δ", ascending=False)

st.dataframe(df2, use_container_width=True)
st.caption("Sắp xếp theo Δ giảm dần để ưu tiên học sinh lệch rõ.")