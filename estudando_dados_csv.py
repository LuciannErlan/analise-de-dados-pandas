#Dicionário das variáveis utilizadas no dataset supermarket_sales1.csv
#Invoice ID = Número de identificação da fatura do recibo de venda gerado por computador
#Branch = Filial do supercentro (estão disponíveis 3 filiais identificadas por A, B e C).
#City = Localização de supercentros
#Customer type = Tipo de clientes, registrados por Associados para clientes com cartão de sócio e Normal e para cliente sem cartão de sócio.
#Gender = Gênero do cliente
#Product line = Grupos de categorização geral de itens - Acessórios eletrônicos, Acessórios de moda, Alimentos e bebidas, Saúde e beleza, Casa e estilo de vida, Esportes e viagens
#Unit price = Preço de cada produto
#Quantity = Número de produtos comprados pelo cliente
#Tax 5% = Taxa de imposto de 5% para a compra do cliente
#Total = Preço total incluindo impostos
#Date = Data de compra (Registro disponível de janeiro de 2019 a março de 2019)
#Time = Horário de compra (10h às 21h)
#Payment = Pagamento usado pelo cliente para compra (3 métodos estão disponíveis – Dinheiro, Cartão de Crédito e Ewallet)
#cogs = Custo dos bens vendidos
#gross margin percentage = Porcentagem de margem bruta
#gross income = Renda bruta
#Rating = Classificação da estratificação do cliente em sua experiência geral de compra (numa escala de 1 a 10)


# Importando biblioteca
import pandas as pd

# Lendo a base de dados
df = pd.read_csv("Base_de_dados_Aula2ateAula7/supermarket_sales1.csv", sep=";", parse_dates=["Date"])
print(df.head())

print(df.info())

# Alterando o tipo de dado de uma coluna
#Trasnformando coluna de data em tipo Data
#df["Date"] = pd.to_datetime(df["Date"])

# Value Counts - Contagem de valores
# Total vendas por cidade
print(df["City"].value_counts())

# Total vendas por Gênero
print(df["Gender"].value_counts())

print(df.nlargest(10, "Quantity"))

print(df.nsmallest(10, "Quantity"))

print(df.sort_values(by="Quantity", ascending=False))

# Filtrando pelo gênero Female
df_female = df[df["Gender"] == "Female"]
print(df_female.shape)

print(df_female.groupby("Product line")["Quantity"].sum().sort_values(ascending=False))

df_male = df.loc[df["Gender"] == "Male"]
print(df_male.shape)

df_male.groupby("Product line")["Quantity"].sum().sort_values(ascending=False)
print(df_male.groupby("Product line")["Quantity"].sum().sort_values(ascending=False))


df.loc[(df["Gender"] != "Female") & (df["City"] == "Yangon")]
print(df.loc[(df["Gender"] != "Female") & (df["City"] == "Yangon")].shape)

df.loc[(df["Gender"] != "Female") | (df["City"] == "Yangon")]
print(df.loc[(df["Gender"] != "Female") | (df["City"] == "Yangon")].shape)

# isin
lista = ["A", "B"]
df[~df["Branch"].isin(lista)]
print(df.shape)

#df["Branch"].isin(lista)
df["Venda sem taxa"] = df["Unit price"] * df["Quantity"]
print(df.head(5))

# Informando onde vai inserir a coluna
df.insert(8, "Venda s/ Taxa", df["Unit price"] * df["Quantity"])
print(df.head(5))

# Renomeando colunas do DataFrame
df.rename(columns={"Venda s/ Taxa":"Receita"}, inplace=True)
print(df.head(5))

# Removendo colunas do DataFrame
df.drop(columns=["Receita", "Venda sem taxa"], inplace=True)
print(df.head(5))

def corrige_numero(coluna):
    if len(coluna) > 8:
        coluna = coluna.replace(".", "")
        coluna = coluna[0:3] + "." + coluna[3:]
        return coluna
    else:
        return coluna

df["Total"] = df["Total"].apply(corrige_numero)
print(df.head(5))

# Alterando o tipo de dado de uma coluna para float
df["Total"] = df["Total"].astype(float)
print(df.dtypes)

# Total de vendas por filial (Branch)
print(df.groupby("Branch")["Total"].sum().sort_values(ascending=False))