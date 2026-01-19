import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ------------------------------------
# CONFIG GENERAL
# ------------------------------------
st.set_page_config(
    page_title="Demo Analítica EDA | Ciencia de Datos con Streamlit",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------
# PALETA CORPORATIVA
# ------------------------------------
PRIMARY = "#2563EB"
SECONDARY = "#9333EA"
SUCCESS = "#16A34A"
WARNING = "#F59E0B"
DANGER = "#DC2626"
GRAY = "#6B7280"

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#E5E7EB",
    "axes.labelcolor": GRAY,
    "xtick.color": GRAY,
    "ytick.color": GRAY,
    "font.size": 11
})

# ------------------------------------
# HTML + CSS (UI/UX PRO)
# ------------------------------------
st.markdown("""
<style>
body {
    background-color: #F8FAFC;
    font-family: Inter, sans-serif;
}

.hero {
    background: linear-gradient(90deg, #2563EB, #9333EA);
    padding: 45px;
    border-radius: 22px;
    color: white;
    margin-bottom: 35px;
}

.kpi {
    padding: 24px;
    border-radius: 18px;
    color: white;
    text-align: center;
    box-shadow: 0 14px 35px rgba(0,0,0,0.15);
}

.blue { background: linear-gradient(135deg, #2563EB, #1E40AF); }
.purple { background: linear-gradient(135deg, #9333EA, #6B21A8); }
.green { background: linear-gradient(135deg, #16A34A, #065F46); }
.orange { background: linear-gradient(135deg, #F59E0B, #B45309); }

.section-title {
    font-size: 26px;
    font-weight: 700;
    margin-top: 45px;
    margin-bottom: 10px;
}

.insight {
    background: #EFF6FF;
    padding: 28px;
    border-left: 6px solid #2563EB;
    border-radius: 16px;
    margin-top: 30px;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------
# HERO / TÍTULO PRINCIPAL
# ------------------------------------
st.markdown("""
<div class="hero">
    <h1>Demo Analítica EDA | Ciencia de Datos con Streamlit</h1>
    <h3 style="font-weight:400; opacity:0.9;">
        Executive Sales Analytics Dashboard
    </h3>
    <p style="margin-top:10px; font-size:16px; opacity:0.85;">
        Desarrollado por <b>Mauricio Poveda</b> · Exploratory Data Analysis · BI & Storytelling
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------
# DATASET SINTÉTICO
# ------------------------------------
np.random.seed(42)

dates = pd.date_range(end=datetime.today(), periods=365)
regions = ["Norte", "Centro", "Sur", "Occidente"]
categories = ["Tecnología", "Hogar", "Retail"]

data = []
for d in dates:
    for r in regions:
        for c in categories:
            price = np.random.uniform(80, 300)
            units = np.random.poisson(22)
            sales = price * units
            data.append([d, r, c, price, units, sales])

df = pd.DataFrame(
    data,
    columns=["date", "region", "category", "price", "units", "sales"]
)

# ------------------------------------
# EXPORT CSV PARA POWER BI
# ------------------------------------
df.to_csv("sales_powerbi_demo.csv", index=False)

# ------------------------------------
# PANEL DE FILTROS (UX PRO)
# ------------------------------------
st.sidebar.markdown("## 🎛️ Panel de Control")

regions_f = st.sidebar.multiselect(
    "Regiones",
    df["region"].unique(),
    df["region"].unique()
)

categories_f = st.sidebar.multiselect(
    "Categorías",
    df["category"].unique(),
    df["category"].unique()
)

price_f = st.sidebar.slider(
    "Rango de Precio",
    int(df.price.min()),
    int(df.price.max()),
    (100, 250)
)

df_f = df[
    (df.region.isin(regions_f)) &
    (df.category.isin(categories_f)) &
    (df.price.between(price_f[0], price_f[1]))
]

# ------------------------------------
# KPIs CON DEGRADADO
# ------------------------------------
k1, k2, k3, k4 = st.columns(4)

k1.markdown(f"""
<div class="kpi blue">
<h4>Total Sales</h4>
<h2>${df_f.sales.sum():,.0f}</h2>
</div>
""", unsafe_allow_html=True)

k2.markdown(f"""
<div class="kpi purple">
<h4>Units Sold</h4>
<h2>{df_f.units.sum():,}</h2>
</div>
""", unsafe_allow_html=True)

k3.markdown(f"""
<div class="kpi green">
<h4>Avg Price</h4>
<h2>${df_f.price.mean():,.0f}</h2>
</div>
""", unsafe_allow_html=True)

k4.markdown(f"""
<div class="kpi orange">
<h4>Active Regions</h4>
<h2>{df_f.region.nunique()}</h2>
</div>
""", unsafe_allow_html=True)

# ------------------------------------
# GRAFICA 1 – SALES POR REGION
# ------------------------------------
st.markdown('<div class="section-title">📍 Desempeño por Región</div>', unsafe_allow_html=True)

sales_region = df_f.groupby("region")["sales"].sum().sort_values()

fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.barh(sales_region.index, sales_region.values, color=PRIMARY)
ax1.set_title("La región Centro lidera el ingreso total")
ax1.grid(axis="x", alpha=0.3)
st.pyplot(fig1)

# ------------------------------------
# GRAFICA 2 – TENDENCIA TEMPORAL
# ------------------------------------
trend = df_f.groupby("date")["sales"].sum()

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(trend.index, trend.values, color=SECONDARY, linewidth=2)
ax2.fill_between(trend.index, trend.values, alpha=0.15, color=SECONDARY)
ax2.set_title("Evolución anual de las ventas")
ax2.grid(alpha=0.3)
st.pyplot(fig2)

# ------------------------------------
# GRAFICA 3 – MIX DE CATEGORÍAS
# ------------------------------------
cat_sales = df_f.groupby("category")["sales"].sum()

fig3, ax3 = plt.subplots(figsize=(6, 4))
ax3.pie(
    cat_sales,
    labels=cat_sales.index,
    autopct="%1.1f%%",
    colors=[PRIMARY, SUCCESS, WARNING]
)
ax3.set_title("Distribución de ventas por categoría")
st.pyplot(fig3)

# ------------------------------------
# GRAFICA 4 – PRECIO VS VOLUMEN
# ------------------------------------
fig4, ax4 = plt.subplots(figsize=(7, 4))
ax4.scatter(df_f.price, df_f.units, alpha=0.4, color=PRIMARY)
ax4.set_title("Relación entre precio y volumen")
ax4.set_xlabel("Precio")
ax4.set_ylabel("Unidades")
ax4.grid(alpha=0.3)
st.pyplot(fig4)

# ------------------------------------
# GRAFICA 5 – UNIDADES PROMEDIO POR REGIÓN
# ------------------------------------
units_region = df_f.groupby("region")["units"].mean()

fig5, ax5 = plt.subplots(figsize=(8, 4))
ax5.bar(units_region.index, units_region.values, color=SUCCESS)
ax5.set_title("Promedio de unidades vendidas por región")
ax5.grid(axis="y", alpha=0.3)
st.pyplot(fig5)

# ------------------------------------
# INSIGHT EJECUTIVO
# ------------------------------------
st.markdown(f"""
<div class="insight">
<b>Insight Ejecutivo:</b><br>
La región <b>{sales_region.idxmax()}</b> mantiene el liderazgo tanto en ingresos
como en volumen promedio. Este comportamiento sugiere oportunidades claras
para estrategias de optimización de precios sin afectar la demanda.
</div>
""", unsafe_allow_html=True)

# ------------------------------------
# FOOTER
# ------------------------------------
st.markdown("<hr><center>Demo Analítica EDA · Ciencia de Datos · Streamlit → Power BI</center>", unsafe_allow_html=True)
