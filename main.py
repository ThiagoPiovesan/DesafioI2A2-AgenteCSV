import streamlit as st
import pandas as pd
import zipfile
import os
import io
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
import tempfile
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(
    page_title="Agente de Análise de Notas Fiscais",
    page_icon="📊",
    layout="wide"
)

class NotasFiscaisAgent:
    def __init__(self):
        self.df_cabecalho = None
        self.df_itens = None
        self.agent = None
        self.data_loaded = False
        
    def extract_zip_file(self, zip_file):
        """Extrai arquivos do ZIP uploadado"""
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # Criar diretório temporário
                temp_dir = tempfile.mkdtemp()
                zip_ref.extractall(temp_dir)
                
                # Listar arquivos extraídos
                extracted_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.csv'):
                            extracted_files.append(os.path.join(root, file))
                
                return extracted_files, temp_dir
        except Exception as e:
            st.error(f"Erro ao extrair arquivo ZIP: {str(e)}")
            return None, None
    
    def load_csv_files(self, file_paths):
        """Carrega os arquivos CSV"""
        try:
            cabecalho_file = None
            itens_file = None
            
            # Identificar arquivos por nome
            for file_path in file_paths:
                filename = os.path.basename(file_path).lower()
                if 'cabecalho' in filename or 'cabeçalho' in filename:
                    cabecalho_file = file_path
                elif 'itens' in filename or 'item' in filename:
                    itens_file = file_path
            
            if not cabecalho_file or not itens_file:
                st.error("Não foi possível identificar os arquivos de cabeçalho e itens.")
                return False
            
            # Carregar DataFrames
            self.df_cabecalho = pd.read_csv(cabecalho_file, encoding='utf-8')
            self.df_itens = pd.read_csv(itens_file, encoding='utf-8')
            
            # Processar datas se existirem
            date_columns = []
            for col in self.df_cabecalho.columns:
                if 'data' in col.lower() or 'date' in col.lower():
                    try:
                        self.df_cabecalho[col] = pd.to_datetime(self.df_cabecalho[col])
                        date_columns.append(col)
                    except:
                        pass
            
            for col in self.df_itens.columns:
                if 'data' in col.lower() or 'date' in col.lower():
                    try:
                        self.df_itens[col] = pd.to_datetime(self.df_itens[col])
                        date_columns.append(col)
                    except:
                        pass
            
            self.data_loaded = True
            return True
            
        except Exception as e:
            st.error(f"Erro ao carregar arquivos CSV: {str(e)}")
            return False
    
    def create_agent(self, openai_api_key):
        """Cria o agente LangChain para análise dos dados"""
        try:
            # Configurar LLM
            llm = ChatOpenAI(
                temperature=0.1,
                model_name="gpt-4o-mini",
                openai_api_key=openai_api_key
            )
            
            # Criar agente para análise dos DataFrames
            self.agent = create_pandas_dataframe_agent(
                llm,
                [self.df_cabecalho, self.df_itens],
                verbose=True,
                agent_type=AgentType.OPENAI_FUNCTIONS,
                allow_dangerous_code=True
            )
            
            return True
            
        except Exception as e:
            st.error(f"Erro ao criar agente: {str(e)}")
            return False
    
    def query_agent(self, question):
        """Faz pergunta ao agente"""
        try:
            if not self.agent:
                return "Agente não foi inicializado."
            
            # Contextualizar a pergunta
            context = f"""
            Você tem acesso a dois DataFrames:
            1. df_cabecalho: Contém os cabeçalhos de 100 notas fiscais (índice 0)
            2. df_itens: Contém os itens das notas fiscais (índice 1)
            
            Colunas do cabeçalho: {list(self.df_cabecalho.columns)}
            Colunas dos itens: {list(self.df_itens.columns)}
            
            DataFrame df_cabecalho: {self.df_cabecalho}
            DataFrame df_itens: {self.df_itens}
            Você pode usar esses dados para responder perguntas sobre as notas fiscais.
            
            Pergunta: {question}
            
            Por favor, analise os dados e forneça uma resposta detalhada.
            """
            
            response = self.agent.run(context)
            return response
            
        except Exception as e:
            return f"Erro ao processar pergunta: {str(e)}"

def main():
    st.title("🤖 Agente de Análise de Notas Fiscais")
    st.markdown("---")
    
    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Input para API Key da OpenAI
        openai_api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Insira sua chave API da OpenAI"
        )
        
        st.markdown("---")
        st.header("📁 Upload de Arquivo")
        
        # Upload do arquivo ZIP
        uploaded_file = st.file_uploader(
            "Selecione o arquivo 202401_NFs.zip",
            type=['zip'],
            help="Faça upload do arquivo ZIP contendo os CSVs das notas fiscais"
        )
    
    # Inicializar agente
    if 'agent' not in st.session_state:
        st.session_state.agent = NotasFiscaisAgent()
    
    # Processar arquivo uploadado
    if uploaded_file and openai_api_key:
        if not st.session_state.agent.data_loaded:
            with st.spinner("Extraindo e carregando dados..."):
                # Extrair ZIP
                file_paths, temp_dir = st.session_state.agent.extract_zip_file(uploaded_file)
                
                if file_paths:
                    # Carregar CSVs
                    if st.session_state.agent.load_csv_files(file_paths):
                        # Criar agente
                        if st.session_state.agent.create_agent(openai_api_key):
                            st.success("✅ Dados carregados e agente inicializado com sucesso!")
                        else:
                            st.error("❌ Erro ao inicializar agente")
                    else:
                        st.error("❌ Erro ao carregar dados")
    
    # Interface principal
    if st.session_state.agent.data_loaded:
        # Mostrar informações dos dados
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Dados do Cabeçalho")
            st.info(f"**Registros:** {len(st.session_state.agent.df_cabecalho)}")
            st.info(f"**Colunas:** {len(st.session_state.agent.df_cabecalho.columns)}")
            
            with st.expander("Ver colunas do cabeçalho"):
                st.write(list(st.session_state.agent.df_cabecalho.columns))
        
        with col2:
            st.subheader("📦 Dados dos Itens")
            st.info(f"**Registros:** {len(st.session_state.agent.df_itens)}")
            st.info(f"**Colunas:** {len(st.session_state.agent.df_itens.columns)}")
            
            with st.expander("Ver colunas dos itens"):
                st.write(list(st.session_state.agent.df_itens.columns))
        
        st.markdown("---")
        
        # Seção de perguntas
        st.subheader("💬 Faça sua Pergunta")
        
        # Exemplos de perguntas
        st.markdown("**Exemplos de perguntas:**")
        examples = [
            "Qual é o valor total das notas fiscais?",
            "Quantas notas fiscais existem por fornecedor?",
            "Qual é o item mais caro nas notas fiscais?",
            "Mostre a distribuição de valores por mês",
            "Quais são os 5 maiores valores de nota fiscal?",
            "Qual é o fornecedor que teve maior montante recebido?",
            "Qual item teve maior volume entregue (em quantidade)?"
        ]
        
        for example in examples:
            if st.button(f"📝 {example}", key=example):
                st.session_state.current_question = example
        
        # Input de pergunta customizada
        user_question = st.text_area(
            "Ou digite sua pergunta personalizada:",
            value=st.session_state.get('current_question', ''),
            height=100,
            placeholder="Ex: Qual é a média de valores das notas fiscais por fornecedor?"
        )
        
        # Botão para processar pergunta
        if st.button("🚀 Processar Pergunta", type="primary"):
            if user_question.strip():
                with st.spinner("Analisando dados..."):
                    response = st.session_state.agent.query_agent(user_question)
                    
                    st.subheader("📊 Resposta do Agente")
                    st.write(response)
            else:
                st.warning("Por favor, digite uma pergunta.")
        
        # Seção de visualização dos dados
        st.markdown("---")
        st.subheader("👀 Visualização dos Dados")
        
        tab1, tab2 = st.tabs(["Cabeçalho", "Itens"])
        
        with tab1:
            st.dataframe(
                st.session_state.agent.df_cabecalho.head(10),
                use_container_width=True
            )
            
        with tab2:
            st.dataframe(
                st.session_state.agent.df_itens.head(10),
                use_container_width=True
            )
    
    else:
        # Instruções iniciais
        st.info("👆 Por favor, configure sua API Key da OpenAI e faça upload do arquivo ZIP na barra lateral.")
        
        st.markdown("""
        ### 📋 Como usar:
        
        1. **Configure a API Key**: Insira sua chave da OpenAI na barra lateral
        2. **Upload do arquivo**: Faça upload do arquivo `202401_NFs.zip`
        3. **Aguarde o processamento**: O sistema irá extrair e carregar os dados
        4. **Faça perguntas**: Use a interface para consultar os dados das notas fiscais
        
        ### 🔍 Tipos de perguntas que você pode fazer:
        
        - Análises estatísticas (médias, somas, contagens)
        - Filtros e agrupamentos por campos específicos
        - Identificação de valores máximos e mínimos
        - Análises temporais (se houver campos de data)
        - Comparações entre fornecedores ou produtos
        """)

if __name__ == "__main__":
    main()