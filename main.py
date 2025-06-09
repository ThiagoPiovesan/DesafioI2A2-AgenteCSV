import os
import zipfile
import asyncio
import pandas as pd
import streamlit as st
from llama_index.core.query_engine import PandasQueryEngine
from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.llms.openai import OpenAI

# Configurar API Key (pode também ser feita via variável de ambiente)
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Consulta de Notas Fiscais", layout="wide")
st.title("Agente de Consulta de Notas Fiscais - Jan/2024")

uploaded_file = st.file_uploader("Faça upload do arquivo 202401_NFs.zip", type=["zip"])

if uploaded_file is not None:
    with open("temp.zip", "wb") as f:
        f.write(uploaded_file.read())

    with zipfile.ZipFile("temp.zip", 'r') as zip_ref:
        zip_ref.extractall("data")

    os.remove("temp.zip")

    # Verificar se os arquivos existem
    cab_path = "data/202401_NFs_Cabecalho.csv"
    itens_path = "data/202401_NFs_Itens.csv"

    if os.path.exists(cab_path) and os.path.exists(itens_path):
        df_cab = pd.read_csv(cab_path)
        df_itens = pd.read_csv(itens_path)

        st.success("Arquivos carregados com sucesso!")

        aba = st.radio("Escolha a tabela para consulta:", ["Cabeçalho", "Itens"])

        user_query = st.text_input("Digite sua pergunta sobre as notas fiscais:")

        if user_query:
            # Cria contexto com LLM da OpenAI
            llm = OpenAI(model="gpt-3.5-turbo")

            if aba == "Cabeçalho":
                query_engine = PandasQueryEngine(df=df_cab, llm=llm)
            else:
                query_engine = PandasQueryEngine(df=df_itens, llm=llm)

            response = query_engine.query(user_query)
            st.subheader("Resposta:")
            st.write(str(response))

    else:
        st.error("Arquivos CSV não encontrados dentro do ZIP.")