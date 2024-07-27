import streamlit as st
import INS_Analysis

Analyzer = INS_Analysis.Analyzer()
st.session_state.Analyzer = Analyzer

st.session_state.Spectrums = {}
st.session_state.Spectrograms = {}