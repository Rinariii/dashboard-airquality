# 💨 Air Quality Analysis Dashboard

Dashboard interaktif untuk menganalisis kualitas udara (PM2.5) berdasarkan data tahun 2013–2017 dari berbagai stasiun pemantauan.

---

## 📌 Project Overview

Polusi udara, khususnya **PM2.5**, merupakan salah satu masalah lingkungan yang berdampak besar terhadap kesehatan manusia.
Project ini bertujuan untuk:

* Menganalisis tren PM2.5 dari waktu ke waktu
* Mengidentifikasi faktor lingkungan yang mempengaruhi kualitas udara
* Menyajikan insight dalam bentuk dashboard interaktif menggunakan Streamlit

---

## ❓ Pertanyaan Analisis

1. **Bagaimana tren konsentrasi PM2.5 dari tahun 2013 hingga 2017?**
2. **Faktor lingkungan apa yang paling mempengaruhi tingkat PM2.5?**

---

## 📊 Insight Utama

### 📈 Tren PM2.5 (2013–2017)

* Konsentrasi PM2.5 **berfluktuasi setiap tahun**
* Tahun dengan polusi tertinggi menunjukkan kondisi udara yang tidak stabil
* Tidak terdapat tren penurunan yang konsisten → kualitas udara masih menjadi masalah

---

### 🌍 Faktor yang Mempengaruhi PM2.5

* **Kecepatan angin (WSPM)** memiliki korelasi negatif paling kuat
  → semakin tinggi angin, polusi menurun
* **Curah hujan (RAIN)** membantu menurunkan PM2.5
  → berperan sebagai “pembersih udara alami”
* Faktor lain seperti suhu dan tekanan memiliki pengaruh lebih kecil

---

## 🚀 Fitur Dashboard

* 📅 Filter berdasarkan tahun
* 📍 Filter berdasarkan stasiun
* 📊 Visualisasi tren PM2.5
* 📉 Perbandingan antar stasiun
* 🌡️ Heatmap korelasi faktor lingkungan
* 🌧️ Analisis pengaruh hujan
* 📦 Kategori kualitas udara (Rendah - Sangat Tinggi)
* 💡 Insight otomatis pada setiap visualisasi

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Pandas
* NumPy
* Matplotlib
* Seaborn

---

## ▶️ Cara Menjalankan Project

### 1. Clone repository

```bash
git clone https://github.com/username/air-quality-dashboard.git
cd air-quality-dashboard/dashboard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Jalankan Streamlit

```bash
streamlit run app.py
```

---

## 🌐 Deploy (Streamlit Cloud)

1. Upload project ke GitHub
2. Buka Streamlit Cloud
3. Pilih repository
4. Set file utama:

```
app.py
```

---

## 📌 Kesimpulan

* Kualitas udara **belum menunjukkan perbaikan signifikan**
* Polusi PM2.5 masih sering berada pada level berbahaya
* Faktor lingkungan seperti **angin dan hujan** memiliki peran penting dalam menurunkan polusi
* Diperlukan strategi tambahan untuk mengendalikan sumber polusi

---

## 👤 Author

**Steven Lie Wibowo**
