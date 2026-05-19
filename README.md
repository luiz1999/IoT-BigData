# Pipeline de Dados IoT — Temperaturas

**Disciplina:** Disruptive Architectures: IoT, Big Data e IA  
**Aluno:** Luiz Filipe Santiago Pereira  
**Repositório:** `{Luiz1999} - IoT-BigData`

---

## Sobre o projeto

Pipeline completo de dados para dispositivos IoT que:
- Armazena 97.606 leituras reais de temperatura em **PostgreSQL**
- Cria 3 **views SQL** para análise dos dados
- Visualiza em **dashboard interativo** com Streamlit e Plotly
- Deploy em produção no **Render.com**

---

## Tecnologias utilizadas

| Tecnologia | Papel no projeto |
|---|---|
| Python 3.11 | Linguagem principal |
| PostgreSQL 18 | Banco de dados (Docker local / Render) |
| Docker | Containerização do PostgreSQL |
| SQLAlchemy | Conexão Python → PostgreSQL |
| pandas | Leitura do CSV |
| Streamlit | Dashboard interativo |
| Plotly | Gráficos interativos |
| python-dotenv | Gerenciamento de credenciais |
| DBeaver | Administração do banco |
| Git / GitHub | Versionamento |
| Render.com | Deploy em produção |

---

## Dataset

**Temperature Readings: IoT Devices** — Kaggle  
Link: https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices

| Coluna | Descrição |
|---|---|
| `id` | Identificador único da leitura |
| `room_id/id` | ID do dispositivo (Room Admin) |
| `noted_date` | Data e hora da leitura |
| `temp` | Temperatura registrada (°C) |
| `out/in` | Leitura externa (Out) ou interna (In) |

> O CSV não está no repositório. Baixe pelo link acima.

---

## Como executar localmente

### 1. Pré-requisitos
- Python 3.11+
- Docker instalado

### 2. Subir o PostgreSQL com Docker
```bash
docker run --name postgres-iot \
  -e POSTGRES_PASSWORD=sua_senha \
  -p 5432:5432 \
  -d postgres
```

### 3. Criar o arquivo `.env` na raiz do projeto
```
DATABASE_URL=postgresql://postgres:sua_senha@localhost:5432/postgres
```

### 4. Instalar dependências
```bash
pip install streamlit pandas sqlalchemy psycopg2-binary plotly python-dotenv
```

### 5. Importar os dados
- Abra o DBeaver e conecte em `localhost:5432`
- Crie a tabela `temperature_readings`
- Importe o CSV via **Import Data**

### 6. Executar o dashboard
```bash
streamlit run src/main.py
```

Acesse em: http://localhost:8501

---

## Views SQL

### `avg_temp_por_dispositivo`
```sql
CREATE VIEW avg_temp_por_dispositivo AS
SELECT "out/in" AS local, COUNT(*) AS total
FROM temperature_readings
GROUP BY "out/in";
```
Mostra a proporção de leituras internas vs externas. Usada no gráfico de pizza.

---

### `leituras_por_hora`
```sql
CREATE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM TO_TIMESTAMP(noted_date, 'DD-MM-YYYY HH24:MI'))::int AS hora,
    COUNT(*) AS contagem
FROM temperature_readings
WHERE noted_date IS NOT NULL
AND EXTRACT(HOUR FROM TO_TIMESTAMP(noted_date, 'DD-MM-YYYY HH24:MI')) >= 0
GROUP BY hora
ORDER BY hora;
```
Conta leituras por hora do dia. Pico identificado às 14h com ~7.000 leituras.

---

### `temp_max_min_por_dia`
```sql
CREATE VIEW temp_max_min_por_dia AS
SELECT
    DATE(TO_TIMESTAMP(noted_date, 'DD-MM-YYYY HH24:MI')) AS data,
    MAX(temp) AS temp_max,
    MIN(temp) AS temp_min
FROM temperature_readings
GROUP BY data
ORDER BY data;
```
Mostra máxima e mínima por dia. Maior amplitude térmica em setembro/outubro 2018.

---

## Capturas de tela do dashboard


**Gráfico 1 — Pizza: Distribuição de leituras In vs Out**  
![Print 1](docs/img/print1.png)

**Gráfico 2 — Linha: Leituras por hora do dia**  
![Print 2](docs/img/print2.png)

**Gráfico 3 — Linha dupla: Temperaturas máximas e mínimas por dia**  
![Print 3](docs/img/print3.png)

---

## Principais insights

- **Temperatura externa maior:** média Out = 36,27°C vs In = 30,45°C (diferença de ~6°C)
- **Pico às 14h:** maior volume de leituras no período da tarde
- **Maior amplitude em setembro:** máximas chegando a 51°C, mínimas abaixo de 25°C
- **Queda em dezembro:** tendência de queda nas máximas a partir de novembro

---

## Estrutura do repositório

```
{nome}{sobrenome}bigdatafecaf/
├── src/
│   └── main.py         ← dashboard Streamlit
├── docs/
│   ├── print1.png      ← prints do dashboard
│   ├── print2.png
│   └── print3.png
├── .env.example        ← modelo de configuração
├── .gitignore
└── README.md
```

---

## Comandos Git utilizados

```bash
git init
git remote add origin https://github.com/SEU_USUARIO/{nome}{sobrenome}bigdatafecaf.git
git add .
git commit -m "feat: pipeline IoT com Streamlit e 3 views SQL"
git push -u origin main
```

---

