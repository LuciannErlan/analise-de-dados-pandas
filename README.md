# 📊 Repositório de Análise de Dados com Python e Pandas

Este repositório contém os projetos, scripts e estudos práticos de Análise de Dados desenvolvidos durante o curso da **Fernanda Santos**.

---

## 🚀 Conteúdo do Repositório

### 1. [`estudando_dados_excel.py`](estudando_dados_excel.py)
* Leitura e manipulação de arquivos Excel (`.xlsx`).
* Análise de pedidos de vendas e produtos mais vendidos.
* Exploração estrutural da base (`head`, `tail`, `columns`, `dtypes`, `info`).

### 2. [`estudando_dados_csv.py`](estudando_dados_csv.py)
* Leitura de arquivos `.csv` com separadores personalizados e parsing de datas.
* Contagem de frequência (`value_counts`) e ordenações com `nlargest` e `nsmallest`.
* Filtros condicionais múltiplos (`&`, `|`, `~` e `isin`).
* Criação, inserção (`insert`), renomeação (`rename`) e remoção (`drop`) de colunas.
* Limpeza e conversão de strings numéricas para `float` com funções personalizadas.

### 3. [`praticando_analise_dados.py`](praticando_analise_dados.py)
* **Cruzamento de Bases:** União de tabelas relacionais com `pd.merge`.
* **Tratamento de Nulos:** Diagnóstico e tratamento de valores ausentes com `fillna` e `dropna`.
* **Análise Temporal:** Extração de Ano, Mês, Trimestre e tradução de dias da semana para português com dicionários e `.map()`.
* **Agrupamento e Agregação:** Uso avançado de `groupby` e `.agg()` com múltiplas métricas simultâneas.
* **Estilização Visual:** Formatação condicional de tabelas em HTML com Pandas Styler.
* **Estatística Descritiva:** Média, Mediana, Moda, Desvio Padrão, Variância, Amplitude e Intervalo Interquartil (IQR).
* **Análise Exploratória Automatizada:** Geração de relatórios com `ydata-profiling` (`ProfileReport`).
* **Automação de Arquivos em Lote:** Leitura e consolidação automática de múltiplas planilhas de filiais usando a biblioteca `glob`.
* **Engenharia de Recursos:** Criação de colunas com condições usando `np.where`, funções tradicionais, `lambda` e `np.select`.
* **Banco de Dados Relacional:** Integração e consultas em bancos MySQL com `SQLAlchemy`.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas
* **Python 3.11**
* **Pandas**
* **NumPy**
* **OpenPyXL**
* **Jinja2**
* **YData-Profiling**
* **SQLAlchemy & PyMySQL**
* **Glob**

---

## 💻 Como Executar os Scripts

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   ```

2. **Instale as dependências:**
   ```bash
   pip install pandas numpy openpyxl jinja2 ydata-profiling sqlalchemy pymysql
   ```

3. **Execute qualquer um dos scripts:**
   ```bash
   python praticando_analise_dados.py
   python estudando_dados_excel.py
   python estudando_dados_csv.py
   ```
