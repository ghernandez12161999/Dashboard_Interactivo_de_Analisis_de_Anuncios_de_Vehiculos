import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------
# CONFIGURACIÓN DE PÁGINA
# -----------------------------
st.set_page_config(layout="wide")

# -----------------------------
# ESTILOS (PALETA BEIGE)
# -----------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #F5F5DC;
    }
    .metric-card {
        background-color: #FAF3E0;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# CARGA DE DATOS
# -----------------------------
df = pd.read_csv("vehicles_us.csv")

# -----------------------------
# SIDEBAR (FILTROS)
# -----------------------------
st.sidebar.header("Filtros dinámicos")

price_range = st.sidebar.slider(
    "Rango de precios",
    int(df['price'].min()),
    int(df['price'].max()),
    (int(df['price'].min()), int(df['price'].max()))
)

year_range = st.sidebar.slider(
    "Año del vehículo",
    int(df['model_year'].min()),
    int(df['model_year'].max()),
    (int(df['model_year'].min()), int(df['model_year'].max()))
)

filtered_df = df[
    (df['price'] >= price_range[0]) & (df['price'] <= price_range[1]) &
    (df['model_year'] >= year_range[0]) & (df['model_year'] <= year_range[1])
]

# -----------------------------
# HEADER
# -----------------------------
st.title("🚗 Dashboard Profesional de Anuncios de Coches")

# -----------------------------
# TARJETAS KPI
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"""
<div class="metric-card">
<h3>Precio promedio</h3>
<h2>${int(filtered_df['price'].mean())}</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="metric-card">
<h3>Total de autos</h3>
<h2>{filtered_df.shape[0]}</h2>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="metric-card">
<h3>Odómetro promedio</h3>
<h2>{int(filtered_df['odometer'].mean())}</h2>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div class="metric-card">
<h3>Año promedio</h3>
<h2>{int(filtered_df['model_year'].mean())}</h2>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# DATASET (OPCIONAL)
# -----------------------------
with st.expander("Ver dataset filtrado"):
    st.dataframe(filtered_df)

# -----------------------------
# HISTOGRAMA
# -----------------------------
st.subheader("Distribución de precios")

fig_hist = px.histogram(
    filtered_df,
    x="price",
    nbins=50,
    title="Distribución de precios",
    color_discrete_sequence=["#C2B280"]  # beige oscuro
)

st.plotly_chart(fig_hist, use_container_width=True)

# -----------------------------
# SCATTER
# -----------------------------
st.subheader("Relación entre odómetro y precio")

fig_scatter = px.scatter(
    filtered_df,
    x="odometer",
    y="price",
    color="model_year",
    title="Odómetro vs Precio",
    color_continuous_scale="earth"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------
# MAPA DE CALOR (CORRELACIÓN)
# -----------------------------
st.subheader("Mapa de calor de correlaciones")

# Seleccionar variables numéricas relevantes
corr = filtered_df[['price', 'odometer', 'model_year']].corr()

fig_heatmap = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='YlGnBu'
    )
)

fig_heatmap.update_layout(
    title="Correlación entre variables",
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# -----------------------------
# GRÁFICO EXTRA (BOXPLOT)
# -----------------------------
st.subheader("Distribución de precios por año")

fig_box = px.box(
    filtered_df,
    x="model_year",
    y="price",
    color_discrete_sequence=["#A67B5B"]
)

st.plotly_chart(fig_box, use_container_width=True)