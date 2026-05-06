import pandas as pd
import numpy as np

df = pd.read_csv('EV_Charging_Data.csv')

df = df.head(110)

total_linhas = len(df)
print(f"--- VERIFICAÇÃO DE REQUISITOS ---")
print(f"Total de observações encontradas: {total_linhas}")
if total_linhas >= 110:
    print("Requisito de pelo menos 100 observações: OK!")
else:
    print("AVISO: Sua base tem menos de 100 linhas. Adicione mais dados antes de enviar.")
print("-" * 33 + "\n")

# ==== Atividade 1 ====

df = df.rename(columns={
    "connectionTime_decimal": "hora_conexao",
    "chargingDuration": "duracao",
    "kWhDelivered": "energia_kwh",
    "dayIndicator": "dia"
})

# Qualitativas nominais
df["periodo"] = pd.cut(df["hora_conexao"], bins=[0, 6, 12, 18, 24],
                        labels=["Madrugada", "Manha", "Tarde", "Noite"])

df["dia_cat"] = df["dia"].astype(str)

# Qualitativas ordinais
df["prioridade"] = pd.cut(df["energia_kwh"],
                          bins=[0, 10, 30, 100],
                          labels=["Baixa", "Media", "Alta"])

df["nivel_duracao"] = pd.cut(df["duracao"],
                               bins=[0, 2, 5, 10, 100],
                               labels=["Muito curta", "Curta", "Media", "Longa"])

# Quantitativas discretas
df["energia_int"] = df["energia_kwh"].fillna(0).astype(int)
df["uso_dia"] = df.groupby("dia")["dia"].transform("count")

# Quantitativas contínuas
df["duracao_continua"] = df["duracao"]
df["energia_continua"] = df["energia_kwh"]


# ==== Atividade 2 - variável quantitativa discreta ====

freq_d = df["energia_int"].value_counts().sort_index()

print("FREQUÊNCIA — ENERGIA (DISCRETA)")
print(freq_d.head(10))

# insights
print("\n# 1: Maioria das sessões ocorre em baixos valores de kWh.")
print("# 2: Indica uso mais rápido e parcial dos carregadores.")


# ==== Atividade 2.B - variável quantitativa contínua ====

# Criando a tabela de distribuição de frequências por classes
df["faixa_duracao"] = pd.cut(df["duracao_continua"], bins=5)
freq_c = df["faixa_duracao"].value_counts().sort_index()

print("\nFREQUÊNCIA — DURAÇÃO (CONTÍNUA)")
print(freq_c)

# insights
print("\n# 1: Maioria das sessões é de curta duração.")
print("# 2: Poucas sessões longas, baixa demanda prolongada.")