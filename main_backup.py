
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dados = pd.read_csv(
    "jogadores_reais.csv",
    sep=";",
    encoding="cp1252"
)

print(" COLUNAS DISPONÍVEIS ")
print(dados.columns.tolist())

print(" PRIMEIROS JOGADORES ")
print(dados.head())

print(dados.columns.tolist())

print(" DESEMPENHO DOS JOGADORES ")
print(dados.to_string(index=False))

media_gols = np.mean(dados["Gols"])
print(f"\nMédia de gols por jogador: {media_gols:.2f}")

media_assistencias = np.mean(dados["Assistencias"])
print(f"Média de assistências: {media_assistencias:.2f}")

indice = dados["Gols"].idxmax()
artilheiro = dados.loc[indice]

print(" DESTAQUE EM GOLS")
print("Jogador:", artilheiro["Jogador"])
print("Clube:", artilheiro["Clube"])
print("Gols:", artilheiro["Gols"])

plt.figure(figsize=(10, 5))

plt.bar(dados["Jogador"], dados["Gols"])
plt.title("Quantidade de gols por jogador")
plt.xlabel("Jogadores")
plt.ylabel("Quantidade de gols")

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))

plt.bar(
    dados["Jogador"],
    dados["Assistencias"]
)
plt.title("Quantidade de assistências por jogador")
plt.xlabel("Jogadores")
plt.ylabel("Quantidade de assistências")

plt.tight_layout()
plt.show()


print("Gols:", artilheiro["Gols"])


dados["Gols_por_partida"] = (
    dados["Gols"] / dados["Partidas"]
).round(2)

print(" GOLS POR PARTIDA ")
print(
    dados[["Jogador", "Gols_por_partida"]]
    .to_string(index=False)
)

ranking = dados.sort_values(
    by="Gols",
    ascending=False
)

print("RANKING DE JOGADORES")
print(
    ranking[["Jogador", "Gols"]]
    .to_string(index=False)
)

plt.figure(figsize=(10, 5))

plt.bar(ranking["Jogador"], ranking["Gols"])
plt.title("Ranking de gols dos jogadores")
plt.xlabel("Jogadores")
plt.ylabel("Total de gols")
plt.tight_layout()
plt.show()

