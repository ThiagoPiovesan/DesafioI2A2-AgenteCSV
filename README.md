# 🤖 Agente de Análise de Notas Fiscais

Sistema inteligente para análise de dados de notas fiscais utilizando IA e frameworks avançados como LangChain e CrewAI.

## 📋 Descrição

Este projeto implementa um ou mais agentes autônomos que permitem aos usuários realizar perguntas sobre arquivos CSV de notas fiscais. O sistema processa automaticamente o arquivo `202401_NFs.zip` contendo:

- `202401_NFs_Cabecalho.csv`: Cabeçalhos de 100 notas fiscais
- `202401_NFs_Itens.csv`: Itens correspondentes das notas fiscais

## 🚀 Funcionalidades

### Capacidades do Sistema:
- ✅ **Descompactação automática** de arquivos ZIP
- ✅ **Carregamento inteligente** dos dados CSV
- ✅ **Processamento de consultas** em linguagem natural
- ✅ **Interface web intuitiva** com Streamlit
- ✅ **Análises estatísticas** avançadas
- ✅ **Visualização de dados** integrada

### Tipos de Consultas Suportadas:
- Análises estatísticas (médias, somas, contagens)
- Filtros e agrupamentos por campos específicos
- Identificação de valores máximos e mínimos
- Análises temporais (quando aplicável)
- Comparações entre fornecedores ou produtos

## 🛠️ Tecnologias Utilizadas

### Frameworks de IA:
- **LangChain**: Para criação de agentes inteligentes
- **CrewAI**: Para sistema multi-agente (versão alternativa)
- **OpenAI GPT**: Como modelo de linguagem principal

### Stack Técnico:
- **Python 3.8+**
- **Streamlit**: Interface web
- **Pandas**: Manipulação de dados
- **Plotly**: Visualizações interativas

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone <seu-repositório>
cd agente-notas-fiscais
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure a API Key da OpenAI
Obtenha sua chave API em: https://platform.openai.com

## 🚀 Como Usar

### Versão Principal (LangChain)
```bash
streamlit run main.py
```

### Versão Alternativa (CrewAI)
```bash
streamlit run crewai_version.py
```

### Passos de Uso:

1. **Acesse a interface web** (geralmente em `http://localhost:8501`)
2. **Insira sua OpenAI API Key** na barra lateral
3. **Faça upload do arquivo** `202401_NFs.zip`
4. **Aguarde o processamento** dos dados
5. **Faça suas perguntas** usando linguagem natural

## 💡 Exemplos de Uso

### Perguntas Básicas:
```
- "Qual é o valor total das notas fiscais?"
- "Quantas notas fiscais existem no arquivo?"
- "Quantos fornecedores únicos temos?"
```

### Análises Avançadas:
```
- "Mostre a distribuição de valores por fornecedor"
- "Qual é o item mais caro nas notas fiscais?"
- "Faça uma análise temporal dos dados"
- "Compare os valores médios por categoria"
```

### Consultas Específicas:
```
- "Liste os 5 maiores valores de nota fiscal"
- "Quais fornecedores têm mais de 10 notas fiscais?"
- "Calcule a média de valores por mês"
```

## 🏗️ Arquitetura do Sistema

### Componentes Principais:

1. **Interface Streamlit**
   - Upload de arquivos
   - Configuração de API Keys
   - Interface de consultas
   - Visualização de resultados

2. **Processador de Dados**
   - Extração de arquivos ZIP
   - Carregamento de CSVs
   - Processamento de datas
   - Validação de dados

3. **Agente de IA (LangChain)**
   - Análise de consultas em linguagem natural
   - Execução de operações nos DataFrames
   - Geração de respostas contextualizadas

4. **Sistema Multi-Agente (CrewAI)**
   - Analista de Dados Fiscais
   - Especialista em Consultas
   - Coordenação entre agentes

## 📊 Estrutura dos Dados

### Arquivo de Cabeçalho (202401_NFs_Cabecalho.csv):
- Informações principais das notas fiscais
- Dados do fornecedor
- Valores totais
- Datas de emissão

### Arquivo de Itens (202401_NFs_Itens.csv):
- Detalhes dos produtos/serviços
- Quantidades e valores unitários
- Descrições dos itens
- Códigos e classificações

### Formato dos Dados:
- **Separador**: Vírgula (,)
- **Decimal**: Ponto (.)
- **Datas**: AAAA-MM-DD HH:MM:SS
- **Encoding**: UTF-8

## 🔧 Configuração Avançada

### Variáveis de Ambiente:
```bash
# LINUX / MACOS:
export OPENAI_API_KEY=sk-xxxx

# WINDOWS (CMD):
set OPENAI_API_KEY=sk-xxxx

```

### Personalização do Agente:
```python
# Modificar temperatura do modelo
llm = ChatOpenAI(
    temperature=0.1,  # Mais determinístico
    model_name="gpt-4",  # Modelo mais avançado
    openai_api_key=openai_api_key
)
```

## 🐛 Solução de Problemas

### Problemas Comuns:

**Erro de API Key:**
```
Verifique se a chave está correta e tem créditos suficientes
```

**Erro de Upload:**
```
Certifique-se de que o arquivo é um ZIP válido
Verifique se contém os arquivos CSV esperados
```

**Erro de Processamento:**
```
Confirme se os CSVs têm o formato correto
Verifique a codificação dos arquivos (UTF-8)
```

**Problemas de Dependências:**
```bash
pip install --upgrade -r requirements.txt
```

## 📈 Métricas e Performance

### Capacidades:
- ✅ Suporta consultas complexas em < 30 segundos
- ✅ Interface responsiva e intuitiva
- ✅ Visualizações interativas em tempo real

### Limitações:
- Requer conexão com internet (API OpenAI)
- Limitado pelo contexto do modelo de IA
- Performance depende da complexidade da consulta
