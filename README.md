# Agente de Consulta de Notas Fiscais - Janeiro/2024

Este projeto permite ao usuário realizar perguntas em linguagem natural sobre os dados de notas fiscais contidos no arquivo `202401_NFs.zip`, disponibilizado pelo TCU.

## 📂 Conteúdo do ZIP

- `202401_NFs_Cabecalho.csv`: Informações gerais das notas fiscais.
- `202401_NFs_Itens.csv`: Itens detalhados vinculados a cada nota.

## 🚀 Funcionalidades

- Interface amigável com Streamlit.
- Descompactação automática do arquivo.
- Consulta em linguagem natural usando LlamaIndex (`PandasQueryEngine`).
- Suporte à seleção entre cabeçalho e itens das notas fiscais.

## ✅ Pré-requisitos

Python 3.8 ou superior

## Como conseguir a API Key do GPT

[Link to API Key](https://platform.openai.com/api-keys)

### Instale as dependências

pip install -r requirements.txt
