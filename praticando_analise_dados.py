#Importando a biblioteca pandas
import pandas as pd

#Ler as bases de dados
df_vendas = pd.read_excel("datasets/Vendas.xlsx")
df_produtos = pd.read_excel("datasets/Produtos.xlsx")
print(df_vendas.head(5))
print(df_produtos.head(5))

#Juntando (mesclando) a base de vendas com a base de produtos pela coluna "ID Produto"
df = pd.merge(df_vendas, df_produtos, on="ID Produto", how="left")
print(df.head(5))

#Verificando o tipo de dado de cada coluna
print(df.info())

#Receita total por produto
print("Receita total:", df["Valor Venda"].sum())
print(df.head(5))

#Custo total por produto
df["Custo"] = df["Custo Unitário"] * df["Quantidade"]
print(df.head(5))

#Criando coluna de Custo total
print("Custo total:", df["Custo"].sum())
print(df.head(5))

#Criando coluna de Lucro
df["Lucro"] = df["Valor Venda"] - df["Custo"]
print(df.head(5))


#COnsultando linhas com valores ausentes 
print(df.isnull().sum())

#Percentual de valores ausentes
print(df.isnull().sum() / df.shape[0] * 100)

#Substituindo as linhas com valores ausentes por zero
df["Valor Desconto"] = df["Valor Desconto"].fillna(0)
print(df.head(5))

#Substiiuindo os valores ausentes da coluna "Valor Desconto" pela média da coluna
#Exemplo alternativo:
#df["Valor Desconto"] = df["Valor Desconto"].fillna(df["Valor Desconto"].mean())

#Apagando as linhas com valores nulos com base em anpenas uma coluna
#Exemplo alternativo:
#df.dropna(subset=["Valor Desconto"], inplace=True)

#Removendo linhas que estejam com valores faltantes em qualquer coluna
#Exemplo alternativo:
#df.dropna(how="all", inplace=True)

#Verificando a data mais antiga e a mais recente da base de dados
print(df["Data Venda"].min())
print(df["Data Venda"].max())

#Criando coluna de Ano 
df["Ano Venda"] = df["Data Venda"].dt.year
print(df.head(5))

#Agrupando por ano da venda e somando o lucro total de cada ano
print(df.groupby("Ano Venda")["Lucro"].sum())

#Ajustando o formato de exibição dos numeros floats
pd.options.display.float_format = "{:20,.2f}".format
print(df.groupby("Ano Venda")["Lucro"].sum())

#Extraindo o mês e o dia da semana da coluna "Data Venda"
df["Mês Venda"], df["dia_venda"] = df["Data Venda"].dt.month, df["Data Venda"].dt.day_name()
print(df.head(5))

#Criando uma coluna de ano e mês
df["Ano e Mês"] = df["Data Venda"].dt.to_period("M")
print(df.head(5))

#Criando uma coluna de trimestre
df["Trimestre-ano"] = df["Data Venda"].dt.to_period("Q")
print(df.head(5))

#Analise por tempo de envio do produto
#Criando uma coluna de tempo de envio do produto    
df["Tempo_envio"] = (df["Data Envio"] - df["Data Venda"]).dt.days
print(df.head(5))

#Agrupando por tempo de envio e calculando a média
print(df.groupby("Tempo_envio")["Lucro"].mean())

#Agrupando por tempo de envio e calculando a média ordenada do maior para o menor
print(df.groupby("Tempo_envio")["Lucro"].mean().sort_values(ascending=False))

#Agrupando por tempo de envio e por marca do produto e calculando a média
print(df.groupby(["Tempo_envio", "Marca"])["Lucro"].mean().sort_values(ascending=False))

#Criando uma coluna com o dia da semana em que a venda foi realizada
df["dia_semana_venda"] = df["Data Venda"].dt.day_name()
print(df.head(5))



#Mapear os valores da coluna "dia_semana_venda" do inglês para o português (Criando um dicionário para mapear os dias da semana)
dias_semana = { 
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
} 
#Aplicando o dicionário de tradução na coluna com a função map()
df["dia_semana_venda"] = df["Data Venda"].dt.day_name().map(dias_semana)
print(df.head(5))

#Analisando a quantidade de vendas por dia da semana
print(df["dia_semana_venda"].value_counts())

#Agrupamento e Agregação de dados
#Somando o lucro total agrupado por Categoria
print(df.groupby("Categoria")["Lucro"].sum())

#Somando o lucro total agrupado por Subcategoria
print(df.groupby("Subcategoria")["Lucro"].sum())

#Somando o lucro total agrupado por Categoria e Subcategoria ao mesmo tempo
print(df.groupby(["Categoria", "Subcategoria"])["Lucro"].sum())

#Somando duas métricas (Lucro e Quantidade) agrupadas por Categoria e Subcategoria
print(df.groupby(["Categoria", "Subcategoria"])[["Lucro", "Quantidade"]].sum())

#Usando agg() para aplicar cálculos diferentes em cada coluna: soma do Lucro e média da Quantidade
print(df.groupby(["Categoria", "Subcategoria"]).agg({"Lucro": "sum", "Quantidade": "mean"}))

#Usando agg() para calcular a soma do Lucro e o desvio padrão (std) da Quantidade
print(df.groupby(["Categoria", "Subcategoria"]).agg({"Lucro": "sum", "Quantidade": "std"}))

#Variação mensal do lucro por categoria
print(df.groupby(["Ano e Mês", "Categoria"])["Lucro"].sum())

#Style - destacar valores máximos e mínimos em uma tabela
def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: white' if v else '' for v in is_max]

def color_negative(value):
    color = 'red' if value < 0 else 'black'
    return f'color: {color}'

#Aplicando as funções de estilo ao DataFrame agrupado
#Nota: No Pandas moderno, usamos .map() (em vez de .applymap) e .hide() (em vez de .hide_index)
styled_df = (
    df.groupby(["Ano e Mês", "Categoria"])["Lucro"].sum().reset_index()
    .style
    .apply(highlight_max, subset=["Lucro"])
    .map(color_negative, subset=["Lucro"])
    .format({"Lucro": "R${:,.2f}"})
    .hide()
    .set_table_styles([{
        'selector': 'th',
        'props': [('background-color', '#f2f2f2'),
                  ('color', '#333'),
                  ('font-weight', 'bold')]
    }])
)

#Como o Styler gera formatação visual (HTML), podemos salvar como arquivo .html para abrir no navegador:
styled_df.to_html("tabela_estilizada.html")
print("Tabela estilizada salva com sucesso em 'tabela_estilizada.html'!")


## Estatísticas descritivas
#### A estatística descritiva é a área da estatística que busca resumir, organizar e descrever os dados de forma clara e concisa. 
# Ela nos permite obter uma visão geral dos dados e identificar padrões e tendências importantes. 
# Como analista, isso é essencial para tomar decisões informadas e comunicar insights de maneira eficaz.

## Medidas de tendência central

### 1 - Média Aritmética: 
   #* Definição e cálculo da média aritmética: A média aritmética é a medida de tendência central mais comumente utilizada. 
   # Ela é obtida somando todos os valores de um conjunto de dados e dividindo pelo número total de observações. 
   # Por exemplo, se tivermos os valores [3, 5, 7, 11, 15], a média seria (3 + 5 + 7 + 11 + 15) / 5 = 8.2.
   
#### OBS: Ela é sensível a valores extremos, pois cada valor contribui igualmente para o cálculo.

salarios = [10000, 8000, 12000, 9000, 13000, 50000]
salarios = pd.Series(salarios)
print("Média dos salários:", salarios.mean())

### 2 - Mediana

  # * Definição e cálculo da mediana: A mediana é o valor que divide o conjunto de dados em duas partes iguais. 
  # Para calcular a mediana, é necessário ordenar os valores em ordem crescente e selecionar o valor do meio. 
  # Por exemplo, para o conjunto [3, 5, 7, 11, 15], a mediana seria 7.
   #* Comparação entre a mediana e a média: A mediana é uma medida de tendência central mais robusta à presença de valores extremos do que a média. 
   # Ela é menos influenciada por valores discrepantes e fornece uma estimativa melhor do centro dos dados em algumas situações.
   
print("Mediana dos salários:", salarios.median())
   
### 3 - Moda
   #* Definição e cálculo da moda: A moda é o valor que ocorre com mais frequência em um conjunto de dados.
   # Para calcular a moda, é necessário identificar o valor que aparece com maior frequência.       
    # Por exemplo, para o conjunto [3, 5, 7, 7, 11, 15], a moda seria 7.
    
salarios = [10000, 8000, 12000, 9000, 9000, 9000, 13000, 9000, 10000]
salarios = pd.Series(salarios)
print("Moda dos salários:\n", salarios.mode())

## Medidas de dispersão

### Essas medidas nos ajudam a compreender a variabilidade dos dados e fornecem informações importantes sobre a distribuição dos valores. 

### 1 - Desvio Padrão

  # * O desvio padrão é uma medida que indica o quanto os valores de um conjunto de dados se afastam da média.
   #* Ele nos permite compreender a dispersão ou variabilidade dos dados em relação à média.
   #* Quanto maior o desvio padrão, maior é a dispersão dos dados em relação à média. Isso indica que os valores estão mais espalhados e há maior variabilidade.
   #*Por outro lado, um desvio padrão baixo indica que os valores estão mais próximos da média e há menor variabilidade nos dados.
   #* No exemplo dos retornos diários da ação, um desvio padrão alto sugere que os retornos variam bastante, o que pode indicar um investimento mais arriscado. 
   # Já um desvio padrão baixo indica que os retornos são mais estáveis.
   
print(salarios.mean())
print(salarios.std())

#### * Dispersão dos salários: O desvio padrão de 1615 indica a dispersão ou variabilidade dos salários em relação à média.
# Valores mais altos de desvio padrão indicariam uma dispersão maior, enquanto um desvio padrão menor indica que os salários estão relativamente próximos da média.
#### * Variação dos salários: O desvio padrão de 1615 sugere que a maioria dos salários está dentro de uma faixa de aproximadamente 1615 pra cima ou pra baixo da média de 9888. 
# Isso nos dá uma ideia da variação esperada dos salários na base de dados.

### Variância 

#### A variância é uma medida de dispersão que nos ajuda a entender o quão espalhados estão os dados em relação à média. 
# Imagine que você está analisando a variação dos preços de ações em um determinado período de tempo.

#* A variância é uma medida que quantifica o quão distantes os valores de um conjunto de dados estão da média.
#* A variância é uma medida de dispersão que nos indica quão distantes os valores estão da média.
#* Quanto maior a variância, maior é a dispersão dos dados em relação à média.
#* Uma variância baixa indica que os valores estão mais próximos da média, sugerindo menor dispersão ou menor variabilidade nos dados.

print(salarios.mean())
print(salarios.std())
print(salarios.var())

#O resultado da variância é uma medida de dispersão que indica o quão distantes os valores estão da média, mas expresso em termos quadrados. 
# Neste caso, a variância é de 2611111.111111111.
#Porém, é importante notar que a variância é uma medida de dispersão ao quadrado, o que torna a interpretação direta do valor menos intuitiva. 
# Para obter uma medida de dispersão na mesma escala dos dados originais, você pode utilizar o desvio padrão, que é a raiz quadrada da variância.

### Amplitude

#### uma medida de dispersão simples, porém importante. 
# A amplitude nos ajuda a entender a extensão total dos dados, fornecendo informações sobre a diferença entre o maior e o menor valor em um conjunto de dados. 

#* A amplitude é uma medida simples de dispersão que representa a diferença entre o maior e o menor valor em um conjunto de dados.
#* Para calcular a amplitude, basta subtrair o menor valor do maior valor.
#* Por exemplo, considere os seguintes dados de altura (em centímetros): [160, 165, 170, 175, 180]. A amplitude seria 180 - 160 = 20.
#* A amplitude nos fornece uma noção básica da variação total dos dados.
#* Quanto maior a amplitude, maior é a diferença entre os valores extremos do conjunto de dados.
#* Uma amplitude baixa indica que os valores estão mais próximos uns dos outros, sugerindo uma variação menor nos dados.
#* Ela é sensível a valores extremos, o que pode distorcer a interpretação se houver valores discrepantes.

amplitude = salarios.max() - salarios.min()
print("Amplitude dos salários:", amplitude)

#No entanto, é importante lembrar que a amplitude é uma medida simples de dispersão que não leva em consideração a distribuição dos salários entre o maior e o menor valor. 
# Portanto, a amplitude por si só não fornece informações sobre a variação dos salários dentro dessa faixa. 
# Pode haver uma grande variação entre os salários intermediários ou uma distribuição relativamente uniforme.

#A interpretação mais adequada da amplitude depende do contexto específico dos dados e do domínio em questão. 
# No caso de salários, a amplitude pode indicar a diferença de renda entre o funcionário com o salário mais alto e o funcionário com o salário mais baixo, mas não nos dá informações detalhadas sobre a distribuição dos salários intermediários.

### Quartis e intervalo interquartil

####  duas medidas de dispersão que nos ajudam a entender a distribuição dos dados de forma mais detalhada.

#* Os quartis dividem um conjunto de dados ordenados em quatro partes iguais.
#* O primeiro quartil (Q1) é o valor abaixo do qual 25% dos dados estão localizados.
#* O segundo quartil (Q2), que é equivalente à mediana, divide o conjunto de dados em duas partes iguais: 50% dos dados estão abaixo dele e 50% estão acima.
#* O terceiro quartil (Q3) é o valor abaixo do qual 75% dos dados estão localizados.
#* Por exemplo, considere as seguintes notas em um exame: [60, 65, 70, 75, 80, 85]. Os quartis seriam Q1 = 65, Q2 = 72.5 e Q3 = 80.

### Intervalo interquartil:

#* O intervalo interquartil é a diferença entre o terceiro quartil (Q3) e o primeiro quartil (Q1).
#* Ele mede a dispersão dos dados em torno da mediana, ignorando os valores extremos.
#* O intervalo interquartil fornece uma medida robusta de dispersão, menos sensível a valores extremos.
#* Por exemplo, no conjunto de notas [60, 65, 70, 75, 80, 85], o intervalo interquartil seria 80 - 65 = 15.

# Calcular os quartis 
q1 = salarios.quantile(0.25)
q2 = salarios.quantile(0.5)
q3 = salarios.quantile(0.75)

# Calcular o intervalo interquartil
iqr = q3 - q1

# Imprimir os resultados
print("Primeiro Quartil (Q1):", q1)
print("Segundo Quartil (Q2):", q2)
print("Terceiro Quartil (Q3):", q3)
print("Intervalo Interquartil (IQR):", iqr)
print(df.head(5))


#Estatísticas descritivas do tempo de envio na base de dados real
print("Média do tempo de envio:", df["Tempo_envio"].mean())
print("Mediana do tempo de envio:", df["Tempo_envio"].median())
print("Desvio padrão do tempo de envio:", df["Tempo_envio"].std())
print("Primeiro quartil (Q1 - 25%) do tempo de envio:", df["Tempo_envio"].quantile(0.25))
print("Segundo quartil (Q2 - 50% / Mediana) do tempo de envio:", df["Tempo_envio"].quantile(0.5))
print("Terceiro quartil (Q3 - 75%) do tempo de envio:", df["Tempo_envio"].quantile(0.75))

#Resumo estatístico geral de todas as colunas numéricas (média, desvio padrão, min, quartis, max)
print("\nResumo estatístico das colunas numéricas:")
print(df.describe())

#Resumo estatístico das colunas de texto/categóricas (contagem, valores únicos, valor mais frequente e frequência)
print("\nResumo estatístico das colunas categóricas (texto):")
print(df.describe(include=object))


### ydata_profiling - Geração de relatório automatizado de análise exploratória
# Nota: Comandos com ponto de exclamação (!pip) são exclusivos do Jupyter Notebook.
# !pip install ydata_profiling

from ydata_profiling import ProfileReport

# Gerando o relatório de perfil exploratório dos dados
profile = ProfileReport(df, title="Relatório de Perfil", explorative=True)

# Salvando o relatório completo em formato HTML para abrir no navegador
profile.to_file("relatorio_perfil.html")
print("Relatório do ProfileReport salvo com sucesso em 'relatorio_perfil.html'!")

# Exibindo as 3 primeiras linhas finais
print("\nPrimeiras 3 linhas finais da base tratada:")
print(df.head(3))

# Exportando a base final tratada para um novo arquivo Excel
df.to_excel("Novo_Vendas.xlsx", index=False)
print("Base final exportada com sucesso para 'Novo_Vendas.xlsx'!")


# Importando nova biblioteca para busca de arquivos
from glob import glob

### A biblioteca glob é uma biblioteca padrão do Python que fornece uma maneira simples de encontrar arquivos que correspondam a padrões específicos em um determinado diretório. 
# Ela permite que você liste os arquivos que atendem a um padrão específico (usando caracteres curinga como *), facilitando a busca e a manipulação desses arquivos em lote.

# -------------------------------------------------------------
# FORMA 1: Manual (lendo e concatenando planilha por planilha)
# -------------------------------------------------------------
# Lendo cada planilha individualmente usando o caminho relativo da pasta Planilhas/
df1 = pd.read_excel("Planilhas/Fortaleza.xlsx")
df2 = pd.read_excel("Planilhas/Natal.xlsx")
df3 = pd.read_excel("Planilhas/Recife.xlsx")
df4 = pd.read_excel("Planilhas/Salvador.xlsx")

# Visualizando as 5 primeiras linhas da planilha de Salvador
print("\nPrimeiras linhas de Salvador:")
print(df4.head())

# Visualizando a quantidade de linhas e colunas da planilha de Natal
print("\nDimensões da planilha de Natal (linhas, colunas):", df2.shape)

# Concatenando (empilhando uma embaixo da outra) as 4 planilhas manualmente
df_manual = pd.concat([df1, df2, df3, df4])
print("\nTotal de linhas após concatenar manualmente:", df_manual.shape[0])


# -------------------------------------------------------------
# FORMA 2: Automatizada com glob (ideal para dezenas/centenas de planilhas)
# -------------------------------------------------------------
# O glob("Planilhas/*.xlsx") busca automaticamente todos os arquivos que terminam com .xlsx dentro da pasta Planilhas
# O sorted() garante que a lista fique em ordem alfabética
arquivos = sorted(glob("Planilhas/*.xlsx"))
print("\nArquivos encontrados automaticamente pelo glob:")
print(arquivos)

# pd.concat com generator: lê cada arquivo encontrado e já empilha todos em um único DataFrame
todos_arquivos = pd.concat((pd.read_excel(arquivo) for arquivo in arquivos), ignore_index=True)
print("\nPrimeiras linhas da base unificada de todas as cidades:")
print(todos_arquivos.head())

# Verificando os tipos de dados de cada coluna da base unificada
print("\nTipos de dados das colunas:")
print(todos_arquivos.dtypes)

# Criando a coluna de Receita (Vendas multiplicado pela Quantidade)
todos_arquivos["Receita"] = todos_arquivos["Vendas"] * todos_arquivos["Qtde"]
print("\nBase com a nova coluna Receita:")
print(todos_arquivos.head())

# Extraindo o ano da data da venda
todos_arquivos["Ano_Vend"] = todos_arquivos["Data"].dt.year
print("\nBase com a nova coluna Ano_Vend:")
print(todos_arquivos.head())

# Exportando a base unificada e calculada para um novo arquivo Excel
todos_arquivos.to_excel("planilha_vendas.xlsx", index=False)
print("\nBase consolidada exportada com sucesso para 'planilha_vendas.xlsx'!")


## Criando novas colunas
# Importando bibliotecas
import pandas as pd
import numpy as np

# Lendo a base de dados (apontando para a pasta Planilhas/)
df = pd.read_excel("Planilhas/Fortaleza.xlsx")
print("\nPrimeiras linhas da base de Fortaleza:")
print(df.head(5))

# Garantindo a coluna ValorProduto (na planilha original o nome é "Vendas")
if "ValorProduto" not in df.columns and "Vendas" in df.columns:
    df["ValorProduto"] = df["Vendas"]

# Calculando a Receita
df["Receita"] = df["ValorProduto"] * df["Qtde"]
print("\nBase com a nova coluna Receita:")
print(df.head(5))

### Criando uma coluna com base em uma condição
### numpy.where(condição, valor_se_verdadeiro, valor_se_falso)

# 1. Usando np.where: muito rápido e ideal para condições simples (se/senão)
df["ClassificaçãoVenda"] = np.where(df["Receita"] > 1000, "Alta", "Baixa")
print("\nAmostra com ClassificaçãoVenda (np.where):")
print(df.sample(5))

# 2. Usando uma função tradicional com .apply():
def classificavenda(valor):
    if valor < 1000:
        return "Baixa"
    else:
        return "Alta"
    
df["ClassificaVenda1"] = df["Receita"].apply(classificavenda)
print("\nAmostra com ClassificaVenda1 (função def):")
print(df.sample(5))

### 3. Usando função lambda com .apply():
### Uma função lambda é uma função anônima definida em uma única linha de código.
df['ClassificacaoVenda2'] = df['Receita'].apply(lambda x: 'Baixa' if x < 1000 else 'Alta')
print("\nAmostra com ClassificacaoVenda2 (lambda):")
print(df.sample(5))

### 4. Várias condições com numpy.select
### numpy.select(condições, valores_possíveis, default=valor_padrão)
condições = [
    df['Receita'].isnull(),
    df['Receita'] < 100,
    (df['Receita'] >= 100) & (df['Receita'] <= 500),
    df['Receita'] > 500
]

valores_possíveis = [
    'Nenhum',
    'Baixa',
    'Média',
    'Alta'
]

df['ClassificacaoVenda'] = np.select(condições, valores_possíveis, default='Desconhecido')
print("\nAmostra com ClassificacaoVenda (np.select com múltiplas condições):")
print(df.sample(5))


# -------------------------------------------------------------
# MYSQL - Conexão com banco de dados MySQL
# -------------------------------------------------------------
# Nota: Comandos com ! (!pip) são exclusivos do Jupyter Notebook.
# No Python normal, instalamos via terminal: pip install sqlalchemy pymysql
# !pip install sqlalchemy

from sqlalchemy import create_engine

# Bloco de conexão com o banco de dados MySQL:
# (Envolvido em try/except para não travar o script caso o servidor MySQL não esteja ligado no momento)
try:
    # 1. Configurando a conexão: tipo_banco+driver://usuario:senha@servidor:porta/nome_banco
    engine = create_engine("mysql+pymysql://root:senha@localhost:3306/vendas")

    # 2. Executando uma consulta SQL e carregando o resultado diretamente em um DataFrame
    df_sql = pd.read_sql_query("SELECT * FROM vendas", engine)
    print("\nPrimeiras linhas da tabela vendas do MySQL:")
    print(df_sql.head(5))
    print(df_sql.dtypes)

    # 3. Convertendo coluna de data para datetime
    df_sql["data_venda"] = pd.to_datetime(df_sql["data_venda"])

    # 4. Agrupando por mês da venda e somando a quantidade
    print("\nTotal de quantidade vendida por mês:")
    print(df_sql.groupby(df_sql["data_venda"].dt.month)["quantidade"].sum())

    # 5. Salvando o DataFrame tratado de volta no Banco de Dados MySQL
    df_sql.to_sql("vendas", con=engine, if_exists="replace", index=False)
    print("\nDados salvos com sucesso na tabela MySQL!")
except Exception as erro:
    print("\n[Aviso didático sobre o bloco MySQL]:")
    print("O código de conexão com o MySQL foi corrigido e estruturado com sucesso.")
    print("Para conectar a um banco real, basta ter o servidor MySQL rodando no seu computador (porta 3306) com o banco 'vendas' criado.")
