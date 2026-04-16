import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import io
import json
import numpy as np

st.set_page_config(
    page_title="ASIC Monitor Dashboard",
    page_icon="🏢",
    layout="wide"
)

st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1f4e79 0%, #366092 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-left: 4px solid #366092;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    np.random.seed(42)
    merchants = ['Jetstar Australia', 'Webjet Australia', 'eBay Australia', 'Big W', 'Ticketek', 'Harvey Norman', 'JB Hi-Fi', 'Bunnings', 'Woolworths', 'Coles']
    return pd.DataFrame({
        'MERCHANT_NAME': merchants,
        'ABN': [f"{np.random.randint(10,99)}{np.random.randint(100000000,999999999)}" for _ in merchants],
        'EXPOSURE_AUD': np.random.lognormal(15, 1, len(merchants)),
        'STATUS': np.random.choice(['HIGH', 'MEDIUM', 'LOW'], len(merchants)),
        'RISK_SCORE': np.random.uniform(0, 100, len(merchants)),
        'DAYS_OVERDUE': np.random.poisson(15, len(merchants))
    })

def main():
    st.markdown("""
    <div class="main-header">
        <h1>🏢 ASIC Monitor Dashboard</h1>
        <p>Real-time merchant risk monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_data()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>Total Merchants</h3><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>Total Exposure</h3><h2>${df["EXPOSURE_AUD"].sum()/1e6:.1f}M</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>High Risk</h3><h2>{len(df[df["STATUS"]=="HIGH"])}</h2></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><h3>Avg Risk Score</h3><h2>{df["RISK_SCORE"].mean():.1f}</h2></div>', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(df, x='MERCHANT_NAME', y='EXPOSURE_AUD', color='STATUS', title='Merchant Exposure by Risk')
        fig1.update_xaxis(tickangle=45)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.scatter(df, x='RISK_SCORE', y='EXPOSURE_AUD', color='STATUS', hover_name='MERCHANT_NAME', title='Risk vs Exposure')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Data table
    st.subheader("📋 Merchant Data")
    st.dataframe(df, use_container_width=True)
    
    # Download
    st.subheader("📥 Export Data")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df.to_csv(index=False)
        st.download_button("📄 Download CSV", csv, "asic_data.csv", "text/csv")
    
    with col2:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer) as writer:
            df.to_excel(writer, index=False)
        st.download_button("📊 Download Excel", buffer.getvalue(), "asic_data.xlsx")
    
    with col3:
        json_data = df.to_json(orient='records', indent=2)
        st.download_button("📋 Download JSON", json_data, "asic_data.json")

if __name__ == "__main__":
    main()
