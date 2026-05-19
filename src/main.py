import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Conexão com o banco de dados


def get_db_connection():
    return create_engine(os.getenv("DATABASE_URL"))


engine = get_db_connection()

# Título do dashboard
st.title("Dashboard de Temperaturas IoT")

# ── Gráfico 1: Pizza — % de leituras In vs Out ──
st.header("1. Distribuição de Leituras: Interno vs Externo")
try:
    df1 = pd.read_sql("""
        SELECT "out/in" AS local, COUNT(*) AS total
       FROM temperature_readings
      GROUP BY "out/in"
    """, engine)
    fig1 = px.pie(
        df1,
        names="local",
        values="total",
        color="local",
        color_discrete_map={"Out": "#E05C5C", "In": "#4A90D9"},
    )
    fig1.update_traces(textinfo="label+percent", textfont_size=14)
    st.plotly_chart(fig1, use_container_width=True)
except Exception:
    st.info("Nenhum dado encontrado. Insira os dados no banco primeiro.")


# ── Gráfico 2: Leituras por hora ──
st.header("2. Leituras por Hora do Dia")
try:
    df2 = pd.read_sql("SELECT * FROM leituras_por_hora", engine)
    fig2 = px.line(
        df2,
        x="hora",
        y="contagem",
        markers=True,
        labels={"hora": "Hora do Dia", "contagem": "Nº de Leituras"},
    )
    fig2.update_layout(xaxis=dict(tickmode="linear", tick0=0, dtick=1))
    st.plotly_chart(fig2, use_container_width=True)
except Exception:
    st.info("Nenhum dado encontrado. Insira os dados no banco primeiro.")

# ── Gráfico 3: Máx e Mín por dia ──
st.header("3. Temperaturas Máximas e Mínimas por Dia")
try:
    df3 = pd.read_sql("SELECT * FROM temp_max_min_por_dia", engine)
    fig3 = px.line(
        df3,
        x="data",
        y=["temp_max", "temp_min"],
        markers=True,
        labels={"data": "Data", "value": "Temperatura (°C)", "variable": ""},
        color_discrete_map={"temp_max": "#E05C5C", "temp_min": "#4A90D9"},
    )
    st.plotly_chart(fig3, use_container_width=True)
except Exception:
    st.info("Nenhum dado encontrado. Insira os dados no banco primeiro.")

st.caption("Projeto Disruptive Architectures: IoT, Big Data e IA | UniFECAF")
