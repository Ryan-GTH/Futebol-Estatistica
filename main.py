
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


dados = pd.read_csv(
    "jogadores_reais.csv",
    sep=";",
    encoding="cp1252"
)


def corrigir_nome(nome):
    nome = str(nome)
    nome_minusculo = nome.lower()

    if "mbapp" in nome_minusculo:
        return "Kylian Mbappé"

    if "llkrug" in nome_minusculo:
        return "Niclas Füllkrug"

    return nome


dados["Player"] = dados["Player"].apply(corrigir_nome)


colunas_numericas = ["Goals", "Assists", "MP", "90s"]

for coluna in colunas_numericas:
    dados[coluna] = pd.to_numeric(
        dados[coluna],
        errors="coerce"
    )

dados = dados.dropna(subset=["Player", "Goals", "MP"])

dados = dados.sort_values(
    by="Goals",
    ascending=False
).head(30).copy()

dados["Assists_estimadas"] = (
    dados["Assists"] * dados["90s"]
).round()

dados["Gols_por_partida"] = (
    dados["Goals"] / dados["MP"].replace(0, np.nan)
).fillna(0)


media_gols = dados["Goals"].mean()
mediana_gols = dados["Goals"].median()
maior_numero_gols = dados["Goals"].max()
total_jogadores = len(dados)

artilheiro = dados.loc[dados["Goals"].idxmax()]


top_gols = dados.nlargest(10, "Goals").sort_values("Goals")

top_assistencias = dados.nlargest(
    10, "Assists_estimadas"
).sort_values("Assists_estimadas")

top_media = dados.nlargest(
    10, "Gols_por_partida"
).sort_values("Gols_por_partida")

gols_clubes = (
    dados.groupby("Squad")["Goals"]
    .sum()
    .nlargest(10)
    .sort_values()
)


print("\n======================================")
print(" ANÁLISE ESTATÍSTICA DO FUTEBOL")
print("======================================")

print("\n=== TABELA DOS 10 PRIMEIROS JOGADORES ===")

tabela = dados[
    ["Player", "Squad", "MP", "Goals",
     "Assists_estimadas", "Gols_por_partida"]
].head(10).copy()

tabela.columns = [
    "Jogador", "Clube", "Partidas",
    "Gols", "Assistências estimadas", "Gols por partida"
]

print(tabela.to_string(index=False))

print("\n=== ESTATÍSTICAS GERAIS ===")
print(f"Jogadores analisados: {total_jogadores}")
print(f"Média de gols: {media_gols:.2f}")
print(f"Mediana de gols: {mediana_gols:.2f}")
print(f"Maior número de gols: {maior_numero_gols:.0f}")
print(f"Menor número de gols: {dados['Goals'].min():.0f}")

print("\n=== DESTAQUE EM GOLS ===")
print("Jogador:", artilheiro["Player"])
print("Clube:", artilheiro["Squad"])
print("Gols:", int(artilheiro["Goals"]))


fig = plt.figure(
    figsize=(18, 15),
    facecolor="#F3F5F8"
)

fig.suptitle(
    "ANÁLISE ESTATÍSTICA DO DESEMPENHO DE JOGADORES",
    fontsize=19,
    fontweight="bold",
    color="#172B4D",
    y=0.985
)

fig.text(
    0.5, 0.935,
    "TEMPORADA 2022–2023 | ANÁLISE DOS 30 JOGADORES COM MAIS GOLS",
    ha="center",
    fontsize=10,
    color="#64748B"
)

grade = fig.add_gridspec(
    3, 2,
    height_ratios=[0.65, 2, 2],
    hspace=0.58,
    wspace=0.28,
    left=0.19,
    right=0.97,
    top=0.89,
    bottom=0.12
)


ax_indicadores = fig.add_subplot(grade[0, :])
ax_indicadores.axis("off")

indicadores = [
    ("JOGADORES", f"{total_jogadores}"),
    ("MÉDIA DE GOLS", f"{media_gols:.2f}"),
    ("MEDIANA DE GOLS", f"{mediana_gols:.1f}"),
    ("ARTILHEIRO", f"{artilheiro['Player']}")
]

posicoes = [0.125, 0.375, 0.625, 0.875]

for posicao, (titulo, valor) in zip(posicoes, indicadores):
    ax_indicadores.text(
        posicao, 0.5,
        f"{titulo}\n{valor}",
        transform=ax_indicadores.transAxes,
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="#172B4D",
        bbox=dict(
            boxstyle="round,pad=0.8",
            facecolor="white",
            edgecolor="#D9E1EC"
        )
    )

def configurar_grafico(ax, titulo, eixo_x):
    ax.set_title(
        titulo,
        fontsize=13,
        fontweight="bold",
        color="#172B4D",
        pad=13
    )

    ax.set_xlabel(eixo_x, fontsize=10)
    ax.set_facecolor("white")
    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.25
    )

    ax.set_axisbelow(True)

    for lado, borda in ax.spines.items():
        if lado in ["top", "right"]:
            borda.set_visible(False)
        else:
            borda.set_color("#CBD5E1")
            borda.set_linewidth(1)


    ax.tick_params(axis="both", labelsize=9)

ax1 = fig.add_subplot(grade[1, 0])

barras1 = ax1.barh(
    top_gols["Player"],
    top_gols["Goals"],
    color="#2878B5"
)

configurar_grafico(
    ax1,
    "TOP 10 JOGADORES POR GOLS",
    "Quantidade de gols"
)

ax1.bar_label(barras1, padding=4, fontsize=9)
ax1.set_xlim(0, top_gols["Goals"].max() * 1.15)


ax2 = fig.add_subplot(grade[1, 1])

barras2 = ax2.barh(
    top_assistencias["Player"],
    top_assistencias["Assists_estimadas"],
    color="#20A486"
)

configurar_grafico(
    ax2,
    "TOP 10 ASSISTÊNCIAS ESTIMADAS",
    "Assistências estimadas"
)

ax2.bar_label(barras2, padding=4, fontsize=9)


ax3 = fig.add_subplot(grade[2, 0])

barras3 = ax3.barh(
    top_media["Player"],
    top_media["Gols_por_partida"],
    color="#E6A23C"
)

configurar_grafico(
    ax3,
    "TOP 10 POR MÉDIA DE GOLS POR PARTIDA",
    "Gols por partida"
)

ax3.bar_label(
    barras3,
    fmt="%.2f",
    padding=4,
    fontsize=9
)

ax4 = fig.add_subplot(grade[2, 1])

barras4 = ax4.barh(
    gols_clubes.index,
    gols_clubes.values,
    color="#805AD5"
)

configurar_grafico(
    ax4,
    "TOP 10 CLUBES EM GOLS",
    "Gols dos jogadores selecionados"
)

ax4.bar_label(barras4, padding=4, fontsize=9)


fig.text(
    0.5, 0.035,
    "Fonte: base de dados de jogadores da temporada 2022–2023 | Elaboração própria em Python",
    ha="center",
    fontsize=9,
    color="#64748B"
)

plt.show()