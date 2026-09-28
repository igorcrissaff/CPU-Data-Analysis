# 1. Carregar os dados
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuração da fonte de dados
fonte = "desktop" # desktop, notebook

df = pd.read_csv(f"{fonte}-data.CSV", encoding="latin-1" if fonte == "desktop" else "utf-8")

df.head()

# 2. Identificar as colunas de temperatura
if fonte == "desktop":
    colunas_temperatura = [
        "Core0 (Die1) [°C]",
        #"Core1 (Die1) [°C]",
        "Core2 (Die1) [°C]",
        "Core3 (Die1) [°C]",
        "Core4 (Die1) [°C]",
        #"Core5 (Die1) [°C]",
        "Core6 (Die1) [°C]",
        "Core7 (Die1) [°C]"
    ]
else:
    colunas_temperatura = [
        "P-core 0 [°C]",
        "P-core 1 [°C]",
        "E-core 2 [°C]",
        "E-core 3 [°C]",
        "E-core 4 [°C]",
        "E-core 5 [°C]",
        "E-core 6 [°C]",
        "E-core 7 [°C]",
        "E-core 8 [°C]",
        "E-core 9 [°C]"
    ]
temperaturas = df[colunas_temperatura].apply(
    pd.to_numeric,
    errors="coerce"
)

# 3. Criar uma coluna de tempo
df["datetime"] = pd.to_datetime(
    df["Date"] + " " + df["Time"],
    dayfirst=True,
    errors="coerce"
)


# 4. Mapa de calor
fig, ax = plt.subplots(figsize=(16, 8))

im = ax.imshow(
    temperaturas.T,
    aspect="auto",
    interpolation="nearest"
)

cbar = fig.colorbar(im, ax=ax)
cbar.set_label("Temperatura (°C)")

# Seleciona aproximadamente 10 marcações no eixo do tempo
n_ticks = 20
indices = np.linspace(
    0,
    len(df) - 1,
    n_ticks,
    dtype=int
)

ax.set_xticks(indices)
ax.set_xticklabels(
    df["datetime"].iloc[indices].dt.strftime("%H:%M:%S"),
    rotation=90
)

ax.set_yticks(range(len(colunas_temperatura)))
ax.set_yticklabels([
    colunas_temperatura[i].replace(" [°C]", "") for i in range(len(colunas_temperatura))
])

ax.set_xlabel("Tempo")
ax.set_ylabel("Núcleo")
ax.set_title("Mapa de calor da temperatura dos núcleos do CPU")

plt.tight_layout()
plt.show()