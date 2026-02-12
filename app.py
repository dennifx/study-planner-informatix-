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

# ─── ОНОВЛЕННЯ СЕРІЇ 🔥 ─────────────────────────────
def update_streak(data):
    """
    Перераховує серію днів, враховуючи всі виконані завдання (homework + goals)
    і пропускає вихідні та канікули.
    """
    # Збираємо всі дати виконання завдань
    done_dates_set = set()
    for hw in data["homework"]:
        if hw.get("done", False):
            done_dates_set.add(hw["date"])
    for g in data["goals"]:
        if g.get("done", False):
            done_dates_set.add(g["date"])

    data["streak"]["done_dates"] = sorted(list(done_dates_set))

    vacations = data.get("vacations", [])
    today = date.today()
    count = 0
    check = today

    # Рахуємо серію від сьогодні назад
    for _ in range(365):
        if not is_school_day(check, vacations):
            check -= timedelta(days=1)
            continue

        if str(check) in done_dates_set:
            count += 1
            check -= timedelta(days=1)
        else:
            break

    data["streak"]["count"] = count
    data["streak"]["last_active_date"] = str(today)


# ─── ABOUT PROJECT DIALOG ─────────────────────────────────────
@st.dialog("ℹ️ Про Study Planner")
def about_project_dialog():
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("🎯 Мета програми")
    st.markdown(
        "<div style='background-color:#E8F5E9; padding:20px; border-radius:10px; font-size:16px; color:black; margin-bottom:15px;'>"
        "📌 Головна мета Study Planner — допомогти учням ефективно організовувати навчальний процес, "
        "стежити за завданнями та прогресом, не перевантажуючи себе зайвою інформацією."
        "</div>",
        unsafe_allow_html=True
    )

    st.subheader("✨ Фішки застосунку")
    st.markdown(
        "<div style='background-color:#F3E5F5; padding:20px; border-radius:10px; font-size:16px; color:black; margin-bottom:15px;'>"
        "🌟 Просте відмічання виконаних завдань<br>"
        "🌟 Візуальна серія днів виконання<br>"
        "🌟 Лаконічна навігація по плану, аналітиці та канікулах<br>"
        "🌟 Легкий перегляд прогресу та цілей"
        "</div>",
        unsafe_allow_html=True
    )

    st.subheader("🚀 Що класного в Study Planner")
    st.markdown(
        "<div style='background-color:#FFF3E0; padding:20px; border-radius:10px; font-size:16px; color:black; margin-bottom:15px;'>"
        "✨ Можливість швидко перевіряти виконані завдання<br>"
        "✨ Легка інтеграція власних цілей та нотаток<br>"
        "✨ Гарний простий дизайн, який не перевантажує очі<br>"
        "✨ Можна планувати свій день та бачити прогрес в реальному часі<br>"
        "✨ Надихає на регулярність та дисципліну, без стресу"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✅ Закрити", use_container_width=True, type="primary"):
        st.rerun()


# ─── SIDEBAR ─────────────────────────────────────────────
st.sidebar.markdown(
    "<div style='margin-top:20px; font-weight:bold; font-size:24px;'>📚 Study Planner</div>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<hr style='margin-top:30px;margin-bottom:25px;'>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<div style='margin-top:20px; font-weight:600; font-size:21px;'>🧭 Навігація</div>",
    unsafe_allow_html=True
)

st.sidebar.markdown("""<style>
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    margin-bottom: 21px !important;
}
</style>""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    ["🏠 Головна", "📅 План", "📊 Аналітика", "🏖️ Канікули"]
)

st.sidebar.markdown(
    "<hr style='margin-top:15px;margin-bottom:10px;'>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<div style='margin-top:15px;'></div>",
    unsafe_allow_html=True
)

st.sidebar.metric("🔥 Серія", f"{data['streak']['count']} дн.")

# ─── КНОПКА ПРО ПРОЄКТ ВНИЗУ ─────────────────────────────
# Додаємо вертикальний простір перед кнопкою в сайдбарі
st.sidebar.markdown("<div style='height:500px;'></div>", unsafe_allow_html=True)


if st.sidebar.button("❓ Про проєкт", use_container_width=True, type="secondary"):
    about_project_dialog()

# ════════════════════════════════════════════════════════════
# 🏠 ГОЛОВНА
# ════════════════════════════════════════════════════════════
if page == "🏠 Головна":

    today = date.today()
    user_name = "Ім'я"  # можеш зробити динамічним

    # ─── ПРИВІТАННЯ ─────────────────────────────
    st.markdown(
        f"<h1 style='color:#FFFFFF;'>Привіт, {user_name}! 👋</h1>"
        f"<p style='color:#BBBBBB; font-size:16px;'>Сьогодні: {today.strftime('%A, %d %B %Y')}</p>",
        unsafe_allow_html=True
    )

    # горизонтальна лінія
    st.markdown(
        "<hr style='border:1px solid #2A2F3A; margin-top:10px; margin-bottom:25px'>",
        unsafe_allow_html=True
    )

    # ─── ДВОКОЛОНКОВИЙ МАКЕТ ─────────────────────────────
    col_left, col_right = st.columns([2, 1], gap="large")

    done_dates_set = set(data["streak"].get("done_dates", []))

    # ═══════════════════════════════════════
    # ЛІВА КОЛОНКА
    # ═══════════════════════════════════════
    with col_left:

        # ─── Прогрес за тиждень ─────────────────────
        st.subheader("📈 Прогрес за тиждень")

        # День тижня з понеділка (0 = Пн, 6 = Нд)
        weekdays_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        # Підсвічування виконаних днів (якщо використовується data["streak"])
        done_dates_set = set(data["streak"].get("done_dates", []))

        # Формуємо список для поточного тижня
        today_weekday = today.weekday()  # 0 = Пн, 6 = Нд
        week_start = today - timedelta(days=today_weekday)  # Понеділок цього тижня
        week_days = [week_start + timedelta(days=i) for i in range(7)]

        cols = st.columns(7)
        for i, d in enumerate(week_days):
            day_short = weekdays_order[i]
            # якщо день сьогодні, зелений; якщо виконаний раніше, темно-зелений; якщо ні — темно-сірий
            if d == today:
                color = "#3AA76D"  # зелений
            elif str(d) in done_dates_set:
                color = "#2E8B57"  # темно-зелений
            else:
                color = "#2A2F3A"  # темно-сірий

            cols[i].markdown(
                f"<div style='background:{color}; padding:10px; border-radius:8px; text-align:center; color:#FFF;'>"
                f"{day_short}</div>",
                unsafe_allow_html=True
            )

        st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)

        # ─── Сьогоднішній план ─────────────────────
        st.markdown("<div style='height:0.5px'></div>", unsafe_allow_html=True)
        st.subheader("📌 Сьогоднішній план")

        today_tasks = [t for t in data["homework"] + data["goals"] if t["date"] == str(today)]

        if not today_tasks:
            st.info("Сьогодні завдань немає")
        else:
            for t in today_tasks:
                subject = t.get("subject", "")
                status = "✅" if t.get("done", False) else "❌"
                st.markdown(
                    f"<div style='background:#1E1E1E; padding:10px; border-radius:8px; margin-bottom:6px;'>"
                    f"{status} {t['title']} {f'({subject})' if subject else ''}</div>",
                    unsafe_allow_html=True
                )

        st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)

        # ─── Пропущені дедлайни ─────────────────────
        st.subheader("⚠️ Пропущені дедлайни")

        missed = [
            t for t in data["homework"] + data["goals"]
            if not t.get("done", False) and date.fromisoformat(t["date"]) < today
        ]

        if not missed:
            st.success("Пропущених завдань немає 🎉")
        else:
            for t in missed:
                st.markdown(
                    f"<div style='background:#2E1E1E; padding:8px; border-radius:8px; margin-bottom:5px; color:#FF6F61;'>"
                    f"{t['title']}</div>",
                    unsafe_allow_html=True
                )

        st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)

        import random

        # ─── 🎲 Сюрприз дня ─────────────────────
        st.markdown("<div style='height:55px'></div>", unsafe_allow_html=True)  # відступ зверху

        st.subheader("🎲 Сюрприз дня")

        # Список сюрпризів / порад
        surprises = [
    "Вивчи одне нове слово англійською та використай його у реченні",
    "Повтори формули з математики, які вчили на минулому уроці",
    "Прочитай коротку статтю з історії та запиши 3 ключові факти",
    "Вивчи одне нове правило з граматики рідної або іноземної мови",
    "Розв’яжи 3 завдання з алгебри або геометрії",
    "Перепиши конспект з одного предмету своїми словами",
    "Вивчи 5 нових слів з іноземної мови та склади з ними речення",
    "Подивись відео з поясненням теми з фізики або хімії і зроби короткі нотатки",
    "Зроби вправи на повторення минулого матеріалу (тести або задачі)",
    "Прочитай розділ з підручника і склади план конспекту",
    "Запиши короткий огляд теми, яку вивчаєш сьогодні",
    "Розв’яжи логічну задачу або задачу на мислення",
    "Придумай приклад задачі з математики та розв’яжи його сам",
    "Переглянь малюнок/схему з біології та поясни її словами",
    "Склади коротку таблицю фактів для швидкого повторення історії або географії",
    "Виконай 5 вправ з англійської граматики",
    "Вивчи одну формулу з фізики та запиши приклад її застосування",
    "Прочитай 1 абзац наукової статті та переказати власними словами",
    "Склади 3 запитання за матеріалом, який сьогодні вивчав"
]

        today_index = today.toordinal() % len(surprises)
        daily_surprise = surprises[today_index]

        # Стильований блок для чорної теми
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #2A2F3A, #4B0082);
                color: #FFFFFF;
                padding: 20px;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.5);
                margin-bottom: 20px;
                border: 1px solid #6A5ACD;
            ">
                🎉 {daily_surprise} 🎉
            </div>
            """,
            unsafe_allow_html=True
        )

    # ═══════════════════════════════════════
    # ПРАВА КОЛОНКА
    # ═══════════════════════════════════════
    with col_right:

        # ─── Нотатки ─────────────────────
        st.subheader("📝 Нотатки")

        notes = st.text_area(
            "Запиши щось важливе...",
            value=data.get("notes", ""),
            height=200  # збільшено висоту поля
        )

        if notes != data.get("notes", ""):
            data["notes"] = notes
            save_data(data)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # ─── Майбутні канікули ─────────────────────
        st.subheader("🏖️ Майбутні канікули")

        upcoming_vac = sorted(
            [v for v in data.get("vacations", []) if date.fromisoformat(v["end"]) >= today],
            key=lambda x: date.fromisoformat(x["start"])
        )

        if upcoming_vac:
            for vac in upcoming_vac:
                start_date = date.fromisoformat(vac["start"])
                end_date = date.fromisoformat(vac["end"])
                days_left = (start_date - today).days

                st.markdown(
                    f"<div style='background:#1E1E1E; padding:10px; border-radius:8px; margin-bottom:8px;'>"
                    f"<b>{vac['name']}</b><br>"
                    f"Початок: {start_date}<br>"
                    f"Кінець: {end_date}<br>"
                    f"Залишилось: {days_left} дн.</div>",
                    unsafe_allow_html=True
                )
        else:
            st.info("Канікули не заплановані")


# ════════════════════════════════════════════════════════════
# 📅 ПЛАН
# ════════════════════════════════════════════════════════════

if page == "📅 План":

    st.title("📅 Навчальний план")
    st.markdown("---")

    # ─── ДОБАВЛЕНИЕ ─────────────────────────────

    with st.container():
        st.subheader("➕ Додати")

        col_add1, col_add2 = st.columns(2)

        with col_add1:
            task_type = st.selectbox("Тип", ["Домашнє завдання", "Навчальна ціль"])
            title = st.text_input("Назва")

        with col_add2:
            deadline = st.date_input("Дедлайн", min_value=date.today())

            if task_type == "Домашнє завдання":
                subject = st.text_input("Предмет")

        if st.button("Додати", use_container_width=True, type="primary"):

            if title.strip() == "":
                st.error("Введи назву")
            else:

                if task_type == "Домашнє завдання":
                    data["homework"].append({
                        "id": str(len(data["homework"])),
                        "title": title,
                        "subject": subject,
                        "date": str(deadline),
                        "done": False
                    })
                else:
                    data["goals"].append({
                        "id": str(len(data["goals"])),
                        "title": title,
                        "date": str(deadline),
                        "done": False
                    })

                save_data(data)
                st.success("Додано ✅")
                st.rerun()

    st.markdown("---")

    # ─── СОРТИРОВКА ─────────────────────────────

    data["homework"] = sorted(data["homework"], key=lambda x: x["date"])
    data["goals"] = sorted(data["goals"], key=lambda x: x["date"])

    # ─── ФУНКЦИЯ ВИЗУАЛА ─────────────────────────────

    def render_task(task, task_type):

        task_date = date.fromisoformat(task["date"])
        days_left = (task_date - date.today()).days

        if days_left < 0:
            color = "#ff4b4b"   # просрочено
        elif days_left <= 2:
            color = "#ffa600"   # срочно
        else:
            color = "#2ecc71"   # нормально

        col1, col2 = st.columns([6, 1])

        with col1:
            if task_type == "homework":
                text = f"**{task['subject']}** — {task['title']}  \n📅 до {task['date']}"
            else:
                text = f"**{task['title']}**  \n📅 до {task['date']}"

            st.markdown(
                f"<div style='background-color:{color}20; padding:10px; border-radius:10px; margin-bottom:8px;'>"
                f"{text}"
                f"</div>",
                unsafe_allow_html=True
            )

        with col2:
            if st.button("🗑️", key=f"del_{task_type}_{task['id']}"):
                if task_type == "homework":
                    data["homework"] = [t for t in data["homework"] if t["id"] != task["id"]]
                else:
                    data["goals"] = [t for t in data["goals"] if t["id"] != task["id"]]

                save_data(data)
                st.rerun()

    # ─── АКТИВНЫЕ ─────────────────────────────

    st.subheader("📌 Активні")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📘 Домашні завдання")

        active_hw = [hw for hw in data["homework"] if not hw.get("done", False)]

        if not active_hw:
            st.info("Немає активних завдань")

        for hw in active_hw:
            checked = st.checkbox(
                "Виконано",
                key=f"hw_done_{hw['id']}"
            )

            render_task(hw, "homework")

            if checked:
                hw["done"] = True
                update_streak(data)
                save_data(data)
                st.rerun()

    with col2:
        st.markdown("### 🎯 Навчальні цілі")

        active_goals = [g for g in data["goals"] if not g.get("done", False)]

        if not active_goals:
            st.info("Немає активних цілей")

        for goal in active_goals:
            checked = st.checkbox(
                "Виконано",
                key=f"goal_done_{goal['id']}"
            )

            render_task(goal, "goal")

            if checked:
                goal["done"] = True
                save_data(data)
                st.rerun()

    st.markdown("---")

    # ─── ВИКОНАНІ ─────────────────────────────
    with st.expander("✅ Виконані"):

        col1, col2 = st.columns(2)

        # ─── ДОМАШНІ ─────────────────
        with col1:
            st.markdown("### 📘 Домашні завдання")

            done_hw = [hw for hw in data["homework"] if hw.get("done", False)]

            if not done_hw:
                st.write("Немає виконаних")

            for hw in done_hw:

                col_a, col_b = st.columns([5, 1])

                with col_a:
                    st.markdown(f"~~{hw['subject']} — {hw['title']}~~")

                with col_b:
                    if st.button("🗑️", key=f"del_done_hw_{hw['id']}"):
                        data["homework"] = [
                            x for x in data["homework"] if x["id"] != hw["id"]
                        ]
                        save_data(data)
                        st.rerun()

        # ─── ЦІЛІ ─────────────────
        with col2:
            st.markdown("### 🎯 Навчальні цілі")

            done_goals = [g for g in data["goals"] if g.get("done", False)]

            if not done_goals:
                st.write("Немає виконаних")

            for goal in done_goals:

                col_a, col_b = st.columns([5, 1])

                with col_a:
                    st.markdown(f"~~{goal['title']}~~")

                with col_b:
                    if st.button("🗑️", key=f"del_done_goal_{goal['id']}"):
                        data["goals"] = [
                            x for x in data["goals"] if x["id"] != goal["id"]
                        ]
                        save_data(data)
                        st.rerun()

        st.markdown("---")

        # ─── КНОПКА ОЧИСТИТИ ВСІ ─────────────────
        if st.button("🧹 Очистити всі виконані", use_container_width=True):
            data["homework"] = [hw for hw in data["homework"] if not hw.get("done", False)]
            data["goals"] = [g for g in data["goals"] if not g.get("done", False)]
            save_data(data)
            st.rerun()

# ════════════════════════════════════════════════════════════
# 📊 АНАЛІТИКА
# ════════════════════════════════════════════════════════════
elif page == "📊 Аналітика":

    st.title("📊 Аналітика")
    st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)  # відступ після заголовка

    # ─── ВИЗНАЧЕННЯ ДАНИХ ─────────────────────────────
    total_hw = len(data["homework"])
    total_goals = len(data["goals"])
    total_tasks = total_hw + total_goals

    completed_hw = len([hw for hw in data["homework"] if hw.get("done", False)])
    completed_goals = len([g for g in data["goals"] if g.get("done", False)])
    total_completed = completed_hw + completed_goals

    completion_rate = round((total_completed / total_tasks) * 100, 1) if total_tasks > 0 else 0

    # ─── МЕТРИКИ ─────────────────────────────
    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)  # додатковий відступ перед картками
    col1, col2, col3, col4 = st.columns(4, gap="large")  # великий gap між метриками

    metric_style = """
    <div style='background-color:#1C1F26; padding:20px; border-radius:12px; text-align:center; border:1px solid #2A2F3A;'>
        <h2 style='color:#FFFFFF; margin:0'>{value}</h2>
        <p style='color:#BBBBBB; margin:0'>{label}</p>
    </div>
    """

    with col1:
        st.markdown(metric_style.format(value=total_tasks, label="Всього задач"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_style.format(value=total_completed, label="Виконано"), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_style.format(value=f"{completion_rate}%", label="Прогрес"), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_style.format(value=f"{data['streak']['count']} дн.", label="Серія 🔥"), unsafe_allow_html=True)

    # ─── ГОРИЗОНТАЛЬНА ЛІНІЯ ПІД МЕТРИКАМИ ─────────────
    st.markdown("<hr style='border:1px solid #2A2F3A; margin-top:20px; margin-bottom:25px'>", unsafe_allow_html=True)

    # ─── РОЗПОДІЛ ВИКОНАНИХ / НЕ ВИКОНАНИХ ─────────────────────────────
    st.subheader("Розподіл виконання задач")
    status_data = {
        "Статус": ["Виконано", "Не виконано"],
        "Кількість": [total_completed, total_tasks - total_completed]
    }

    fig_status = px.pie(
        status_data,
        names="Статус",
        values="Кількість",
        color_discrete_map={"Виконано":"#3AA76D", "Не виконано":"#E57373"},
        hole=0.5
    )
    fig_status.update_layout(
        template="plotly_dark",
        font_color="#FFFFFF",
        title_font_size=18,
        legend=dict(orientation="h", y=-0.2)
    )
    st.plotly_chart(fig_status, use_container_width=True)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ─── СТРУКТУРА ЗАДАЧ ─────────────────────────────
    st.subheader("Структура задач")
    type_data = {
        "Тип": ["Домашні завдання", "Навчальні цілі"],
        "Кількість": [total_hw, total_goals]
    }

    fig_type = px.bar(
        type_data,
        x="Тип",
        y="Кількість",
        text="Кількість",
        color="Тип",
        color_discrete_map={"Домашні завдання":"#8AB4F8", "Навчальні цілі":"#FBC02D"}
    )
    fig_type.update_traces(marker_line_color='#1C1F26', marker_line_width=1.5)
    fig_type.update_layout(
        template="plotly_dark",
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font_color="#FFFFFF",
        title_font_size=18,
        showlegend=False,
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_type, use_container_width=True)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ─── АКТИВНІСТЬ ЗА 30 ДНІВ ─────────────────────────────
    st.subheader("Активність за останні 30 днів")
    done_dates = data["streak"].get("done_dates", [])
    today = date.today()
    days_30 = [(today - timedelta(days=i)) for i in range(29, -1, -1)]

    activity = []
    for d in days_30:
        activity.append({
            "Дата": d,
            "Активність": 1 if str(d) in done_dates else 0
        })

    fig_activity = px.bar(
        activity,
        x="Дата",
        y="Активність",
        text="Активність",
        color="Активність",
        color_discrete_map={1:"#3AA76D", 0:"#E57373"}
    )
    fig_activity.update_traces(marker_line_color='#0E1117', marker_line_width=1)
    fig_activity.update_layout(
        template="plotly_dark",
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font_color="#FFFFFF",
        title_font_size=18,
        yaxis=dict(showticklabels=False, showgrid=False)
    )
    st.plotly_chart(fig_activity, use_container_width=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# 🏖️ КАНІКУЛИ (мінімально)
# ════════════════════════════════════════════════════════════
elif page == "🏖️ Канікули":

    st.title("🏖️ Канікули та перерви")
    st.markdown("---")

    st.subheader("➕ Додати період канікул")

    col1, col2 = st.columns(2)

    with col1:
        vac_name = st.text_input("Назва періоду (наприклад: Зимові канікули)")
        vac_start = st.date_input("Початок", key="vac_start")

    with col2:
        vac_end = st.date_input("Кінець", key="vac_end")

    if st.button("Додати період", use_container_width=True, type="primary"):

        if vac_name.strip() == "":
            st.error("Введи назву періоду")
        elif vac_end < vac_start:
            st.error("Дата завершення не може бути раніше початку")
        else:
            data["vacations"].append({
                "name": vac_name,
                "start": str(vac_start),
                "end": str(vac_end)
            })

            save_data(data)
            st.success("Період додано ✅")
            st.rerun()

    st.markdown("---")

    st.subheader("📋 Заплановані перерви")

    if not data["vacations"]:
        st.info("Поки що немає доданих канікул")

    for v in data["vacations"]:

        start = date.fromisoformat(v["start"])
        end = date.fromisoformat(v["end"])
        duration = (end - start).days + 1

        col_a, col_b = st.columns([6, 1])

        with col_a:
            st.markdown(
                f"""
                <div style='background-color:#E3F2FD; padding:12px; border-radius:10px; margin-bottom:10px;'>
                <b>{v['name']}</b><br>
                📅 {v['start']} → {v['end']}<br>
                ⏳ {duration} днів
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_b:
            if st.button("🗑️", key=f"del_vac_{v['name']}"):
                data["vacations"] = [x for x in data["vacations"] if x != v]
                save_data(data)
                st.rerun()

    st.markdown("---")

    # ─── СТАТИСТИКА ПО КАНІКУЛАХ ─────────────────────────────

    st.subheader("📊 Статистика")

    total_vacations = len(data["vacations"])

    total_days = 0
    for v in data["vacations"]:
        start = date.fromisoformat(v["start"])
        end = date.fromisoformat(v["end"])
        total_days += (end - start).days + 1

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.metric("🏖️ Кількість періодів", total_vacations)

    with col_s2:
        st.metric("📅 Всього днів канікул", total_days)

    st.markdown("---")

    st.info(
        "Під час канікул серія 🔥 не переривається. "
        "Система автоматично не враховує ці дні як навчальні."
    )

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
