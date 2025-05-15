import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def app():
    st.header("2. Разведочный анализ (EDA)")
    df = pd.read_csv("data/flight_prices.csv")

    st.subheader("Распределение числа маршрутов по авиакомпаниям")
    companies = ['Россия','Аэрофлот','Победа','S7 Airlines','Уральские авиалинии']

    route_counts = [df[c].notna().sum() for c in companies]
    fig, ax = plt.subplots(figsize=(6,3))

    sns.barplot(x=companies, y=route_counts, ax=ax, palette="pastel")

    ax.set_ylabel("Число маршрутов")
    ax.set_xticklabels(companies, rotation=45)
    st.pyplot(fig)

    st.subheader("Статистика цен (руб.)")

    st.write(df[companies].describe())
