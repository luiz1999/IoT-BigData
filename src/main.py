import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Dashboard IoT", layout="wide")
st.title("📊 Pipeline de Dados IoT — Temperaturas")
st.markdown("**Disruptive Architectures: IoT, Big Data e IA | UniFECAF**")


def get_db_connection():
    url = os.getenv("DATABASE_URL")
    if not url:
        st.error(
            "❌ DATABASE_URL não encontrada. Crie o arquivo .env na raiz do projeto.")
        st.stop()
    return create_engine(url)


engine = get_db_connection()

# ── UPLOAD ──
st.header("📂 Upload de Arquivo CSV")
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Estrutura do Dataset:")
    st.write(df.head())

    if st.button("Inserir dados no PostgreSQL"):
        with st.spinner("Inserindo dados..."):
            df.to_sql("temperature_readings", engine,
                      if_exists="replace", index=False)

            with engine.connect() as conn:
                conn.execute(text("""
                    CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
                    SELECT
                        "room_id/id"  AS device_id,
                        "out/in"      AS local,
                        ROUND(AVG(temp)::numeric, 2) AS avg_temp,
                        COUNT(*)      AS total_leituras
                    FROM temperature_readings
                    GROUP BY "room_id/id", "out/in"
                    ORDER BY avg_temp DESC;
                """))
                conn.execute(text("""
                    CREATE OR REPLACE VIEW leituras_por_hora AS
                    SELECT
                        EXTRACT(HOUR FROM TO_TIMESTAMP(
                            noted_date, 'DD-MM-YYYY HH24:MI'
                        ))::int AS hora,
                        COUNT(*) AS total_leituras,
                        ROUND(AVG(temp)::numeric, 2) AS avg_temp_hora
                    FROM temperature_readings
                    GROUP BY hora
                    ORDER BY hora;
                """))
                conn.execute(text("""
                    CREATE OR REPLACE VIEW temp_max_min_por_dia AS
                    SELECT
                        DATE(TO_TIMESTAMP(
                            noted_date, 'DD-MM-YYYY HH24:MI'
                        )) AS data,
                        ROUND(MAX(temp)::numeric, 2) AS temp_max,
                        ROUND(MIN(temp)::numeric, 2) AS temp_min,
                        ROUND(AVG(temp)::numeric, 2) AS temp_media
                    FROM temperature_readings
                    GROUP BY data
                    ORDER BY data;
                """))
                conn.commit()

        st.success("✅ Dados inseridos e views criadas com sucesso!")
        st.balloons()

# ── DASHBOARD ──
st.header("📈 Visualização dos Dados")

st.subheader("1. Média de Temperatura por Dispositivo e Local")
try:
    df1 = pd.read_sql("SELECT * FROM avg_temp_por_dispositivo", engine)
    fig1 = px.bar(
        df1, x="local", y="avg_temp", color="local", text="avg_temp",
        title="Temperatura Média: Interno vs Externo",
        labels={"local": "Local", "avg_temp": "Temp. Média (°C)"},
        color_discrete_map={"In": "#185FA5", "Out": "#E24B4A"},
    )
    fig1.update_traces(texttemplate="%{text:.2f}°C", textposition="outside")
    fig1.update_layout(showlegend=False, height=420)
    st.plotly_chart(fig1, use_container_width=True)
except Exception as e:
    st.warning(
        f"Gráfico 1: {e} — faça o upload do CSV e clique em 'Inserir dados'.")

st.subheader("2. Leituras por Hora do Dia")
try:
    df2 = pd.read_sql("SELECT * FROM leituras_por_hora", engine)
    fig2 = px.line(
        df2, x="hora", y="total_leituras", markers=True,
        title="Quantidade de Leituras por Hora",
        labels={"hora": "Hora do Dia", "total_leituras": "Nº de Leituras"},
        color_discrete_sequence=["#1D9E75"],
    )
    fig2.update_layout(xaxis=dict(tickmode="linear", dtick=1), height=380)
    st.plotly_chart(fig2, use_container_width=True)
except Exception as e:
    st.warning(
        f"Gráfico 2: {e} — faça o upload do CSV e clique em 'Inserir dados'.")

st.subheader("3. Temperaturas Máximas e Mínimas por Dia")
try:
    df3 = pd.read_sql("SELECT * FROM temp_max_min_por_dia", engine)
    fig3 = px.line(
        df3, x="data", y=["temp_max", "temp_min", "temp_media"], markers=True,
        title="Evolução Diária de Temperatura",
        labels={"data": "Data",
                "value": "Temperatura (°C)", "variable": "Métrica"},
        color_discrete_map={"temp_max": "#E24B4A",
                            "temp_min": "#378ADD", "temp_media": "#1D9E75"},
    )
    fig3.update_layout(height=420)
    st.plotly_chart(fig3, use_container_width=True)
except Exception as e:
    st.warning(
        f"Gráfico 3: {e} — faça o upload do CSV e clique em 'Inserir dados'.")

st.subheader("📊 Métricas Gerais")
try:
    total = pd.read_sql(
        "SELECT COUNT(*) AS n FROM temperature_readings", engine).iloc[0, 0]
    tmax = pd.read_sql(
        "SELECT MAX(temp) FROM temperature_readings", engine).iloc[0, 0]
    tmin = pd.read_sql(
        "SELECT MIN(temp) FROM temperature_readings", engine).iloc[0, 0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de Leituras", f"{total:,}")
    c2.metric("Temperatura Máxima", f"{tmax}°C")
    c3.metric("Temperatura Mínima", f"{tmin}°C")
except:
    st.info("Métricas disponíveis após inserir os dados.")

st.caption("Projeto Disruptive Architectures: IoT, Big Data e IA | UniFECAF")
