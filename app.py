# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


import streamlit as st
import json
import os
from datetime import date, timedelta
import plotly.express as px

st.set_page_config(
    page_title="Study Planner",
    page_icon="📚",
    layout="wide"
)

DATA_FILE = "data.json"


# ─── LOAD / SAVE ─────────────────────────────────────────────
def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "homework": [],
            "goals": [],
            "streak": {
                "count": 0,
                "last_active_date": None,
                "done_dates": []
            },
            "vacations": []
        }

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "streak" not in data:
        data["streak"] = {"count": 0, "last_active_date": None, "done_dates": []}
    if "vacations" not in data:
        data["vacations"] = []

    return data


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


data = load_data()


# ─── STREAK LOGIC ─────────────────────────────────────────────
def is_weekend(d):
    return d.weekday() >= 5


def is_vacation(d, vacations):
    for v in vacations:
        start = date.fromisoformat(v["start"])
        end = date.fromisoformat(v["end"])
        if start <= d <= end:
            return True
    return False


def is_school_day(d, vacations):
    return not is_weekend(d) and not is_vacation(d, vacations)


def get_prev_school_day(d, vacations):
    prev = d - timedelta(days=1)
    for _ in range(60):
        if is_school_day(prev, vacations):
            return prev
        prev -= timedelta(days=1)
    return prev


def recalc_streak(data):
    done_dates = set(data["streak"].get("done_dates", []))
    vacations = data.get("vacations", [])
    today = date.today()

    if not done_dates:
        return 0

    count = 0

    if str(today) not in done_dates:
        check = get_prev_school_day(today, vacations)
    else:
        check = today

    for _ in range(365):
        if not is_school_day(check, vacations):
            check -= timedelta(days=1)
            continue

        if str(check) in done_dates:
            count += 1
            check -= timedelta(days=1)
        else:
            break

    return count


def mark_hw_done_today(data):
    today_str = str(date.today())
    if today_str not in data["streak"]["done_dates"]:
        data["streak"]["done_dates"].append(today_str)

    data["streak"]["count"] = recalc_streak(data)
    data["streak"]["last_active_date"] = today_str


# ─── SIDEBAR ─────────────────────────────────────────────

# Заголовок Study Planner з більшим шрифтом
st.sidebar.markdown(
    "<div style='margin-top:20px; font-weight:bold; font-size:24px;'>📚 Study Planner</div>",
    unsafe_allow_html=True
)

# Лінія під заголовком
st.sidebar.markdown(
    "<hr style='margin-top:30px;margin-bottom:25px;'>",
    unsafe_allow_html=True
)

# Опускаємо Навігацію нижче та робимо текст більшим
st.sidebar.markdown(
    "<div style='margin-top:20px; font-weight:600; font-size:21px;'>🧭 Навігація</div>",
    unsafe_allow_html=True
)

# CSS для відстані між пунктами навігації
st.sidebar.markdown("""
<style>
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    margin-bottom: 21px !important;   /* відстань між пунктами */
}
</style>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    ["📅 План", "📊 Аналітика", "🏖️ Канікули", "ℹ️ Про проєкт"]
)

# Лінія під навігацією
st.sidebar.markdown(
    "<hr style='margin-top:15px;margin-bottom:10px;'>",
    unsafe_allow_html=True
)

# Відступ перед серією
st.sidebar.markdown(
    "<div style='margin-top:15px;'></div>",
    unsafe_allow_html=True
)

# Серія (залишаємо внизу)
st.sidebar.metric("🔥 Серія", f"{data['streak']['count']} дн.")

# ════════════════════════════════════════════════════════════
# 📅 ПЛАН
# ════════════════════════════════════════════════════════════
if page == "📅 План":

    st.title("📅 Навчальний план")
    st.markdown("---")

    with st.expander("➕ Додати завдання або ціль"):

        task_type = st.selectbox("Тип", ["Домашнє завдання", "Навчальна ціль"])
        title = st.text_input("Назва")

        if task_type == "Домашнє завдання":
            subject = st.text_input("Предмет")
            deadline = st.date_input("Дедлайн", min_value=date.today())
        else:
            deadline = st.date_input("Дедлайн", min_value=date.today())

        if st.button("Додати"):
            if title.strip() == "":
                st.error("Введи назву")
            else:
                if task_type == "Домашнє завдання":
                    data["homework"].append({
                        "id": f"{len(data['homework'])}",
                        "title": title,
                        "subject": subject,
                        "date": str(deadline),
                        "done": False
                    })
                else:
                    data["goals"].append({
                        "id": f"{len(data['goals'])}",
                        "title": title,
                        "date": str(deadline),
                        "done": False
                    })

                save_data(data)
                st.success("Додано ✅")
                st.rerun()

    st.markdown("---")

    if "hw_completed_today" not in st.session_state:
        st.session_state.hw_completed_today = False

    if "streak_dialog_shown" not in st.session_state:
        st.session_state.streak_dialog_shown = False

    col1, col2 = st.columns(2)

    # ─── HOMEWORK ─────────────────
    with col1:
        st.subheader("📘 Домашні завдання")

        if not data["homework"]:
            st.info("Немає домашніх завдань")

        for hw in data["homework"]:
            key = f"hw_{hw['id']}"

            checked = st.checkbox(
                f"{hw['subject']} — {hw['title']} (до {hw['date']})",
                value=hw.get("done", False),
                key=key
            )

            if checked and not hw.get("done", False):
                hw["done"] = True
                mark_hw_done_today(data)
                save_data(data)
                st.session_state.hw_completed_today = True
                st.rerun()

    # ─── GOALS ─────────────────
    with col2:
        st.subheader("🎯 Навчальні цілі")

        if not data["goals"]:
            st.info("Немає цілей")

        for goal in data["goals"]:
            key = f"goal_{goal['id']}"

            checked = st.checkbox(
                goal["title"],
                value=goal.get("done", False),
                key=key
            )

            if checked and not goal.get("done", False):
                goal["done"] = True
                save_data(data)
                st.rerun()

    save_data(data)

    st.markdown("---")

    col_s1, col_s2, col_s3 = st.columns(3)

    with col_s1:
        st.metric("🔥 Поточна серія", f"{data['streak']['count']} дн.")

    with col_s2:
        done_today = str(date.today()) in data["streak"].get("done_dates", [])
        st.metric("✅ Сьогодні виконано", "Так" if done_today else "Ні")

    with col_s3:
        st.metric("📅 Всього активних днів", len(data["streak"].get("done_dates", [])))



# ════════════════════════════════════════════════════════════
# 📊 АНАЛІТИКА
# ════════════════════════════════════════════════════════════
elif page == "📊 Аналітика":

    st.title("📊 Аналітика")
    st.markdown("---")

    done_dates = data["streak"].get("done_dates", [])
    today = date.today()

    days_30 = [(today - timedelta(days=i)) for i in range(29, -1, -1)]
    activity = []

    for d in days_30:
        if str(d) in done_dates:
            status = "Виконано"
        else:
            status = "Не виконано"

        activity.append({"Дата": str(d), "Статус": status})

    fig = px.bar(activity, x="Дата", y=[1]*30, color="Статус")
    fig.update_layout(yaxis=dict(showticklabels=False), height=250)

    st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════
# 🏖️ КАНІКУЛИ (мінімально)
# ════════════════════════════════════════════════════════════
elif page == "🏖️ Канікули":

    st.title("🏖️ Канікули")
    st.markdown("Функціонал можна розширити при потребі.")


# ════════════════════════════════════════════════════════════
# ℹ️ ПРО ПРОЄКТ
# ════════════════════════════════════════════════════════════
elif page == "ℹ️ Про проєкт":

    st.title("ℹ️ Про Study Planner")
    st.markdown("""
    Study Planner допомагає:
    - Додавати завдання
    - Ставити цілі
    - Відстежувати серію виконання
    - Аналізувати прогрес
    """)
