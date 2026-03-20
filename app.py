import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?id=1MiZvCaDOJ3xasMAqsbEfsx6h32oaBegf"
    df = pd.read_csv(url)
    return df

df_raw = load_data()

st.sidebar.title("Filter Dashboard")

years = st.sidebar.multiselect(
    "Pilih Tahun",
    sorted(df_raw['year'].unique()),
    default=sorted(df_raw['year'].unique())
)

stations = st.sidebar.multiselect(
    "Pilih Stasiun",
    sorted(df_raw['station'].unique()),
    default=sorted(df_raw['station'].unique())
)

# Terapkan filter
df = df_raw[(df_raw['year'].isin(years)) & (df_raw['station'].isin(stations))]

st.title("💨 Air Quality Dashboard")
st.markdown("**Oleh: Steven Lie Wibowo**")
st.divider()

# --- METRICS ---
avg_pm25 = df['PM2.5'].mean()
max_pm25 = df['PM2.5'].max()
pct_high = (df['PM2.5'] > 100).mean() * 100
worst_station = df.groupby('station')['PM2.5'].mean().idxmax()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Rata-rata PM2.5", f"{avg_pm25:.1f}")
col2.metric("PM2.5 Tertinggi", f"{max_pm25:.0f}")
col3.metric("Hari Buruk (>100) (%)", f"{pct_high:.1f}%")
col4.metric("Stasiun Terburuk", worst_station)

st.divider()

# --- TREN PM2.5 ---
st.subheader("📈 Tren Konsentrasi PM2.5 per Tahun")
pm25_year = df.groupby('year')['PM2.5'].mean()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(pm25_year.index, pm25_year.values, marker='o', color='#d62728', linewidth=2)
ax.set_xlabel("Tahun")
ax.set_ylabel("Rata-rata PM2.5")
ax.set_xticks(pm25_year.index)
ax.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig)
st.caption("Kualitas udara belum mengalami perbaikan yang stabil dan cenderung fluktuatif.")

st.divider()

# --- FAKTOR LINGKUNGAN ---
st.subheader("🌬️ Faktor Lingkungan yang Mempengaruhi PM2.5")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("**Heatmap Korelasi Faktor Cuaca**")
    corr = df[['PM2.5','TEMP','WSPM','PRES','DEWP','RAIN']].corr()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1, ax=ax)
    st.pyplot(fig)

with col_right:
    st.markdown("**Pengaruh Kecepatan Angin (WSPM)**")
    fig, ax = plt.subplots(figsize=(6, 5))
    # Menggunakan sample jika data terlalu besar agar plot tidak berat
    sns.scatterplot(data=df.sample(n=min(5000, len(df)), random_state=42), x='WSPM', y='PM2.5', alpha=0.3, color='#1f77b4', ax=ax)
    ax.set_xlabel("Kecepatan Angin (WSPM)")
    ax.set_ylabel("PM2.5")
    st.pyplot(fig)
    
st.caption("Kecepatan angin (WSPM) memiliki hubungan negatif yang paling kuat. Semakin kencang angin, polutan PM2.5 semakin tersebar/menurun.")

st.divider()

# --- HUJAN & STASIUN ---
col_bottom1, col_bottom2 = st.columns(2)

with col_bottom1:
    st.subheader("🌧️ Efek Curah Hujan")
    df['rain_bin'] = pd.cut(df['RAIN'],
                           bins=[-1, 0, 2, 10, 1000],
                           labels=['Tidak Hujan', 'Ringan', 'Sedang', 'Lebat'])
    rain_pm25 = df.groupby('rain_bin')['PM2.5'].mean()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    rain_pm25.plot(kind='bar', color='#2ca02c', ax=ax)
    ax.set_xlabel("Intensitas Hujan")
    ax.set_ylabel("Rata-rata PM2.5")
    plt.xticks(rotation=0)
    st.pyplot(fig)

with col_bottom2:
    st.subheader("📍 Rata-rata PM2.5 per Stasiun")
    pm25_station = df.groupby('station')['PM2.5'].mean().sort_values()
    
    fig, ax = plt.subplots(figsize=(6, 4))
    pm25_station.plot(kind='barh', color='#ff7f0e', ax=ax)
    ax.set_xlabel("Rata-rata PM2.5")
    ax.set_ylabel("Stasiun")
    st.pyplot(fig)

st.divider()

if st.checkbox("Tampilkan Dataset Mentah"):
    st.dataframe(df.head(100)) # Menampilkan 100 baris pertama agar tidak memberatkan browser
