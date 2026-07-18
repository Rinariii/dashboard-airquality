import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

st.set_page_config(page_title="Air Quality Dashboard | Beijing 2013-2017", page_icon="🌫️", layout="wide")

PRIMARY = "#2563EB"
TEAL = "#0D9488"
AMBER = "#D97706"
RED = "#DC2626"
SLATE_900 = "#0F172A"
SLATE_700 = "#334155"
SLATE_500 = "#64748B"
SLATE_200 = "#E2E8F0"
BG = "#F5F7FA"
CARD = "#FFFFFF"

AQI_BANDS = [
    (0, 35, "Baik", "#0D9488"),
    (35, 75, "Sedang", "#2563EB"),
    (75, 115, "Tidak Sehat", "#D97706"),
    (115, 150, "Sangat Tidak Sehat", "#EA580C"),
    (150, 100000, "Berbahaya", "#DC2626"),
]

def aqi_color(value):
    for low, high, _, color in AQI_BANDS:
        if low <= value < high:
            return color
    return SLATE_500

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background-color: {BG};
}}

#MainMenu, footer, header {{visibility: hidden;}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 3rem;
}}

.dashboard-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding-bottom: 8px;
    border-bottom: 2px solid {SLATE_900};
    margin-bottom: 4px;
}}

.dashboard-title {{
    font-size: 30px;
    font-weight: 800;
    color: {SLATE_900};
    letter-spacing: -0.5px;
    margin: 0;
}}

.dashboard-subtitle {{
    font-size: 14px;
    color: {SLATE_500};
    margin-top: 4px;
}}

.dashboard-tag {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: {SLATE_500};
    text-align: right;
}}

.section-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: {PRIMARY};
    margin-bottom: -4px;
}}

.section-title {{
    font-size: 19px;
    font-weight: 700;
    color: {SLATE_900};
    margin-top: 2px;
    margin-bottom: 10px;
}}

.insight-caption {{
    font-size: 13px;
    color: {SLATE_500};
    border-left: 3px solid {SLATE_200};
    padding-left: 10px;
    margin-top: 6px;
}}

div[data-testid="stMetric"] {{
    background-color: {CARD};
    border: 1px solid {SLATE_200};
    border-radius: 10px;
    padding: 16px 18px 12px 18px;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}}

div[data-testid="stMetricLabel"] {{
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    color: {SLATE_500};
}}

div[data-testid="stMetricValue"] {{
    font-family: 'JetBrains Mono', monospace;
    color: {SLATE_900};
    font-weight: 700;
}}

section[data-testid="stSidebar"] {{
    background-color: {CARD};
    border-right: 1px solid {SLATE_200};
}}

section[data-testid="stSidebar"] .stMarkdown h1 {{
    font-size: 17px;
    font-weight: 700;
    color: {SLATE_900};
}}

hr {{
    border-color: {SLATE_200} !important;
}}
</style>
""", unsafe_allow_html=True)

sns.set_theme(style="whitegrid", rc={
    "axes.facecolor": CARD,
    "figure.facecolor": CARD,
    "axes.edgecolor": SLATE_200,
    "grid.color": SLATE_200,
    "axes.labelcolor": SLATE_700,
    "text.color": SLATE_700,
    "xtick.color": SLATE_500,
    "ytick.color": SLATE_500,
    "font.family": "sans-serif",
})

@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?id=1MiZvCaDOJ3xasMAqsbEfsx6h32oaBegf"
    return pd.read_csv(url)

df_raw = load_data()

st.sidebar.markdown("# Filter Dashboard")
st.sidebar.markdown("<span style='font-size:13px;color:#64748B'>Sesuaikan cakupan data yang ditampilkan</span>", unsafe_allow_html=True)
st.sidebar.markdown("---")

years = st.sidebar.multiselect(
    "Tahun",
    sorted(df_raw["year"].unique()),
    default=sorted(df_raw["year"].unique()),
)
stations = st.sidebar.multiselect(
    "Stasiun Pemantauan",
    sorted(df_raw["station"].unique()),
    default=sorted(df_raw["station"].unique()),
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<span style='font-size:12px;color:#94A3B8'>Sumber data: Beijing Multi-Site Air Quality (2013–2017), UCI Machine Learning Repository</span>",
    unsafe_allow_html=True,
)

df = df_raw[df_raw["year"].isin(years) & df_raw["station"].isin(stations)]

st.markdown(f"""
<div class="dashboard-header">
    <div>
        <p class="dashboard-title">Air Quality Monitoring Dashboard</p>
        <p class="dashboard-subtitle">Analisis Konsentrasi PM2.5 di Beijing &middot; Periode 2013–2017</p>
    </div>
    <div class="dashboard-tag">Oleh Steven Lie Wibowo<br>{len(stations)} stasiun &middot; {len(years)} tahun terpilih</div>
</div>
""", unsafe_allow_html=True)

st.write("")

avg_pm25 = df["PM2.5"].mean()
max_pm25 = df["PM2.5"].max()
pct_high = (df["PM2.5"] > 100).mean() * 100
worst_station = df.groupby("station")["PM2.5"].mean().idxmax()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Rata-rata PM2.5", f"{avg_pm25:.1f} µg/m³")
col2.metric("PM2.5 Tertinggi", f"{max_pm25:.0f} µg/m³")
col3.metric("Hari Tidak Sehat (>100)", f"{pct_high:.1f}%")
col4.metric("Stasiun Terburuk", worst_station)

st.write("")
st.markdown('<p class="section-label">Tren Historis</p>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Konsentrasi Rata-rata PM2.5 per Tahun</p>', unsafe_allow_html=True)

pm25_year = df.groupby("year")["PM2.5"].mean()
fig, ax = plt.subplots(figsize=(11, 3.8))
ax.plot(pm25_year.index, pm25_year.values, marker="o", markersize=7, color=PRIMARY, linewidth=2.5, zorder=3)
ax.fill_between(pm25_year.index, pm25_year.values, color=PRIMARY, alpha=0.06)
ax.axhline(35, color=TEAL, linestyle="--", linewidth=1.2, alpha=0.8)
ax.text(pm25_year.index.max(), 35, "  Baku Mutu WHO (35 µg/m³)", va="center", fontsize=9, color=TEAL)
ax.set_xlabel("Tahun")
ax.set_ylabel("Rata-rata PM2.5 (µg/m³)")
ax.set_xticks(pm25_year.index)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig)
st.markdown('<p class="insight-caption">Kualitas udara belum mengalami perbaikan yang stabil dan cenderung fluktuatif dari tahun ke tahun, namun tetap jauh di atas ambang batas aman WHO.</p>', unsafe_allow_html=True)

st.write("")
st.markdown("---")
st.markdown('<p class="section-label">Analisis Faktor</p>', unsafe_allow_html=True)
st.markdown('<p class="section-title">Faktor Lingkungan yang Mempengaruhi PM2.5</p>', unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("**Korelasi Antar Variabel Cuaca**")
    corr = df[["PM2.5", "TEMP", "WSPM", "PRES", "DEWP", "RAIN"]].corr()
    fig, ax = plt.subplots(figsize=(5.5, 4.6))
    sns.heatmap(
        corr, annot=True, fmt=".2f", vmin=-1, vmax=1, ax=ax,
        cmap=sns.diverging_palette(220, 20, as_cmap=True),
        linewidths=0.5, linecolor=CARD, cbar_kws={"shrink": 0.8},
        annot_kws={"fontsize": 9},
    )
    st.pyplot(fig)

with col_right:
    st.markdown("**Pengaruh Kecepatan Angin terhadap PM2.5**")
    fig, ax = plt.subplots(figsize=(5.5, 4.6))
    sns.scatterplot(
        data=df.sample(n=min(5000, len(df)), random_state=42),
        x="WSPM", y="PM2.5", alpha=0.35, color=PRIMARY, s=18, ax=ax,
    )
    ax.set_xlabel("Kecepatan Angin (WSPM)")
    ax.set_ylabel("PM2.5 (µg/m³)")
    ax.spines[["top", "right"]].set_visible(False)
    st.pyplot(fig)

st.markdown('<p class="insight-caption">Kecepatan angin memiliki hubungan negatif paling kuat terhadap PM2.5 — semakin kencang angin, polutan semakin cepat tersebar dan konsentrasinya menurun.</p>', unsafe_allow_html=True)

st.write("")
st.markdown("---")

col_bottom1, col_bottom2 = st.columns(2)

with col_bottom1:
    st.markdown('<p class="section-label">Cuaca</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Efek Curah Hujan terhadap PM2.5</p>', unsafe_allow_html=True)
    df = df.copy()
    df["rain_bin"] = pd.cut(
        df["RAIN"], bins=[-1, 0, 2, 10, 1000],
        labels=["Tidak Hujan", "Ringan", "Sedang", "Lebat"],
    )
    rain_pm25 = df.groupby("rain_bin")["PM2.5"].mean()
    fig, ax = plt.subplots(figsize=(5.8, 4))
    bars = ax.bar(rain_pm25.index.astype(str), rain_pm25.values, color=TEAL, width=0.55)
    ax.set_xlabel("Intensitas Hujan")
    ax.set_ylabel("Rata-rata PM2.5 (µg/m³)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.bar_label(bars, fmt="%.1f", padding=3, fontsize=9, color=SLATE_700)
    st.pyplot(fig)

with col_bottom2:
    st.markdown('<p class="section-label">Perbandingan Lokasi</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Rata-rata PM2.5 per Stasiun</p>', unsafe_allow_html=True)
    pm25_station = df.groupby("station")["PM2.5"].mean().sort_values()
    colors = [aqi_color(v) for v in pm25_station.values]
    fig, ax = plt.subplots(figsize=(5.8, 4))
    ax.barh(pm25_station.index, pm25_station.values, color=colors)
    ax.set_xlabel("Rata-rata PM2.5 (µg/m³)")
    ax.set_ylabel("")
    ax.spines[["top", "right"]].set_visible(False)
    st.pyplot(fig)

st.write("")
st.markdown("---")

with st.expander("Tampilkan Dataset Mentah"):
    st.dataframe(df.head(100), use_container_width=True)
