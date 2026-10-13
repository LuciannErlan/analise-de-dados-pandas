import pandas as pd

# Lendo a base de dados
df = pd.read_excel("Base_de_dados_Aula1/Vendas.xlsx")
print(df.head(5))

# Visualizando as 5 últimas linhas
print(df.tail(5))

# Retornando apenas os nomes das colunas
print(df.columns)

# Tipo de dado de cada coluna
print(df.dtypes)

print(df.info())

# Visualizando apenas uma coluna
print(df["Product"].head(20))

# Visualizando os valores únicos da coluna Product
print(df["Product"].unique())

print(df.groupby("Product")["Quantity Ordered"].sum().sort_values(ascending=False))