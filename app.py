import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?id=1MiZvCaDOJ3xasMAqsbEfsx6h32oaBegf"
    df = pd.read_csv(url)
    return df

df = load_data()
st.sidebar.title("Filter")

years = st.sidebar.multiselect(
    "Pilih Tahun",
    sorted(df['year'].unique()),
    default=sorted(df['year'].unique())
)

stations = st.sidebar.multiselect(
    "Pilih Stasiun",
    sorted(df['station'].unique()),
    default=sorted(df['station'].unique())
)

df = df[(df['year'].isin(years)) & (df['station'].isin(stations))]

st.title("💨 Air Quality Dashboard")
avg_pm25 = df['PM2.5'].mean()
max_pm25 = df['PM2.5'].max()
pct_high = (df['PM2.5'] > 100).mean() * 100
worst_station = df.groupby('station')['PM2.5'].mean().idxmax()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rata-rata PM2.5", f"{avg_pm25:.1f}")
col2.metric("PM2.5 Tertinggi", f"{max_pm25:.0f}")
col3.metric("Hari Buruk (%)", f"{pct_high:.1f}%")
col4.metric("Stasiun Terburuk", worst_station)

st.subheader("📈 Tren PM2.5 per Tahun")

pm25_year = df.groupby('year')['PM2.5'].mean()

fig, ax = plt.subplots()
ax.plot(pm25_year.index, pm25_year.values, marker='o')
ax.set_xlabel("Tahun")
ax.set_ylabel("PM2.5")
st.pyplot(fig)

st.subheader("📍 PM2.5 per Stasiun")

pm25_station = df.groupby('station')['PM2.5'].mean().sort_values()

fig, ax = plt.subplots()
ax.barh(pm25_station.index, pm25_station.values)
st.pyplot(fig)

st.subheader("🌡️ Korelasi")

corr = df[['PM2.5','TEMP','WSPM','PRES','DEWP','RAIN']].corr()

st.dataframe(corr)

st.subheader("🌧️ Pengaruh Hujan")

df['rain_bin'] = pd.cut(df['RAIN'],
                       bins=[-1,0,2,10,1000],
                       labels=['No Rain','Light','Medium','Heavy'])

rain_pm25 = df.groupby('rain_bin')['PM2.5'].mean()

fig, ax = plt.subplots()
rain_pm25.plot(kind='bar', ax=ax)
st.pyplot(fig)

if st.checkbox("Tampilkan Data"):
    st.dataframe(df)
