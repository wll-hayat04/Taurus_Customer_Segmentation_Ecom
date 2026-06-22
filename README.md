# 🛒 Taurus — E-Commerce Customer Segmentation

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-deployed-red?logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-KMeans-orange?logo=scikit-learn)
![Dataset](https://img.shields.io/badge/Dataset-541K%20rows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end customer segmentation pipeline for e-commerce using **RFM analysis** and **KMeans clustering** — with an interactive Streamlit dashboard to explore segments visually.

---

## 📸 Demo

<img width="1888" height="767" alt="image" src="https://github.com/user-attachments/assets/2ed718d9-4b25-407c-9766-de9971a9e833" />


| [🛒 Taurus Customer Segmentation](https://github.com/wll-hayat04/Taurus_Customer_Segmentation_Ecom) | RFM + KMeans on 541K rows | [🚀 Live Demo]([https://tauruscustomersegmentationecom-ivd8sykracw4uvceyebxyd.streamlit.app/]) |


---

## 🎯 What is RFM?

| Letter | Metric | Description |
|--------|--------|-------------|
| **R** | Recency | How recently did the customer purchase? |
| **F** | Frequency | How often do they purchase? |
| **M** | Monetary | How much do they spend? |

---

## 🧠 Pipeline

```
Raw Data (541,909 rows)
        ↓
  Data Cleaning
  (remove nulls, duplicates, returns)
        ↓
  RFM Feature Engineering
  (per customer: Recency, Frequency, Monetary)
        ↓
  StandardScaler
        ↓
  KMeans Clustering (K configurable)
        ↓
  Segment Labeling + Visualization
```

---

## ✨ App Features

- 🎛️ **Adjustable K** — change number of clusters live via sidebar slider
- 📊 **Segment donut chart** + horizontal bar chart
- 🔍 **RFM scatter plot** — explore any 2 dimensions colored by segment
- 📋 **Segment summary table** — avg recency, frequency, revenue per segment
- 🌍 **Top 10 countries** by revenue
- ⬇️ **Download** RFM results as CSV

---

## 🚀 Run Locally

```bash
git clone https://github.com/wll-hayat04/Taurus_Customer_Segmentation_Ecom.git
cd Taurus_Customer_Segmentation_Ecom
pip install -r requirements.txt
streamlit run taurus_app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Select repo → set `taurus_app.py` as main file → **Deploy**

---

## 📁 Project Structure

```
Taurus_Customer_Segmentation_Ecom/
│
├── taurus_app.py                 # Streamlit dashboard
├── Nettoyagedataset.ipynb        # Data cleaning notebook
├── online_retail_cleaned.csv     # Cleaned dataset (406K rows)
├── requirements.txt              # Dependencies
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core language |
| pandas | Data manipulation |
| scikit-learn | KMeans + StandardScaler |
| Streamlit | Interactive dashboard |
| Plotly | Charts & visualizations |

---

## 📊 Dataset

- **Source**: [UCI Online Retail Dataset](https://archive.ics.uci.edu/ml/datasets/Online+Retail)
- **Raw size**: 541,909 transactions
- **After cleaning**: ~406,829 rows
- **Features**: InvoiceNo, StockCode, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

---

## 👩‍💻 Author

**Hayat** — 4th Year Engineering Student  
🌍 Morocco | 💼 Open to freelance & internships  
[![GitHub](https://img.shields.io/badge/GitHub-wll--hayat04-181717?logo=github)](https://github.com/wll-hayat04)

---

## 📄 License

[MIT License](LICENSE)
