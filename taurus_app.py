import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Taurus — Customer Segmentation",
    page_icon="🛒",
    layout="wide"
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Settings")
    n_clusters = st.slider("Number of clusters (K)", min_value=2, max_value=8, value=4,
                           help="How many customer segments to identify")
    st.markdown("---")
    st.markdown("""
**Taurus** segments e-commerce customers using **RFM analysis** + **KMeans clustering**.

**RFM stands for:**
- 🕐 **Recency** — days since last purchase
- 🔁 **Frequency** — number of orders
- 💰 **Monetary** — total amount spent

Built by **Hayat** · [GitHub](https://github.com/wll-hayat04)
""")

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🛒 Taurus — Customer Segmentation")
st.caption("RFM Analysis + KMeans Clustering on E-Commerce Data")
st.markdown("---")

# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("online_retail_cleaned.csv", encoding="unicode_escape")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    return df

@st.cache_data
def compute_rfm(df, n_clusters):
    snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("CustomerID").agg(
        Recency=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("TotalPrice", "sum")
    ).reset_index()

    # Scale & cluster
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[["Recency", "Frequency", "Monetary"]])
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    rfm["Cluster"] = km.fit_predict(rfm_scaled)

    # Label clusters by monetary value
    cluster_order = rfm.groupby("Cluster")["Monetary"].mean().sort_values(ascending=False)
    labels = ["Champions", "Loyal Customers", "At Risk", "Lost Customers",
              "Potential", "New Customers", "Hibernating", "Promising"]
    label_map = {old: labels[i] for i, old in enumerate(cluster_order.index)}
    rfm["Segment"] = rfm["Cluster"].map(label_map)
    return rfm

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ `online_retail_cleaned.csv` not found. Please add it to the project folder.")
    st.stop()

rfm = compute_rfm(df, n_clusters)

# ── KPIs ──────────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{len(rfm):,}")
col2.metric("Total Transactions", f"{df['InvoiceNo'].nunique():,}")
col3.metric("Total Revenue", f"£{df['TotalPrice'].sum():,.0f}")
col4.metric("Avg Order Value", f"£{df.groupby('InvoiceNo')['TotalPrice'].sum().mean():,.2f}")

st.markdown("---")

# ── Segment distribution ──────────────────────────────────────────────────────
st.subheader("📊 Customer Segments")
col_left, col_right = st.columns(2)

seg_counts = rfm["Segment"].value_counts().reset_index()
seg_counts.columns = ["Segment", "Count"]

with col_left:
    fig_pie = px.pie(seg_counts, values="Count", names="Segment",
                     title="Segment Distribution",
                     color_discrete_sequence=px.colors.qualitative.Set2,
                     hole=0.4)
    fig_pie.update_layout(margin=dict(t=40, b=0))
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    fig_bar = px.bar(seg_counts.sort_values("Count", ascending=True),
                     x="Count", y="Segment", orientation="h",
                     title="Customers per Segment",
                     color="Count",
                     color_continuous_scale="Teal")
    fig_bar.update_layout(margin=dict(t=40, b=0), coloraxis_showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)

# ── RFM scatter ───────────────────────────────────────────────────────────────
st.subheader("🔍 RFM Explorer")
col_x, col_y = st.columns(2)
x_axis = col_x.selectbox("X axis", ["Recency", "Frequency", "Monetary"], index=0)
y_axis = col_y.selectbox("Y axis", ["Recency", "Frequency", "Monetary"], index=2)

fig_scatter = px.scatter(
    rfm, x=x_axis, y=y_axis, color="Segment",
    size="Monetary", size_max=20,
    hover_data=["CustomerID", "Recency", "Frequency", "Monetary"],
    title=f"{x_axis} vs {y_axis} by Segment",
    color_discrete_sequence=px.colors.qualitative.Set2,
    opacity=0.7
)
fig_scatter.update_layout(margin=dict(t=40, b=0))
st.plotly_chart(fig_scatter, use_container_width=True)

# ── Segment stats table ────────────────────────────────────────────────────────
st.subheader("📋 Segment Summary")
summary = rfm.groupby("Segment").agg(
    Customers=("CustomerID", "count"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Monetary=("Monetary", "mean"),
    Total_Revenue=("Monetary", "sum")
).round(1).reset_index()
summary["Total_Revenue"] = summary["Total_Revenue"].apply(lambda x: f"£{x:,.0f}")
summary["Avg_Monetary"] = summary["Avg_Monetary"].apply(lambda x: f"£{x:,.1f}")
st.dataframe(summary, use_container_width=True, hide_index=True)

# ── Revenue by country ────────────────────────────────────────────────────────
st.subheader("🌍 Revenue by Country (Top 10)")
top_countries = df.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False).head(10).reset_index()
fig_country = px.bar(top_countries, x="Country", y="TotalPrice",
                     color="TotalPrice", color_continuous_scale="Blues",
                     title="Top 10 Countries by Revenue")
fig_country.update_layout(margin=dict(t=40, b=0), coloraxis_showscale=False)
st.plotly_chart(fig_country, use_container_width=True)

# ── Download RFM ──────────────────────────────────────────────────────────────
st.markdown("---")
csv = rfm.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download RFM Segments CSV", csv,
                   file_name="taurus_rfm_segments.csv", mime="text/csv")
