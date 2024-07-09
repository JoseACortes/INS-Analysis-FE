import streamlit as st
import INS_Analysis

Analyzer = INS_Analysis.Analyzer()
st.session_state.Analyzer = Analyzer

st.page_link("server.py", label="Home", icon="🏠")
st.page_link("pages/mins.py", label="MINS", icon="1️⃣")
