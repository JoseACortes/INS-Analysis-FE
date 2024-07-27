import streamlit as st


import INS_Analysis
import os
import plotly.express as px
from streamlit_plotly_events import plotly_events
import pandas as pd
from toolbox import fileOptions

import states

if 'Spectrums' not in st.session_state:
    st.session_state.Spectrums = {}

st.page_link("server.py", label="Home", icon="🏠")

st.title('Parse Spectrum')


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
            bins, vals = INS_Analysis.read(_tmp, **opts)
            st.session_state.Spectrums[filename] = {'bins': bins, 'vals': vals}
            # st.session_state.Analyzer.addSpectrum(_tmp, filename, **opts)
            os.remove(_tmp)
for label in st.session_state.Spectrums:
    bins = st.session_state.Spectrums[label]['bins']
    vals = st.session_state.Spectrums[label]['vals']
    fig1.add_scatter(x=bins, y=vals, mode='lines', name=label)
plotly_events(fig1, 'fig1')

if st.button('Parse'):
    # df = pd.DataFrame.from_dict(st.session_state.Spectrums)
    dfs = []
    for file in st.session_state.Spectrums:
        df = pd.DataFrame(st.session_state.Spectrums[file])
        df = df.set_index('bins')
        dfs.append(df)
    df = pd.concat(dfs, axis=1, keys=[file.split('.')[0] for file in st.session_state.Spectrums])
    df.columns = df.columns.map(lambda x: f'{x[0]}_{x[1]}')
    df = df.reset_index()
    df = df.sort_values('bins')
    st.write(df)