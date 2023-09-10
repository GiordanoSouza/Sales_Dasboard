import pandas as pd
import plotly.express as px 
import streamlit as st

# Configurando a página do STREAMLITE ==============================================================================

st.set_page_config(page_title="sales Dash",
                   page_icon=":bar_chart",
                   layout="wide"
)

# PUXANDO AS PLANILHAS ===============================================================================================

df = pd.read_csv('SQL.csv')

df_decoded = pd.read_csv("Decoded.csv")

# Mudança da Data para mês ==========================================================================================

df['won_time'] = pd.to_datetime(df['won_time'])
df['won_mes'] = df['won_time'].dt.month

# Mudança da Data para Ano ==========================================================================================
df['won_year'] = df['won_time'].dt.year

# Preenchendo espaços de NAN com 0 ===============================================================================

df['won_mes'].fillna(0, inplace=True)
df['won_year'].fillna(0, inplace=True)

# Substitui os números dos meses pelos nomes dos meses ============================================================

meses = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}

df['won_mes'] = df['won_mes'].map(meses)

# Decodificando os "id" em valores no "id_lead_origin" da planilha SQL.csv ===============================================
# PS 1: transformando os valores "NAN" em 0  
# PS 2: Transformando os números de ambos em Inteiros. Sem isso,a operação de mapear o dicionário não funciona

for i in range(len(df_decoded)):
    try:
        int_value = int(df_decoded.at[i, "id"])
        df_decoded.at[i, "id"] = int_value
    except ValueError:
        current_id = df_decoded.at[i, "id"]
        df_decoded.at[i, "id"] = 0

for i in range(len(df)):
    try:
        int_value = int(df.at[i, "id_lead_origin"])
        df.at[i, "id_lead_origin"] = int_value
    except ValueError:
        current_id = df.at[i, "id_lead_origin"]
        df.at[i, "id_lead_origin"] = 0
        
for i in range(len(df)):
    try:
        int_value = int(df.at[i, "id_segmentation"])
        df.at[i, "id_segmentation"] = int_value
    except ValueError:
        current_id = df.at[i, "id_segmentation"]
        df.at[i, "id_segmentation"] = 0


mapping_dict = df_decoded.set_index("id")["label"].to_dict()

df["id_lead_origin"] = df["id_lead_origin"].map(mapping_dict)
df["id_segmentation"] = df["id_segmentation"].map(mapping_dict)


# st.dataframe(df)

# Criando a SIDEBAR e seus respectivos filtros ==================================================================

st.sidebar.header("Please Filter Here: ")

won_mes = st.sidebar.multiselect(
    "select the month:",
    options=df["won_mes"].unique(),
    default=df["won_mes"].unique()
)

won_year = st.sidebar.multiselect(
    "select the Customer Type:",
    options=df["won_year"].unique(),
    default=df["won_year"].unique()
)

# Alinhando a variável dos filtros com a tabela 
 
df_selection = df.query(
    "won_mes == @won_mes & won_year == @won_year"
)



# # MAIN PAGE ============================================================================================

st.title(":bar_chart: Sales DashBoard")


# # Bar Chart ====

Total = df_selection["title"].count()

column = st.columns(3)

with column[0]:  # Ajuste o índice conforme necessário
    st.subheader("Total:")
    st.subheader(str(Total))

# Montando o gráfico ==========
with column[1]:
    st.subheader("Sales by Lead Origin")
    filtered_data = df_selection.copy()

    lead_origin_counts = filtered_data["id_lead_origin"].value_counts().reset_index()
    lead_origin_counts.columns = ["id_lead_origin", "count"]


    fig = px.bar(
        filtered_data,
        x="id_lead_origin",
        title="Contagem de Leads por Origem",
        labels={"id_lead_origin": "Origem do Lead", "count": "Contagem"},
    )

    for idx, row in lead_origin_counts.iterrows():
        fig.add_annotation(
            x=row["id_lead_origin"],
            y=row["count"],
            text=str(row["count"]),
            showarrow=True,
            font=dict(size=10),
            align="center",
        )
    st.plotly_chart(fig, use_container_width=True)

# GRAFICO 2
with column[2]:
    st.subheader("Sales by Lead Segmentação")


    lead_segmentation_counts = filtered_data["id_segmentation"].value_counts().reset_index()
    lead_segmentation_counts.columns = ["id_segmentation", "count"]


    fig2 = px.bar(
        filtered_data,
        x="id_segmentation",
        title="Contagem de Leads por Origem",
        labels={"id_segmentation": "Segmentação", "count": "Contagem"},
    )

    for idx, row in lead_segmentation_counts.iterrows():
        fig2.add_annotation(
            x=row["id_segmentation"],
            y=row["count"],
            text=str(row["count"]),
            showarrow=True,
            font=dict(size=10),
            align="center",
        )

    st.plotly_chart(fig2, use_container_width=True)

# PErsonalizando =====================


# Fundo personalizado


# Conteúdo da coluna 1


# Dropando o streamlit XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX 

st.dataframe(df_selection[["title","id_segmentation","id_lead_origin"]])

