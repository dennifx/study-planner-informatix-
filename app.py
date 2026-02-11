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
from datetime import date
import plotly.express as px


st.set_page_config(
    page_title="Study Planner",
    page_icon="📚",
    layout="wide"
)


DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"homework": [], "goals": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()


import streamlit as st

# Заголовок сайдбару
st.sidebar.title("📚 Study Planner")

# Горизонтальна лінія під заголовком
st.sidebar.markdown("<hr>", unsafe_allow_html=True)



# Навігація
st.sidebar.markdown("### Навігація")
page = st.sidebar.radio(
    "",
    ["📅 План","➕ Додати", "📊 Аналітика", "ℹ️ Про проєкт"]
)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.sidebar.caption("Informatix Project")

if page == "📅 План":
    st.title("📅 Навчальний план")

    # --- горизонтальна лінія під заголовком ---
    st.markdown("---")

    # --- відступ після лінії, щоб текст не прилипав ---
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📘 Домашні завдання")
        if not data["homework"]:
            st.info("Немає домашніх завдань")

        new_homework = []
        priority_emoji = {"Низький": "🟢", "Середній": "🟡", "Високий": "🔴"}

        for hw in data["homework"]:
            if "priority" not in hw:
                hw["priority"] = "Середній"

            checked = st.checkbox(
                f"{priority_emoji.get(hw['priority'], '')} {hw['subject']} — {hw['title']} (до {hw['date']})",
                value=False,
                key=f"hw_{hw['id']}"
            )

            if not checked:
                new_homework.append(hw)

        data["homework"] = new_homework
        save_data(data)

    with col2:
        st.subheader("🎯 Навчальні цілі")
        if not data["goals"]:
            st.info("Немає цілей")

        new_goals = []

        # Індикатори по терміну виконання
        term_emoji = {
            "Короткострокова (1-4 тижня)": "🟢",
            "Середньострокова (1-3 місяця)": "🟡",
            "Довгострокова (3–12 місяців)": "🔴"
        }

        for goal in data["goals"]:
            # чекбокс для виконання цілі
            done = st.checkbox(
                f"{term_emoji.get(goal['term'], '')} {goal['title']}",
                value=False,
                key=f"goal_{goal['id']}"
            )

            # якщо користувач не поставив галочку — залишаємо ціль
            if not done:
                new_goals.append(goal)

        data["goals"] = new_goals
        save_data(data)

elif page == "➕ Додати":
    st.title("➕ Додати завдання або ціль")

    # --- горизонтальна лінія під заголовком ---
    st.markdown("---")

    # --- відступ після лінії, щоб форма не прилипала ---
    st.markdown("<br>", unsafe_allow_html=True)

    task_type = st.selectbox(
        "Тип",
        ["Домашнє завдання", "Навчальна ціль"]
    )

    # --- Домашнє завдання ---
    if task_type == "Домашнє завдання":
        title = st.text_input("Назва")
        subject = st.text_input("Предмет")

        priority_options = {"Низький": "🟢", "Середній": "🟡", "Високий": "🔴"}
        priority_text = st.selectbox(
            "Пріоритет",
            ["Низький", "Середній", "Високий"],
            format_func=lambda x: f"{priority_options[x]} {x}"
        )

        deadline = st.date_input("Дедлайн", min_value=date.today())

    # --- Навчальна ціль ---
    elif task_type == "Навчальна ціль":
        title = st.text_input("Назва")

        term_options = {
            "Короткострокова (1-4 тижня)": "🟢",
            "Середньострокова (1-3 місяця)": "🟡",
            "Довгострокова (3–12 місяців)": "🔴"
        }
        term_text = st.selectbox(
            "Термін виконання",
            ["Короткострокова (1-4 тижня)", "Середньострокова (1-3 місяця)", "Довгострокова (3–12 місяців)"],
            format_func=lambda x: f"{term_options[x]} {x}"
        )

        goal_deadline = st.date_input("Дедлайн (опціонально)", min_value=date.today())

    # --- Кнопка додати ---
    if st.button("➕ Додати", key="add_task", use_container_width=True):
        if title.strip() == "":
            st.error("Введи назву")
        else:
            if task_type == "Домашнє завдання":
                data["homework"].append({
                    "id": f"{len(data['homework'])}",
                    "title": title,
                    "subject": subject,
                    "priority": priority_text,
                    "date": str(deadline),
                    "done": False
                })
            else:  # Навчальна ціль
                data["goals"].append({
                    "id": f"{len(data['goals'])}",
                    "title": title,
                    "term": term_text,
                    "date": str(goal_deadline),
                    "done": False
                })

            save_data(data)
            st.success("Додано! Оновіть сторінку, щоб побачити зміни")

elif page == "📊 Аналітика":
    st.title("📊 Аналітика та прогрес")

    # --- горизонтальна лінія ---
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)

    # Підрахунок домашніх завдань
    total_hw = len(data["homework"])
    done_hw = len([h for h in data["homework"] if h.get("done", False)])
    todo_hw = total_hw - done_hw

    # Підрахунок цілей
    total_goals = len(data["goals"])
    done_goals = len([g for g in data["goals"] if g.get("done", False)])
    todo_goals = total_goals - done_goals

    # --- Прогрес-бари ---
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div style='font-size:24px; font-weight:bold; margin-bottom:5px;'>📘 Домашні завдання</div>",
                    unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:16px; color:gray; margin-bottom:10px;'>{done_hw}/{total_hw} виконано</div>",
                    unsafe_allow_html=True)
        st.progress(total_hw and done_hw / total_hw or 0)

    with col2:
        st.markdown(f"<div style='font-size:24px; font-weight:bold; margin-bottom:5px;'>🎯 Навчальні цілі</div>",
                    unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:16px; color:gray; margin-bottom:10px;'>{done_goals}/{total_goals} виконано</div>",
            unsafe_allow_html=True)
        st.progress(total_goals and done_goals / total_goals or 0)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Кругові діаграми виконання ---
    col1, col2 = st.columns(2)
    with col1:
        if total_hw > 0:
            fig_hw = px.pie(
                names=["Виконано", "В процесі"],
                values=[done_hw, todo_hw],
                color_discrete_sequence=["#00C49F", "#FFBB28"]
            )
            fig_hw.update_layout(title="Домашні завдання", title_x=0.5)
            st.plotly_chart(fig_hw, use_container_width=True)
        else:
            st.info("Немає домашніх завдань для аналізу")

    with col2:
        if total_goals > 0:
            fig_goals = px.pie(
                names=["Досягнуто", "В процесі"],
                values=[done_goals, todo_goals],
                color_discrete_sequence=["#0088FE", "#FF8042"]
            )
            fig_goals.update_layout(title="Навчальні цілі", title_x=0.5)
            st.plotly_chart(fig_goals, use_container_width=True)
        else:
            st.info("Немає цілей для аналізу")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Фільтри для домашніх завдань за пріоритетом ---
    st.subheader("Фільтр домашніх завдань за пріоритетом")
    priority_filter = st.multiselect(
        "Виберіть пріоритет",
        ["Низький", "Середній", "Високий"],
        default=["Низький", "Середній", "Високий"]
    )

    filtered_hw = [h for h in data["homework"] if any(p in h["priority"] for p in priority_filter)]

    if filtered_hw:
        fig_bar_hw = px.bar(
            x=[h["title"] for h in filtered_hw],
            y=[1 for _ in filtered_hw],
            color=[h["priority"] for h in filtered_hw],
            color_discrete_map={"Низький": "#00C49F", "Середній": "#FFBB28", "Високий": "#FF4136"},
            labels={"y": "Кількість"}
        )
        fig_bar_hw.update_layout(showlegend=False, yaxis=dict(showticklabels=False))
        st.plotly_chart(fig_bar_hw, use_container_width=True)
    else:
        st.info("Немає завдань для обраного фільтру")

    # --- Фільтри для цілей за терміном ---
    st.subheader("Фільтр навчальних цілей за терміном")
    term_filter = st.multiselect(
        "Виберіть термін виконання",
        ["Короткострокова (1-4 тижня)", "Середньострокова (1-3 місяця)", "Довгострокова (3–12 місяців)"],
        default=["Короткострокова (1-4 тижня)", "Середньострокова (1-3 місяця)", "Довгострокова (3–12 місяців)"]
    )

    filtered_goals = [g for g in data["goals"] if g["term"] in term_filter]

    if filtered_goals:
        fig_bar_goals = px.bar(
            x=[g["title"] for g in filtered_goals],
            y=[1 for _ in filtered_goals],
            color=[g["term"] for g in filtered_goals],
            color_discrete_map={
                "Короткострокова (1-4 тижня)": "#00C49F",
                "Середньострокова (1-3 місяця)": "#FFBB28",
                "Довгострокова (3–12 місяців)": "#FF4136"
            },
            labels={"y": "Кількість"}
        )
        fig_bar_goals.update_layout(showlegend=False, yaxis=dict(showticklabels=False))
        st.plotly_chart(fig_bar_goals, use_container_width=True)
    else:
        st.info("Немає цілей для обраного фільтру")

elif page == "ℹ️ Про проєкт":
    st.title("ℹ️ Про Study Planner")

    # --- горизонтальная линия под заголовком ---
    st.markdown("---")

    # --- небольшой отступ после линии, чтобы текст не прилипал ---
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Контейнеры с блоками информации ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📘 Завдання")
        st.markdown("""
        <div style="background-color:#E3F2FD; padding:20px; border-radius:10px; font-size:16px; color:black; margin-bottom:20px;">
        - Додавай домашні завдання<br>
        - Встановлюй дедлайни<br>
        - Відмічай виконані завдання одним кліком
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🎯 Цілі")
        st.markdown("""
        <div style="background-color:#FFF3E0; padding:20px; border-radius:10px; font-size:16px; color:black; margin-bottom:20px;">
        - Відслідковуй навчальні цілі<br>
        - Став короткострокові та довгострокові цілі<br>
        - Миттєво відмічай виконані
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("📊 Прогрес")
        st.markdown("""
        <div style="background-color:#E8F5E9; padding:20px; border-radius:10px; font-size:16px; color:black; margin-bottom:20px;">
        - Візуальна аналітика прогресу<br>
        - Графіки виконання завдань<br>
        - Легкий перегляд статистики
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🔹 Приклад прогресу користувача")

    col1, col2 = st.columns(2)

    progress_homework = 70
    progress_goals = 50

    with col1:
        st.markdown(f"""
        <div style="margin-top:20px; font-size:24px; font-weight:bold; margin-bottom:10px;">📘 Домашні завдання</div>
        <div style="font-size:16px; color:gray; margin-bottom:20px;">{progress_homework}% виконано</div>
        """, unsafe_allow_html=True)
        st.progress(progress_homework / 100)

    with col2:
        st.markdown(f"""
        <div style="margin-top:20px; font-size:24px; font-weight:bold; margin-bottom:10px;">🎯 Навчальні цілі</div>
        <div style="font-size:16px; color:gray; margin-bottom:20px;">{progress_goals}% виконано</div>
        """, unsafe_allow_html=True)
        st.progress(progress_goals / 100)

    with st.expander("Детальніше про Завдання"):
        st.markdown("""
        <div style="color:white; line-height:1.8; margin-top:10px;">
        - Можливість додавати завдання та ставити дедлайн<br>
        - Checkbox для відмітки виконаних завдань<br>
        - Пріоритети від низького до високого з кольоровими емодзі
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Детальніше про Цілі"):
        st.markdown("""
        <div style="color:white; line-height:1.8; margin-top:10px;">
        - Короткострокові та довгострокові цілі<br>
        - Відмітка виконаних цілей одним кліком<br>
        - Пріоритети з кольоровими індикаторами
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Детальніше про Прогрес"):
        st.markdown("""
        <div style="color:white; line-height:1.8; margin-top:10px;">
        - Динамічні графіки виконання<br>
        - Візуальна аналітика домашніх завдань і цілей<br>
        - Статистика за предметами та пріоритетом
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    🌱 **Ціль сталого розвитку:** Якісна освіта (SDG 4)  
    © 2026 Study Planner — створено для презентації на **Informatix**
    """)

