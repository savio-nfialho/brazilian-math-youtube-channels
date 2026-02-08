"""# Parte 1: Extração e preparação dos dados dos canais via API do Youtube Data"""

# ------------------------------------------------------------
# PARTE 1 — COLETA / LEITURA
# ------------------------------------------------------------

# --- Imports ---
from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns; sns.set(style='white')
import numpy as np
import json
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime, timezone, timedelta
from dateutil import parser

# ----------------------------
# 1) CONFIG
# ----------------------------

api_key = "sua_chave"  # Substitua pela sua chave de API de verdade

requisitar_da_api = False  # True = buscar da API | False = ler CSV
csv_path = "brazilian-math-youtube-channels/data/raw/dados_canais_youtube.csv"

# Lista de IDs dos canais a serem analisados (usada apenas se fetch_from_api for True)
channel_ids = [
    "UCCTHtVMXy9gQA8X_HOEJA2A",
    "UCJX2x-WgMyk54OqwnPWGz2Q",
    "UCXBJ_Ef8qfYrwN5cY8W7ziA",
    "UCjIPRjJZtGhzWD2LrEKOHMA",
    "UC5Y3Kw7DCG6FTiC0Xx7sgfQ",
    "UCZLyNRqqp2MeFuwuZdbGDJw",
    "UCvMdTwY9FYB3cskV9f9djoQ",
    "UC-gOGJkGLl4FPHmu3DoNZpQ",
    "UCoB7wLA9hJ8-H4ss1KlR_JQ",
    "UCf8HI4bUyOOORoVRbeXwVLw",
    "UCUx-xXpbDOnd-7VQDioFq_Q",
    "UCqLLvE_v2ktQVFO_TnSQoTg",
    "UCKWhzq69oEmFOdAfjNQYKeg",
    "UCz5-HfBqc2WzfiI6PI5figA",
    "UCFpAlHLWnGaMoBP3QBEEsbQ",
    "UCGABb0CDdh9yv4M_w9tkW7g",
    "UCMUM7htFCzxSE4yvn1aQ2zg",
    "UCoKv7o7GFD188FcTbhsx15w",
    "UCw1x5GDOQsQ9yVrpTrKYxHg",
    "UCwnv0WmFneTIW76wULgFlcQ",
    "UC_UB3VlNDytQccGOa8tGljQ",
    "UCzs574vJvpTNc4Z9vaN5Wmg",
    "UC2ARrBxwEFyXhk-rkdrZx2w",
    "UC_2Pl-hyJkGrLz9NCAq2Knw",
    "UC1-Ym9T_Yn5y1sfPxppqKlQ",
    "UCyjCLZQIlXl1qTAJyUaPVTg",
    "UCido3v0CxXHg_vBAgpGHgkA",
    "UCN0XT4R0FZbFhVAHILYujxQ",
    "UCMYJXszXk5zlKgczRU_nZZA",
    "UCTVEAGIOrVsmq0mOWwvB_Og",
    "UCfDiNXDO5eb_Z3ew-dFhwHQ",
    "UCVngl-zszbWdMcRht9GVrnQ",
    "UCh5Vx4qBR2my3iryuYY2JKg",
    "UC6TTtp9Hdx7GUz0OjrVg1_Q",
    "UCh4wFjGWkFR6LpCfgXZv1eg",
    "UC5Y_eqLLV2oBTcbOyIAKmFg",
    "UCYAFWZxU8NIW4usayhANl5Q",
    "UCHcvG8rLz1NVHTFqvdkwatw",
    "UC16Iw9JWE6BMg2OKqLHeybQ",
    "UCLrpSGZxlnq6uQNNXRXXppw",
    "UCcQPFUfaQGFbElakEZa72Bw",
    "UCSPjiPET3XrnAmbWE5mzSnA",
    "UCwJn1Nb0nKcNIzGBx1Iq8Qw",
    "UCxkrv0Mvgc5GTi8xj0DhSTQ",
    "UCTcB5Wtk6gF0gBw4vvK2QeQ",
    "UC2eAnIEpGG5TPD--K6il96A",
    "UCu8lEv0rJy2VpMXeJAltlEA",
    "UCUsDa4Eo6ow-2fJfXReXfLQ",
    "UCW9_n8p_Byz-4k8wV1tnUBg",
    "UCkD_O6F2yt97117PhrBxqYA"
]

# ------------------------------------------------------------
# 2) FUNÇÕES — CANAIS
# ------------------------------------------------------------


def get_channel_stats(youtube, channel_ids):
    """
    Coleta estatísticas básicas dos canais a partir da API do YouTube.
    Retorna uma lista de dicionários com os dados.
    """
    all_data = []

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=",".join(channel_ids)  # passa a lista toda de uma vez
    )
    response = request.execute()

    for item in response["items"]:
        data = dict(
            Channel_id=item["id"],
            Created_at=item["snippet"]["publishedAt"],
            Channel_name=item["snippet"]["title"],
            Custom_url=item["snippet"].get("customUrl", ""),
            Subscribers=item["statistics"]["subscriberCount"],
            Views=item["statistics"]["viewCount"],
            Total_Videos=item["statistics"]["videoCount"],
            Playlist_id=item["contentDetails"]["relatedPlaylists"]["uploads"],
        )
        all_data.append(data)

    return all_data


# ------------------------------------------------------------
# 3) EXECUÇÃO — CARREGAR DADOS DOS CANAIS (API OU CSV)
# ------------------------------------------------------------
if requisitar_da_api and not api_key:
    raise ValueError("API key não definida")

elif requisitar_da_api:
    print("Buscando dados da API do YouTube...")
    youtube = build("youtube", "v3", developerKey=api_key)
    channel_stats = get_channel_stats(youtube, channel_ids)
    channel_data = pd.DataFrame(channel_stats)

else:
    print("Lendo dados do arquivo CSV local...")
    try:
        csv_path = "brazilian-math-youtube-channels/data/raw/dados_canais_youtube.csv"
        channel_data = pd.read_csv(csv_path)
        print("Dados lidos com sucesso!")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{csv_path}' não foi encontrado no GitHub indicado.")
        print("Por favor, verifique o caminho ou defina 'requisitar_da_api = True' para buscar da API.")
        raise


# ------------------------------------------------------------
# 4) TRATAMENTO - FORMATAÇÃO
# ------------------------------------------------------------

channel_data["Subscribers"] = pd.to_numeric(channel_data["Subscribers"])
channel_data["Views"] = pd.to_numeric(channel_data["Views"])
channel_data["Total_Videos"] = pd.to_numeric(channel_data["Total_Videos"])

# Garante que a coluna 'Created_at' está no formato datetime
channel_data["Created_at"] = pd.to_datetime(channel_data["Created_at"], format="ISO8601")

# Calcula idade do canal em anos (2 casas)
channel_data["Channel_age_years"] = round(
    (datetime.now(timezone.utc) - channel_data["Created_at"]).dt.days / 365.25,
    2
)

# Exibe o DataFrame para verificar se a leitura foi bem-sucedida
display(channel_data.head(3))


# ------------------------------------------------------------
# 5) FUNÇÕES — VÍDEOS (UPLOADS) + PARSE DURAÇÃO
# ------------------------------------------------------------

def get_video_details(youtube, video_ids):
    all_details = []

    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        request = youtube.videos().list(
            part="statistics,contentDetails",
            id=",".join(batch)
        )
        response = request.execute()

        for item in response.get("items", []):
            dur = item.get("contentDetails", {}).get("duration")  # ✅ aqui vem duração

            if parse_isoduration(dur) > 180:
                stats = item.get("statistics", {})
                all_details.append({
                    "Video_id": item["id"],
                    "Views": stats.get("viewCount", 0),
                    "Likes": stats.get("likeCount", 0),
                    "Comments": stats.get("commentCount", 0),
                    "Duration": dur,  # ✅ PT#M#S
                    "Duration_seconds": parse_isoduration(dur)  # ✅ número
                })

    return all_details


def get_isosplit(s, split):
    if split in s:
        n, s = s.split(split)
    else:
        n = 0
    return n, s


def parse_isoduration(s):
    """
    Converte duração ISO 8601 (ex.: 'PT5M30S') em segundos.
    Mantém a lógica original do seu código.
    """
    # Remove prefix
    s = s.split("P")[-1]

    # Step through letter dividers
    days, s = get_isosplit(s, "D")
    _, s = get_isosplit(s, "T")
    hours, s = get_isosplit(s, "H")
    minutes, s = get_isosplit(s, "M")
    seconds, s = get_isosplit(s, "S")

    # Convert all to seconds
    dt = timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    return int(dt.total_seconds())

"""# Parte 2: Cálculo do Índice de Performance"""

def calc_index_performance(subs, videos, views, age, md_subs, md_videos, md_views, md_age):
    """
    Calcula um índice de performance ponderado com base no produto entre inscritos,
    vídeos e visualizações, normalizado pelas respectivas medianas.
    """
    return (subs * videos * views * age) / (md_subs * md_videos * md_views * md_age)

# Calculando as medianas para normalização
md_subs = channel_data['Subscribers'].median()
md_videos = channel_data['Total_Videos'].median()
md_views = channel_data['Views'].median()
md_age = channel_data['Channel_age_years'].median()

# Calculando e aplicando log10 ao índice
channel_data['Index_Performance'] = calc_index_performance(
    channel_data['Subscribers'],
    channel_data['Total_Videos'],
    channel_data['Views'],
    channel_data['Channel_age_years'],
    md_subs, md_videos, md_views, md_age
)
channel_data['Index_Performance_log10'] = np.log10(channel_data['Index_Performance'])

"""# Parte 3: Gráficos e Estatística"""

# ----------------------------
# SEÇÃO 1: PREPARAÇÃO (BOXPLOT + CORR)
# ----------------------------

COLS_PT = {
    'Subscribers': 'Inscritos',
    'Views': 'Visualizações',
    'Total_Videos': 'Vídeos publicados',
    'Channel_age_years': 'Idade do canal (anos)',
    'Index_Performance_log10': 'Índice de performance'
}

df_boxplot_chann = channel_data[list(COLS_PT.keys())].rename(columns=COLS_PT)

channel_data_corr = channel_data[
    ['Subscribers', 'Views', 'Total_Videos', 'Channel_age_years', 'Index_Performance_log10']
].rename(columns={
    'Subscribers': 'Inscritos',
    'Views': 'Visualizações',
    'Total_Videos': 'Vídeos',
    'Channel_age_years': 'Idade do canal (anos)',
    'Index_Performance_log10': 'Índice de performance'
})


# ----------------------------
# HELPERS (não muda a lógica)
# ----------------------------

def format_quartil(feature_name: str, value: float) -> str:
    """Formatação dos quartis (mesma regra que você usou)."""
    if feature_name in ('Idade do canal (anos)', 'Índice de performance'):
        return f'{value:.2f}'
    return f'{value:.2e}'


def annotate_quartis(ax, series: pd.Series, feature_name: str):
    """Anota Q1/Q2/Q3 no canto do gráfico (mesmo posicionamento)."""
    Q1 = series.quantile(0.25)
    Q2 = series.quantile(0.50)
    Q3 = series.quantile(0.75)

    ax.text(1, 0.95, f'Q1: {format_quartil(feature_name, Q1)}',
            va='top', ha='right', transform=ax.transAxes, fontsize=8, color='black')
    ax.text(1, 0.85, f'Q2: {format_quartil(feature_name, Q2)}',
            va='top', ha='right', transform=ax.transAxes, fontsize=8, color='black')
    ax.text(1, 0.75, f'Q3: {format_quartil(feature_name, Q3)}',
            va='top', ha='right', transform=ax.transAxes, fontsize=8, color='black')


# ----------------------------
# SEÇÃO 2: BOXPLOTS
# ----------------------------

fig, axes = plt.subplots(3, 2, figsize=(14, 10))
axes = axes.flatten()
fig.delaxes(axes[-1])  # remove o subplot extra

for ax, feature in zip(axes[:5], df_boxplot_chann.columns):
    sns.boxplot(data=df_boxplot_chann, x=feature, ax=ax)

    ax.set_title(f'Boxplot {feature}')
    ax.xaxis.set_label_text(feature)
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)

    if feature == 'Visualizações':
        ax.ticklabel_format(style='sci', axis='x', scilimits=(6, 6))

    annotate_quartis(ax, df_boxplot_chann[feature], feature)

plt.tight_layout()
plt.show()


# ----------------------------
# SEÇÃO 3: RANKING DE PERFORMANCE
# ----------------------------

channel_data_sorted = channel_data.sort_values(by='Index_Performance_log10', ascending=False)

plt.figure(figsize=(10, 12))
ax = sns.barplot(
    data=channel_data_sorted,
    x='Index_Performance_log10',
    y='Channel_name',
    color='blue'
)
plt.xticks(rotation=0, ha='center')
plt.xlabel('Índice de performance (log10)')
plt.ylabel('Nome do canal')
plt.title('Ranking de Performance dos Canais (escala logarítmica)')
ax.grid(True, axis='y', linestyle='--', alpha=1)
plt.tight_layout()
plt.show()


# ----------------------------
# SEÇÃO 4: CORRELAÇÃO (PAIRPLOT)
# ----------------------------

from scipy.stats import pearsonr

def corrfunc(x, y, ax=None, **kws):
    r, _ = pearsonr(x, y)
    ax = ax or plt.gca()
    ax.annotate(f'R² = {r:.2f}', xy=(.4, .9), xycoords=ax.transAxes)

g = sns.pairplot(
    data=channel_data_corr,
    kind='reg',
    corner=True,
    plot_kws={'line_kws': {'color': 'red'}}
)
g.map_lower(corrfunc)
plt.show()

# ----------------------------
# SEÇÃO 5: DESCRIÇÃO
# ----------------------------

channel_data.describe().apply(lambda s: s.apply('{0:.2f}'.format))

"""# Parte 4: Análise dos Canais com IP > 2,5

## 4.1 os 10 vídeos mais curtidos
"""

# ============================
# PARTE 4.1 — TOP 10 VÍDEOS MAIS CURTIDOS (Canais IP > 2.5)
# Fonte: API ou CSV estático
# ============================

import pandas as pd

IP_CUTOFF = 2.5
MIN_SECONDS = 180
YEAR_FILTER = None # Use "None" para buscar todos ou troque por um ano específico.

PATH_ALL_VIDEOS = "brazilian-math-youtube-channels/data/raw/all_videos.csv"
PATH_VIDEO_DETAILS = "brazilian-math-youtube-channels/data/raw/video_details.csv"


# ----------------------------
# HELPERS
# ----------------------------

def get_canais_ip_alto(channel_data: pd.DataFrame, ip_cutoff: float) -> set:
    canais = channel_data[channel_data["Index_Performance_log10"] > ip_cutoff]
    return set(canais["Channel_name"].tolist())


def normalize_details(df_details: pd.DataFrame) -> pd.DataFrame:
    out = df_details.copy()
    out["Likes"] = pd.to_numeric(out["Likes"], errors="coerce")
    out["Views"] = pd.to_numeric(out["Views"], errors="coerce")
    out["Comments"] = pd.to_numeric(out["Comments"], errors="coerce")
    return out


def apply_year_filter(df: pd.DataFrame, year: int | None) -> pd.DataFrame:
    out = df.copy()
    out["Published_at"] = pd.to_datetime(out["Published_at"], errors="coerce")
    if year is None:
        return out
    return out[out["Published_at"].dt.year == year]


def top10_por_canal(df: pd.DataFrame) -> dict:
    resultado = {}
    for canal in df["Channel_name"].dropna().unique():
        df_c = df[df["Channel_name"] == canal]
        top10 = df_c.sort_values(by="Likes", ascending=False).head(10)
        resultado[canal] = top10[["Title", "Video_id", "Likes", "Views", "Published_at"]]
    return resultado


def print_top10(top10_dict: dict, year: int | None):
    titulo = f"ANO {year}" if year is not None else "TODOS OS TEMPOS"
    print(f"====== TOP 10 MAIS CURTIDOS ({titulo}) ======\n")

    for canal, tabela in top10_dict.items():
        print(f"\nCanal: {canal}")
        if tabela.empty:
            print(f"  Nenhum vídeo{' em ' + str(year) if year else ''}.")
            continue

        for _, row in tabela.iterrows():
            print(f"\n  - {row['Title']}")
            print(f"    Curtidas: {row['Likes']}")
            print(f"    Visualizações: {row['Views']}")
            print(f"    Data: {row['Published_at']}")
            print(f"    Video_id: {row['Video_id']}")


# ----------------------------
# LOADER — CSV ESTÁTICO
# ----------------------------

def build_df_full_from_static(canais_validos: set) -> pd.DataFrame:
    df_videos = pd.read_csv(PATH_ALL_VIDEOS)
    df_details = pd.read_csv(PATH_VIDEO_DETAILS)
    df_details = normalize_details(df_details)

    df_full = df_videos.merge(df_details, on="Video_id", how="left")
    df_full = df_full[df_full["Channel_name"].isin(canais_validos)].copy()
    return df_full


# ----------------------------
# LOADER — API
# ----------------------------

def build_df_full_from_api(channel_data: pd.DataFrame, canais_validos: set) -> pd.DataFrame:
    rows = []

    df_canais = channel_data[channel_data["Channel_name"].isin(canais_validos)]

    print("Coletando dados de vídeos (API) para canais com IP alto...")
    for _, row in df_canais.iterrows():
        playlist_id = row["Playlist_id"]
        channel_name = row["Channel_name"]
        print(f"  Canal: {channel_name}")

        videos = get_all_videos_channel(youtube, playlist_id)
        df_videos = pd.DataFrame(videos)

        if df_videos.empty:
            continue

        video_ids = df_videos["Video_id"].tolist()
        details = get_video_details(youtube, video_ids)
        df_details = pd.DataFrame(details)

        if not df_details.empty:
            df_details["Likes"] = pd.to_numeric(df_details["Likes"], errors="coerce")
            df_details["Views"] = pd.to_numeric(df_details["Views"], errors="coerce")
            df_details["Comments"] = pd.to_numeric(df_details["Comments"], errors="coerce")

        df_full_ch = df_videos.merge(df_details, on="Video_id", how="left")
        rows.append(df_full_ch)

    if not rows:
        return pd.DataFrame(columns=["Channel_name", "Title", "Video_id", "Likes", "Views", "Published_at"])

    return pd.concat(rows, ignore_index=True)


# ----------------------------
# PIPELINE ÚNICO
# ----------------------------

canais_validos = get_canais_ip_alto(channel_data, IP_CUTOFF)

df_full = build_df_full_from_api(channel_data, canais_validos) if requisitar_da_api else build_df_full_from_static(canais_validos)

df_full = apply_year_filter(df_full, YEAR_FILTER)

top10 = top10_por_canal(df_full)
print_top10(top10, YEAR_FILTER)

# ----------------------------
# SEÇÃO 4.2 — GRÁFICOS (OPCIONAL)
# ----------------------------

GERAR_GRAFICOS = True  # True = plota | False = não plota

if GERAR_GRAFICOS:

    import matplotlib.pyplot as plt
    import pandas as pd

    def plot_top10_por_canal(top10_dict_or_list, metric="Likes", year=None):
        """
        Plota top 10 por canal no estilo barh (matplotlib puro).
        Aceita:
          - lista antiga [{Channel_name, Top_10_Videos}]
          - dict novo {canal: dataframe}
        """

        # ----------------------------
        # Detectar formato entrada
        # ----------------------------

        if isinstance(top10_dict_or_list, list):
            iterator = []
            for canal_data in top10_dict_or_list:
                canal = canal_data["Channel_name"]
                top_videos = (
                    canal_data.get("Top_10_Videos")
                    or canal_data.get("Top_10_Videos_2025")
                )

                if isinstance(top_videos, list) and top_videos:
                    iterator.append((canal, pd.DataFrame(top_videos)))
                else:
                    iterator.append((canal, pd.DataFrame()))
        else:
            iterator = [(canal, df.copy()) for canal, df in top10_dict_or_list.items()]

        # ----------------------------
        # Texto período
        # ----------------------------

        periodo = f"(ANO {year})" if year is not None else "(TODOS OS TEMPOS)"

        # ----------------------------
        # Loop canais
        # ----------------------------

        for canal, df in iterator:

            if df is None or df.empty:
                print(f"Não há vídeos para exibir o gráfico para o canal: {canal}")
                continue

            df_plot = df.copy()

            # Garantir numérico
            df_plot[metric] = pd.to_numeric(df_plot[metric], errors="coerce")

            # Ordenar
            df_sorted = df_plot.sort_values(by=metric, ascending=False)

            titulo = f"Top 10 Vídeos por {metric} {periodo} — {canal}"

            plt.figure(figsize=(16, 6))

            # ESTILO
            bars = plt.barh(df_sorted["Title"], df_sorted[metric])

            plt.title(titulo)
            plt.xlabel(f"Número de {metric}")
            plt.ylabel("Título do Vídeo")

            # Maior no topo
            plt.gca().invert_yaxis()

            # Grade estilo paper
            plt.grid(
                axis="x",
                linestyle="--",
                linewidth=1.5,
                color="black",
                alpha=0.5
            )

            # Notação científica automática
            plt.ticklabel_format(style="sci", axis="x", scilimits=(3, 3))

            plt.tight_layout()
            plt.show()
    # ----------------------------
    # CHAMADA
    # ----------------------------

    plot_top10_por_canal(top10, metric="Likes", year=YEAR_FILTER)
