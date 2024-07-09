import streamlit as st

st.page_link("server.py", label="Home", icon="🏠")

import INS_Analysis
import os
import plotly.express as px
from streamlit_plotly_events import plotly_events
import pandas as pd
from toolbox import fileOptions

st.title('MINS')

tab1, tab2, tab3 = st.tabs(["Import Files", "Calibrate", "Process"])

with tab1:
    fig1 = px.line()
    fig1.update_xaxes(title_text='Energy (MeV)')
    fig1.update_yaxes(title_text='Counts')   
    files = st.file_uploader('Upload file(s)', type=['csv', 'mctal', 'mca'], accept_multiple_files=True)
    file_options = fileOptions.file_options(files)
    if st.button('Add files'):
        for file in files:
            filename = file.name
            ext = filename.split('.')[-1]
            _tmp = 'temp.'+ext
            with open(_tmp, 'wb') as f:
                f.write(file.getvalue())
                f.close()
                opts = file_options[filename]
                st.session_state.Analyzer.addSpectrum(_tmp, filename, **opts)
                os.remove(_tmp)
    for label in st.session_state.Analyzer.spectrums:
        bins = st.session_state.Analyzer.spectrums[label]['bins']
        vals = st.session_state.Analyzer.spectrums[label]['vals']
        fig1.add_scatter(x=bins, y=vals, mode='lines', name=label)
    plotly_events(fig1, 'fig1')

with tab2:
    fig = px.line()
    fig.update_xaxes(title_text='Energy (MeV)')
    fig.update_yaxes(title_text='Counts')   
    if len(st.session_state.Analyzer.spectrums) == 0:
        st.warning('No spectrums to calibrate')
    else:
        labels = st.multiselect('Select spectrums for calibration', st.session_state.Analyzer.spectrums.keys())

        cailb_files_df = pd.DataFrame(st.session_state.Analyzer.spectrums).T[['vals', 'areas', 'fits', 'true_comp', 'pred_comp', 'for_calib']]
        cailb_files_df = cailb_files_df.loc[labels]
        st.dataframe(
            cailb_files_df,
            column_config={
                'vals': st.column_config.LineChartColumn(
                    'vals',
                    width="medium",
                    ),
            }
            )

        if st.button('Calibrate'):
            pass
        for label in labels:
            bins = st.session_state.Analyzer.spectrums[label]['bins']
            vals = st.session_state.Analyzer.spectrums[label]['vals']
            fig.add_scatter(x=bins, y=vals, mode='lines', name=label)
        plotly_events(fig, 'clibrate fig')

with tab3:
    if st.button('Process'):
        pass

