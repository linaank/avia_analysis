import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def app():
    st.header("3. Тренды & закономерности")

    df = pd.read_csv("data/flight_prices.csv")

    companies = ['Россия','Аэрофлот','Победа','S7 Airlines','Уральские авиалинии']

    df_long = df.melt(id_vars=['origin','dest'], value_vars=companies,
                      var_name='Авиакомпания', value_name='Цена')

    # распределение цен компаний
    st.subheader("Распределение цен по компаниям")

    fig1, ax1 = plt.subplots(figsize=(6,4))
    sns.boxplot(x='Авиакомпания', y='Цена', data=df_long, ax=ax1, palette="muted")

    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
    st.pyplot(fig1)

    # средняя цена компании
    st.subheader("Средняя цена по компании")

    avg = df_long.groupby('Авиакомпания')['Цена'].mean().sort_values()
    fig2, ax2 = plt.subplots(figsize=(6,3))

    sns.barplot(x=avg.index, y=avg.values, ax=ax2, palette="pastel")

    ax2.set_ylabel("Средняя цена")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)

    st.pyplot(fig2)

    # тепловая карта
    st.subheader("Тепловая карта цен для авиакомпании")

    df['Средняя цена'] = df[companies].mean(axis=1, skipna=True)

    pivot = df.pivot(index='origin', columns='dest', values='Средняя цена')

    fig3, ax3 = plt.subplots(figsize=(10, 8))
    sns.heatmap(pivot, cmap='coolwarm', annot=True, fmt=".0f")

    plt.title("Средние цены между направлениями", fontsize=14)

    plt.xlabel("Город назначения")
    plt.ylabel("Город вылета")

    st.pyplot(fig3)
