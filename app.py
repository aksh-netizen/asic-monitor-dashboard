import streamlit as st
import pandas as pd

st.title("🏢 ASIC Monitor Dashboard")

# Simple data
data = {
    'Merchant': ['Jetstar', 'Webjet', 'eBay', 'Big W'],
    'Exposure': [50000000, 30000000, 20000000, 40000000],
    'Status': ['HIGH', 'MEDIUM', 'LOW', 'MEDIUM']
}

df = pd.DataFrame(data)

# Display
st.metric("Total Merchants", len(df))
st.dataframe(df)

# Download
csv = df.to_csv(index=False)
st.download_button("Download CSV", csv, "data.csv")

st.success("Dashboard is working! ✅")


