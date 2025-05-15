import streamlit as st

st.set_page_config(
    page_title="Airfare Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Dashboard цен авиабилетов (2025)")
st.sidebar.title("Навигация")

page = st.sidebar.radio("Перейти на страницу:", [
    "1. Данные",
    "2. EDA",
    "3. Тренды & закономерности",
    "4. Выводы & рекомендации"
])

if page == "1. Данные":
    from pages import data as module
elif page == "2. EDA":
    from pages import eda as module
elif page == "3. Тренды & закономерности":
    from pages import trends as module
else:
    from pages import conclusions as module

module.app()
