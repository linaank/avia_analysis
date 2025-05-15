import streamlit as st
import pandas as pd

def app():
    st.header("1. Данные")

    st.markdown("""
    **Описание набора данных**  
    В таблице `flight_prices.csv` находятся маршруты (origin -> dest) и цены (в руб.) 
    от пяти авиакомпаний: Россия, Аэрофлот, Победа, S7 Airlines, Уральские авиалинии.
    """)

    df = pd.read_csv("data/flight_prices.csv")

    st.subheader("Основные характеристики")

    st.write(f"- Всего маршрутов: {df.shape[0]}")
    st.write(f"- Столбцы: {', '.join(df.columns)}")

    st.write("Количество пропусков по столбцам:")
    st.write(df.isna().sum())

    st.subheader("Интерактивная таблица")
    st.dataframe(df, use_container_width=True)
