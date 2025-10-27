import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------
# Datos
# ---------------------------
df_mercat = pd.DataFrame({
    'Mercat': ['Domèstic', 'Estranger', 'Total'],
    'Viatgers': [289817, 415444, 705261],
    'Pernoctacions': [842852, 1744508, 2587360],
    'Estada mitjana': [2.9, 4.2, 3.7]
})

df_interanual = pd.DataFrame({
    'Indicador': ['Viatgers', 'Pernoctacions', 'Estada mitjana'],
    'Domèstic': [0.054, 0.029, -0.036],
    'Estranger': [0.068, -0.014, -0.065]
})

df_comarca = pd.DataFrame({
    'Comarca': ['Maresme', 'Baix Llobregat', 'Vallès Occidental', 'Garraf', 'Anoia',
                'Vallès Oriental', 'Osona', 'Alt Penedès', 'Berguedà', 'Bages', 'Moianès'],
    'Ocupació (%)': [0.871, 0.789, 0.779, 0.753, 0.694, 0.66, 0.656, 0.644, 0.61, 0.575, 0.351],
    'Obertura (%)': [0.976, 0.985, 1.0, 0.962, 0.907, 0.99, 0.966, 0.975, 0.959, 0.967, 0.768]
})

# ---------------------------
# Layout
# ---------------------------
st.set_page_config(layout="wide")
st.title("🏙️ Evolució del turisme i Pisos turistics a Barcelona")

# ---------------------------
# PDF no topo
# ---------------------------
with open("./pdf/informe.pdf", "rb") as f:
    pdf_bytes = f.read()

st.markdown(
    f'<a href="file://{pdf_path}" target="_blank" style="font-size:22px; font-weight:bold;">📄 Obrir indicadors Turistics a l´entorn de Barcelona</a>',
    unsafe_allow_html=True
)
#st.download_button(label="⬇️ Baixar PDF", data=pdf_bytes, file_name="informe.pdf", mime="application/pdf")

# ---------------------------
# Filtros laterales
# ---------------------------
st.sidebar.header("🎛️ Filtres")
mercat_seleccionat = st.sidebar.radio("Selecciona el mercat", df_mercat['Mercat'].tolist())
comarca_seleccionada = st.sidebar.selectbox("Selecciona la comarca", ["*"] + df_comarca['Comarca'].tolist())

# ---------------------------
# KPIs principales
# ---------------------------
total_viatgers = df_mercat['Viatgers'].sum()
total_pernoctacions = df_mercat['Pernoctacions'].sum()
estada_mitjana = df_mercat['Estada mitjana'].mean()

st.markdown(
    f"<div style='display:flex; gap:20px; flex-wrap:wrap;'>"
    f"<div style='flex:1; min-width:150px; padding:15px; background:#ffe066; text-align:center; border-radius:10px; box-shadow:2px 2px 8px rgba(0,0,0,0.2);'>"
    f"<h4>Total Viatgers</h4><p style='font-size:20px'>{total_viatgers:,}</p></div>"
    f"<div style='flex:1; min-width:150px; padding:15px; background:#6a4c93; color:white; text-align:center; border-radius:10px; box-shadow:2px 2px 8px rgba(0,0,0,0.2);'>"
    f"<h4>Total Pernoctacions</h4><p style='font-size:20px'>{total_pernoctacions:,}</p></div>"
    f"<div style='flex:1; min-width:150px; padding:15px; background:#ff6b6b; color:white; text-align:center; border-radius:10px; box-shadow:2px 2px 8px rgba(0,0,0,0.2);'>"
    f"<h4>Estada Mitjana</h4><p style='font-size:20px'>{estada_mitjana:.1f} nits</p></div>"
    f"</div>", unsafe_allow_html=True
)

# ---------------------------
# Gráficos lado a lado: Viatgers/Pernoctacions e Estada Mitjana (pizza)
# ---------------------------
mercat_data = df_mercat[df_mercat['Mercat'] == mercat_seleccionat]
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Viatgers i Pernoctacions")
    df_vp = pd.DataFrame({
        'Categoria': ['Viatgers', 'Pernoctacions'],
        'Valor': [mercat_data['Viatgers'].values[0], mercat_data['Pernoctacions'].values[0]]
    })

    fig_vp = go.Figure()

    fig_vp.add_trace(go.Bar(
        y=df_vp['Categoria'],
        x=df_vp['Valor'],
        orientation='h',
        text=df_vp['Valor'],
        textposition='outside',
        marker=dict(color=['#FF7F0E', '#2CA02C'])
    ))

    fig_vp.update_layout(
        height=300,
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig_vp, use_container_width=True)

with col2:
    st.markdown("### Estada Mitjana (nits)")
    fig_pie = go.Figure(data=[go.Pie(
        labels=df_mercat['Mercat'],
        values=df_mercat['Estada mitjana'],
        hole=0.3,
        marker=dict(colors=['#FF7F0E', '#2CA02C', '#9467BD'])
    )])

    fig_pie.update_traces(textinfo='label+value', textfont_size=16)
    fig_pie.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ---------------------------
# KPIs per Comarca
# ---------------------------
st.markdown("### KPIs per Comarca")
if comarca_seleccionada == "*":
    kpi_ocupacio = df_comarca['Ocupació (%)'].mean()
    kpi_obertura = df_comarca['Obertura (%)'].mean()
    kpi_max_ocupacio = df_comarca['Ocupació (%)'].max()
    kpi_min_ocupacio = df_comarca['Ocupació (%)'].min()
else:
    comarca_data = df_comarca[df_comarca['Comarca']==comarca_seleccionada]
    kpi_ocupacio = comarca_data['Ocupació (%)'].values[0]
    kpi_obertura = comarca_data['Obertura (%)'].values[0]
    kpi_max_ocupacio = kpi_ocupacio
    kpi_min_ocupacio = kpi_ocupacio

st.markdown(
    """
    <div style='display:flex; gap:20px; flex-wrap:wrap; margin-top:30px;'>
        <div style='flex:1; min-width:150px; padding:15px; background:#ffe066; text-align:center; border-radius:10px; box-shadow:2px 2px 8px rgba(0,0,0,0.2);'>
            <h4>Total Viatgers</h4>
            <p style='font-size:20px'>289817</p>
        </div>
        <div style='flex:1; min-width:150px; padding:15px; background:#6a4c93; color:white; text-align:center; border-radius:10px; box-shadow:2px 2px 8px rgba(0,0,0,0.2);'>
            <h4>Total Pernoctacions</h4>
            <p style='font-size:20px'>842852</p>
        </div>
        <div style='flex:1; min-width:150px; padding:15px; background:#ff6b6b; color:white; text-align:center; border-radius:10px; box-shadow:2px 2px 8px rgba(0,0,0,0.2);'>
            <h4>Estada Mitjana</h4>
            <p style='font-size:20px'>3.7 nits</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Gráfico Viatgers por Comarca
# ---------------------------
st.markdown("### Número de Viatgers per Comarca")
df_comarca_viatgers = df_comarca[['Comarca', 'Ocupació (%)']]

fig_comarca = go.Figure()

fig_comarca.add_trace(go.Bar(
    x=df_comarca_viatgers['Comarca'],
    y=df_comarca_viatgers['Ocupació (%)'],
    text=df_comarca_viatgers['Ocupació (%)'],
    textposition='outside',
    marker=dict(color='lightblue')
))

fig_comarca.update_layout(
    height=400,
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis_title="Comarca",
    yaxis_title="Ocupació (%)"
)

st.plotly_chart(fig_comarca, use_container_width=True)



