import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

st.set_page_config(
    page_title="Air Quality Dashboard",
    page_icon="💨",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #1e293b;
}
[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f8fafc !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: #1d4ed8 !important;
}

/* Main background */
.main .block-container {
    background: #f8fafc;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Metric card style */
div[data-testid="metric-container"] {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
div[data-testid="metric-container"] label {
    color: #64748b !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
}
div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.78rem !important;
}

/* Section headers */
h2.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #0f172a;
    border-left: 3px solid #2563eb;
    padding-left: 0.75rem;
    margin: 2rem 0 1rem;
}

/* Insight boxes */
.insight-box {
    background: #eff6ff;
    border-left: 4px solid #2563eb;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.2rem;
    margin-top: 0.75rem;
    color: #1e3a5f;
    font-size: 0.88rem;
    line-height: 1.6;
}
.insight-box.warn {
    background: #fff7ed;
    border-color: #f97316;
    color: #7c2d12;
}
.insight-box.good {
    background: #f0fdf4;
    border-color: #22c55e;
    color: #14532d;
}

/* Pill badges */
.badge {
    display: inline-block;
    padding: 0.2em 0.75em;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 0.15rem;
}
.badge-red   { background:#fee2e2; color:#991b1b; }
.badge-amber { background:#fef3c7; color:#92400e; }
.badge-green { background:#dcfce7; color:#166534; }
.badge-blue  { background:#dbeafe; color:#1e40af; }

/* Plot cards */
.plot-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}

/* Footer */
.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 0.8rem;
    padding-top: 2rem;
    border-top: 1px solid #e2e8f0;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\steve\Downloads\Dicoding submission\dashboard\main_data.csv")
    return df

df_raw = load_data()

def categorize_pm25(val):
    if val <= 50:   return "Rendah"
    elif val <= 100: return "Sedang"
    elif val <= 200: return "Tinggi"
    else:            return "Sangat Tinggi"

df_raw['PM25_Category'] = df_raw['PM2.5'].apply(categorize_pm25)


def aqi_color(mean):
    if mean <= 50:   return "#22c55e", "Baik"
    elif mean <= 100: return "#eab308", "Sedang"
    elif mean <= 150: return "#f97316", "Tidak Sehat (Sensitif)"
    elif mean <= 200: return "#ef4444", "Tidak Sehat"
    else:             return "#7c3aed", "Sangat Tidak Sehat"

with st.sidebar:
    st.markdown("## 💨 Air Quality\n### Dashboard")
    st.markdown("---")
    st.markdown("### Filter Data")

    all_years  = sorted(df_raw['year'].unique())
    sel_years  = st.multiselect("Tahun", all_years, default=all_years)

    all_stations = sorted(df_raw['station'].unique())
    sel_stations = st.multiselect("Stasiun", all_stations, default=all_stations)

    show_raw = st.checkbox("Tampilkan raw data", value=False)

    st.markdown("---")
    st.markdown("**Kategori PM2.5**")
    st.markdown("""
    <div>
      <span class='badge badge-green'>Rendah ≤50</span>
      <span class='badge badge-amber'>Sedang ≤100</span>
      <span class='badge badge-red'>Tinggi ≤200</span>
      <span class='badge badge-red' style='opacity:.7'>Sangat Tinggi >200</span>
    </div>
    """, unsafe_allow_html=True)

df = df_raw[df_raw['year'].isin(sel_years) & df_raw['station'].isin(sel_stations)].copy()

st.markdown("# 💨 Air Quality Dashboard")
st.markdown(f"<span style='color:#64748b;font-size:.9rem'>Data dari {df['year'].min()} – {df['year'].max()} · {len(sel_stations)} stasiun · {len(df):,} record</span>", unsafe_allow_html=True)
st.markdown("---")

avg_pm25  = df['PM2.5'].mean()
max_pm25  = df['PM2.5'].max()
aqi_clr, aqi_label = aqi_color(avg_pm25)
pct_high  = (df['PM2.5'] > 100).mean() * 100
worst_stn = df.groupby('station')['PM2.5'].mean().idxmax()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Rata-rata PM2.5", f"{avg_pm25:.1f} µg/m³",
              delta=f"Status: {aqi_label}", delta_color="inverse" if avg_pm25 > 100 else "normal")
with col2:
    st.metric("PM2.5 Tertinggi", f"{max_pm25:.0f} µg/m³")
with col3:
    st.metric("Hari Kualitas Buruk", f"{pct_high:.1f}%",
              delta="PM2.5 > 100 µg/m³", delta_color="inverse" if pct_high > 30 else "off")
with col4:
    st.metric("Stasiun Terpolusi", worst_stn)

st.markdown("")

st.markdown("<h2 class='section-title'>📈 Tren & Distribusi Stasiun</h2>", unsafe_allow_html=True)
c1, c2 = st.columns([1.4, 1])

with c1:
    pm25_year = df.groupby('year')['PM2.5'].mean()
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.fill_between(pm25_year.index, pm25_year.values, alpha=0.15, color='#2563eb')
    ax.plot(pm25_year.index, pm25_year.values, marker='o', color='#2563eb',
            linewidth=2.5, markersize=7, markerfacecolor='white', markeredgewidth=2.5)

    # Reference lines
    ax.axhline(50,  ls='--', lw=1, color='#22c55e', alpha=.6, label='Baik (50)')
    ax.axhline(100, ls='--', lw=1, color='#f97316', alpha=.6, label='Tidak Sehat (100)')

    for x, y in zip(pm25_year.index, pm25_year.values):
        ax.annotate(f"{y:.0f}", (x, y), textcoords="offset points",
                    xytext=(0, 10), ha='center', fontsize=9, color='#1e40af', fontweight='600')

    ax.set_title("Rata-rata PM2.5 per Tahun", fontsize=11, fontweight='600', pad=10, color='#0f172a')
    ax.set_xlabel("Tahun", fontsize=9, color='#64748b')
    ax.set_ylabel("PM2.5 (µg/m³)", fontsize=9, color='#64748b')
    ax.legend(fontsize=8, framealpha=0.8)
    ax.set_facecolor('#f8fafc')
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['left','bottom']].set_color('#e2e8f0')
    ax.tick_params(colors='#64748b', labelsize=9)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

    peak_year = pm25_year.idxmax()
    low_year  = pm25_year.idxmin()
    delta_pct = ((pm25_year.max() - pm25_year.min()) / pm25_year.min() * 100)
    st.markdown(f"""<div class='insight-box warn'>
    📊 <b>Insight:</b> Tahun <b>{peak_year}</b> mencatat PM2.5 tertinggi (<b>{pm25_year.max():.1f} µg/m³</b>),
    sedangkan <b>{low_year}</b> paling bersih (<b>{pm25_year.min():.1f} µg/m³</b>).
    Selisih antara tahun terbersih dan terpolusi mencapai <b>{delta_pct:.0f}%</b> — menunjukkan kualitas udara yang sangat fluktuatif dan belum stabil.
    </div>""", unsafe_allow_html=True)

with c2:
    pm25_station = df.groupby('station')['PM2.5'].mean().sort_values()
    colors = ['#ef4444' if v > 100 else '#f97316' if v > 75 else '#22c55e' for v in pm25_station]

    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    bars = ax.barh(pm25_station.index, pm25_station.values, color=colors, height=0.6)
    ax.axvline(100, ls='--', lw=1.2, color='#ef4444', alpha=0.7)
    ax.set_title("Rata-rata PM2.5 per Stasiun", fontsize=11, fontweight='600', pad=10, color='#0f172a')
    ax.set_xlabel("PM2.5 (µg/m³)", fontsize=9, color='#64748b')
    ax.set_facecolor('#f8fafc')
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['left','bottom']].set_color('#e2e8f0')
    ax.tick_params(colors='#64748b', labelsize=8)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 1, bar.get_y() + bar.get_height()/2, f"{w:.0f}",
                va='center', fontsize=8, color='#64748b')
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

    n_danger = (pm25_station > 100).sum()
    st.markdown(f"""<div class='insight-box {"warn" if n_danger > 0 else "good"}'>
    📍 <b>Insight:</b> <b>{n_danger} dari {len(pm25_station)} stasiun</b> rata-rata PM2.5-nya melampaui ambang batas 100 µg/m³.
    Stasiun <b>{pm25_station.idxmax()}</b> paling berpolusi — perlu perhatian prioritas.
    </div>""", unsafe_allow_html=True)

st.markdown("<h2 class='section-title'>🌍 Faktor Lingkungan & Distribusi Kategori</h2>", unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
    corr_cols = ['PM2.5', 'TEMP', 'WSPM', 'PRES', 'DEWP', 'RAIN']
    corr = df[corr_cols].corr()

    cmap = LinearSegmentedColormap.from_list("custom", ['#ef4444','#f8fafc','#2563eb'])
    fig, ax = plt.subplots(figsize=(5, 4))
    mask = np.zeros_like(corr, dtype=bool)
    mask[np.triu_indices_from(mask, k=1)] = True
    sns.heatmap(corr, annot=True, fmt=".2f", cmap=cmap, center=0,
                ax=ax, square=True, linewidths=0.5,
                linecolor='#e2e8f0', annot_kws={'size': 9},
                cbar_kws={'shrink': 0.8})
    ax.set_title("Korelasi PM2.5 dengan Faktor Cuaca", fontsize=11, fontweight='600', pad=10, color='#0f172a')
    ax.tick_params(labelsize=9, colors='#0f172a')
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

    corr_pm25 = corr['PM2.5'].drop('PM2.5').abs().sort_values(ascending=False)
    top_factor = corr_pm25.idxmax()
    top_val    = corr['PM2.5'][top_factor]
    st.markdown(f"""<div class='insight-box'>
    🌡️ <b>Insight:</b> Faktor paling berpengaruh terhadap PM2.5 adalah <b>{top_factor}</b>
    (korelasi: <b>{top_val:+.2f}</b>).
    {'Angin (WSPM) bersifat protektif — semakin kencang angin, PM2.5 cenderung menurun karena polutan tersebar.' if top_factor == 'WSPM' else f'Nilai positif berarti semakin tinggi {top_factor}, PM2.5 juga cenderung naik.'}
    Faktor lainnya (TEMP, PRES, DEWP, RAIN) memiliki pengaruh relatif lebih kecil.
    </div>""", unsafe_allow_html=True)

with c4:
    cat_order  = ['Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi']
    cat_colors = ['#22c55e', '#eab308', '#f97316', '#ef4444']
    cat_counts = df['PM25_Category'].value_counts().reindex(cat_order).fillna(0)
    cat_pct    = cat_counts / cat_counts.sum() * 100

    fig, ax = plt.subplots(figsize=(5, 4))
    bars = ax.bar(cat_order, cat_counts.values, color=cat_colors,
                  width=0.55, edgecolor='white', linewidth=1.5)

    for bar, pct in zip(bars, cat_pct):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + max(cat_counts)*0.01,
                f"{pct:.1f}%", ha='center', va='bottom', fontsize=9,
                fontweight='600', color='#0f172a')

    ax.set_title("Distribusi Kategori PM2.5", fontsize=11, fontweight='600', pad=10, color='#0f172a')
    ax.set_xlabel("Kategori", fontsize=9, color='#64748b')
    ax.set_ylabel("Jumlah Record", fontsize=9, color='#64748b')
    ax.set_facecolor('#f8fafc')
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['left','bottom']].set_color('#e2e8f0')
    ax.tick_params(colors='#64748b', labelsize=9)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

    dominant = cat_pct.idxmax()
    dom_pct  = cat_pct.max()
    bad_pct  = cat_pct[['Tinggi','Sangat Tinggi']].sum()
    st.markdown(f"""<div class='insight-box {"warn" if bad_pct > 20 else "good"}'>
    📊 <b>Insight:</b> Kategori dominan adalah <b>{dominant}</b> ({dom_pct:.1f}% record).
    Namun, <b>{bad_pct:.1f}% data berada di kategori Tinggi atau Sangat Tinggi</b> — menandakan
    masih seringnya kejadian polusi berbahaya. {"Perlu intervensi serius!" if bad_pct > 30 else "Situasi masih dalam batas toleransi, namun perlu dipantau."}
    </div>""", unsafe_allow_html=True)

st.markdown("<h2 class='section-title'>🌧️ Pola Musiman & Pengaruh Hujan</h2>", unsafe_allow_html=True)
c5, c6 = st.columns(2)

with c5:
    if 'month' in df.columns:
        month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'Mei',6:'Jun',
                       7:'Jul',8:'Agu',9:'Sep',10:'Okt',11:'Nov',12:'Des'}
        pm25_month = df.groupby('month')['PM2.5'].mean()

        fig, ax = plt.subplots(figsize=(5, 3.5))
        ax.fill_between(pm25_month.index, pm25_month.values, alpha=0.12, color='#7c3aed')
        ax.plot(pm25_month.index, pm25_month.values, marker='o', color='#7c3aed',
                linewidth=2.5, markersize=6, markerfacecolor='white', markeredgewidth=2)
        ax.set_xticks(list(month_names.keys()))
        ax.set_xticklabels(list(month_names.values()), fontsize=8)
        ax.set_title("Rata-rata PM2.5 per Bulan", fontsize=11, fontweight='600', pad=10, color='#0f172a')
        ax.set_ylabel("PM2.5 (µg/m³)", fontsize=9, color='#64748b')
        ax.set_facecolor('#f8fafc')
        ax.spines[['top','right']].set_visible(False)
        ax.spines[['left','bottom']].set_color('#e2e8f0')
        ax.tick_params(colors='#64748b', labelsize=9)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

        peak_month = pm25_month.idxmax()
        low_month  = pm25_month.idxmin()
        st.markdown(f"""<div class='insight-box'>
        📅 <b>Insight:</b> Polusi PM2.5 memuncak di bulan <b>{month_names.get(peak_month, peak_month)}</b>
        ({pm25_month.max():.1f} µg/m³) dan paling rendah di <b>{month_names.get(low_month, low_month)}</b>
        ({pm25_month.min():.1f} µg/m³). Pola musiman ini bisa terkait musim kering/penghujan
        atau pola aktivitas industri.
        </div>""", unsafe_allow_html=True)
    else:
        st.info("Kolom 'month' tidak tersedia. Tambahkan kolom bulan ke data untuk analisis musiman.")

with c6:
    df['rain_bin'] = pd.cut(df['RAIN'], bins=[-0.1,0,2,10,1000],
                            labels=['Tidak Hujan','Gerimis (0-2mm)','Hujan (2-10mm)','Lebat (>10mm)'])
    rain_pm25 = df.groupby('rain_bin', observed=True)['PM2.5'].mean()

    rain_colors = ['#ef4444','#f97316','#3b82f6','#06b6d4']
    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.bar(rain_pm25.index, rain_pm25.values, color=rain_colors[:len(rain_pm25)],
                  width=0.55, edgecolor='white', linewidth=1.5)

    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.5,
                f"{h:.1f}", ha='center', va='bottom', fontsize=9, fontweight='600', color='#0f172a')

    ax.set_title("Efek Curah Hujan terhadap PM2.5", fontsize=11, fontweight='600', pad=10, color='#0f172a')
    ax.set_xlabel("Intensitas Hujan", fontsize=9, color='#64748b')
    ax.set_ylabel("Rata-rata PM2.5 (µg/m³)", fontsize=9, color='#64748b')
    ax.set_facecolor('#f8fafc')
    ax.spines[['top','right']].set_visible(False)
    ax.spines[['left','bottom']].set_color('#e2e8f0')
    ax.tick_params(colors='#64748b', labelsize=8)
    plt.xticks(rotation=15)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

    no_rain_pm = rain_pm25.get('Tidak Hujan', None)
    heavy_pm   = rain_pm25.get('Lebat (>10mm)', None)
    if no_rain_pm and heavy_pm:
        reduction = (no_rain_pm - heavy_pm) / no_rain_pm * 100
        st.markdown(f"""<div class='insight-box good'>
        🌧️ <b>Insight:</b> Hujan terbukti <b>menurunkan konsentrasi PM2.5</b> secara signifikan.
        Hari tidak hujan rata-rata PM2.5 = <b>{no_rain_pm:.1f} µg/m³</b>,
        sedangkan saat hujan lebat turun menjadi <b>{heavy_pm:.1f} µg/m³</b>
        — penurunan sekitar <b>{reduction:.0f}%</b>. Hujan berfungsi sebagai "pencuci udara" alami.
        </div>""", unsafe_allow_html=True)

if show_raw:
    st.markdown("<h2 class='section-title'>🗄️ Raw Data</h2>", unsafe_allow_html=True)
    st.dataframe(
        df.head(500).style.background_gradient(subset=['PM2.5'], cmap='RdYlGn_r'),
        use_container_width=True, height=320
    )
    st.caption(f"Menampilkan 500 dari {len(df):,} record")

st.markdown("""
<div class='footer'>
    Dibuat oleh <b>Steven Lie Wibowo</b> · Air Quality Analysis Dashboard · Data 2013–2017
</div>
""", unsafe_allow_html=True)