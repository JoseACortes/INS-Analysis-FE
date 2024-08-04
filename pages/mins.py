import streamlit as st

# from ..states import Analyzer

st.page_link("server.py", label="Home", icon="🏠")

import INS_Analysis
import os
import plotly.express as px
from streamlit_plotly_events import plotly_events
import pandas as pd
from toolbox import fileOptions


if 'Analyzer' not in st.session_state:
    st.session_state.Analyzer = INS_Analysis.Analyzer()

st.title('MINS')

import_tab, area_tab, cal_tab, proc_tab = st.tabs(["Import Files", "Calculate Areas", "Calibrate", "Process"])
window_labels = ['Si1', 'Si2C1']

with import_tab:
    fig1 = px.line()
    fig1.update_xaxes(title_text='Energy (MeV)')
    fig1.update_yaxes(title_text='Counts')   
    files = st.file_uploader('Upload file(s)', type=['csv', 'mctal', 'mca'], accept_multiple_files=True)
    file_options = fileOptions.file_options(files)
    if st.button('Add files'):
        for file in files:
            filename = file.name
            name = filename.split('.')[0]
            ext = filename.split('.')[-1]
            _tmp = 'temp.'+ext
            with open(_tmp, 'wb') as f:
                f.write(file.getvalue())
                f.close()
                opts = file_options[filename]
                st.session_state.Analyzer.addSpectrum(_tmp, name, **opts)
                os.remove(_tmp)
    for label in st.session_state.Analyzer.spectrums:
        bins = st.session_state.Analyzer.spectrums[label]['bins']
        vals = st.session_state.Analyzer.spectrums[label]['vals']
        fig1.add_scatter(x=bins, y=vals, mode='lines', name=label)
    plotly_events(fig1, 'fig1')

with area_tab:
    with st.expander('Area Configuration'):
        baselineFunction = st.selectbox('Baseline Function', ['point_slope', 'point_slope_super', 'exp_falloff', 'fat_tail', 'None'])    
        peakFunction = st.selectbox('Peak Function', ['gaus', 'None'])
        si_window_min_col, si_window_max_col = st.columns(2)
        with si_window_min_col:
            si_window_min = st.number_input('Silicone Window Min', 0.0, 14.0, 1.63)
        with si_window_max_col:
            si_window_max = st.number_input('Silicone Window Max', 0.0, 14.0, 2.0)
        si_window = [si_window_min, si_window_max]
        c_window_min_col, c_window_max_col = st.columns(2)
        with c_window_min_col:
            c_window_min = st.number_input('Carbon Window Min', 0.0, 14.0, 4.2)
        with c_window_max_col:
            c_window_max = st.number_input('Carbon Window Max', 0.0, 14.0, 4.7)
        c_window = [c_window_min, c_window_max]

        geb_check = st.checkbox('GEB Assumption', value=False)
        geb = None
        if geb_check:
            geba, gebb, gebc = st.columns(3)
            with geba:
                geb_a = st.number_input('a', -100.0000000, 100.0000000, -0.0073, 0.00000001, format="%0.4f")
            with gebb:
                geb_b = st.number_input('b', -100.0000000, 100.0000000, 0.078, 0.00000001, format="%0.4f")
            with gebc:
                geb_c = st.number_input('c', -100.0000000, 100.0000000, 0.0, 0.00000001, format="%0.4f")
            geb = {'a': geb_a, 'b': geb_b, 'c': geb_c}
    
    if len(st.session_state.Analyzer.spectrums) == 0:
        st.warning('No spectrums found')
    else:
        spec_labels = list(st.session_state.Analyzer.spectrums.keys())
    if st.button('Fit Areas'):
        area_results = st.session_state.Analyzer.calcPeakAreas(spec_labels, returnFits=True, peakWindows={'Si1': si_window, 'Si2C1': c_window}, baselineFunction=baselineFunction, peakFunction=peakFunction, geb=geb)
    if len(st.session_state.Analyzer.spectrums) != 0:
        df = st.session_state.Analyzer.toDataFrame()
        st.write(df[['label', 'areas', 'area_calc_failed']])
    fig2 = px.line()
    ls = st.multiselect('Select spectrums to display', st.session_state.Analyzer.spectrums.keys())
    for label in ls:
        spec = st.session_state.Analyzer.spectrums[label]
        bins = spec['bins']
        vals = spec['vals']
        # print(spec)
        fig2.add_scatter(x=bins, y=vals, mode='lines', name=label)
        if spec['fits']['Si1']['bins'] is not None:
            
            binss = spec['fits']['Si1']['bins']
            baseline = spec['fits']['Si1']['baseline']
            peak = spec['fits']['Si1']['peak']
            fig2.add_scatter(x=binss, y=peak, mode='lines', name=label+' Si1 peak', marker_color='red')
            fig2.add_scatter(x=binss, y=baseline, mode='lines', name=label+' Si1 baseline', marker_color='blue')

        if spec['areas']['Si2C1'] is not None:
            binss = spec['fits']['Si2C1']['bins']
            baseline = spec['fits']['Si2C1']['baseline']
            peak = spec['fits']['Si2C1']['peak']
            fig2.add_scatter(x=binss, y=peak, mode='lines', name=label+' Si2C1 peak', marker_color='red')
            fig2.add_scatter(x=binss, y=baseline, mode='lines', name=label+' Si2C1 baseline', marker_color='blue')
    # turn off legend
    fig2.update_layout(showlegend=False)
    plotly_events(fig2, 'fig2')
    
with cal_tab:
    with st.expander('Calibration Configuration'):
        calib = st.selectbox('Calibration', ['original', 'none'])
    fig = px.line()
    fig.update_xaxes(title_text='Energy (MeV)')
    fig.update_yaxes(title_text='Counts')   
    if len(st.session_state.Analyzer.spectrums) == 0:
        labels = st.multiselect('Select spectrums for calibration', [])
        st.warning('No spectrums found')
    else:
        labels = st.multiselect('Select spectrums for calibration', st.session_state.Analyzer.spectrums.keys())
        labels = list(set(labels))
        cailb_files_df = st.session_state.Analyzer.toDataFrame().set_index('label')[['vals', 'true_comp', 'areas']]
        
        for label in window_labels:
            cailb_files_df['True '+label] = cailb_files_df['true_comp'].apply(lambda x: x[label])
            cailb_files_df[label+' Area'] = cailb_files_df['areas'].apply(lambda x: x[label])
        
        cailb_files_df = cailb_files_df.drop('true_comp', axis=1)
        cailb_files_df = cailb_files_df.drop('areas', axis=1)
        
        cailb_files_df = cailb_files_df.loc[labels]

        cailb_files_df = st.data_editor(
            cailb_files_df,
            column_config={
                'vals': st.column_config.LineChartColumn(
                    'vals',
                    width="small",
                    ),
            }
            )
        
    if st.button('Calibrate'):
        for label in labels:
            st.session_state.Analyzer.spectrums[label]['true_comp']['Si1'] = cailb_files_df.loc[label]['True Si1']
            st.session_state.Analyzer.spectrums[label]['true_comp']['Si2C1'] = cailb_files_df.loc[label]['True Si2C1']
        cal = st.session_state.Analyzer.calibrate(labels)
        st.write(cal)
    if labels:
        for label in labels:
            bins = st.session_state.Analyzer.spectrums[label]['bins']
            vals = st.session_state.Analyzer.spectrums[label]['vals']
            fig.add_scatter(x=bins, y=vals, mode='lines', name=label)
    plotly_events(fig, 'clibrate fig')

with proc_tab:
    with st.expander('Processing Configuration'):
        # checkbox to compile spectrum data
        spec_comp_check = st.checkbox('Compile Spectrum Data', value=False)
        # checkbox to compile results
        res_comp_check = st.checkbox('Compile Results', value=True)
    st.write('If no spectrums are selected, all non-error spectrums will be processed')
    if len(st.session_state.Analyzer.spectrums) == 0:
        st.warning('No spectrums found')
    else:
        labels = st.multiselect('Select spectrums for proccessing', st.session_state.Analyzer.spectrums.keys())
        labels = list(set(labels))
        if len(labels) == 0:
            labels = None
    if st.button('Process'):
        st.session_state.Analyzer.applyCalibrationAreas(labels)
        if len(st.session_state.Analyzer.spectrums) != 0:
            _df = st.session_state.Analyzer.toDataFrame()
            if spec_comp_check:
                specs_df = _df[['label', 'bins', 'vals', 'fits']]
                __df = {}
                for wl in window_labels:
                    specs_df[wl+'_fit_bins'] = specs_df['fits'].apply(lambda x: x[wl]['bins'])
                    specs_df[wl+'_fit_baseline'] = specs_df['fits'].apply(lambda x: x[wl]['baseline'])
                    specs_df[wl+'_fit_peak'] = specs_df['fits'].apply(lambda x: x[wl]['peak'])
                specs_df = specs_df.drop('fits', axis=1)
                specs_df = specs_df.set_index('label')
                labels = specs_df.index

                for label in labels:
                    __df[label+'_bins'] = specs_df.loc[label]['bins']
                    __df[label+'_vals'] = specs_df.loc[label]['vals']
                    for wl in window_labels:
                        if specs_df.loc[label][wl+'_fit_bins'] is not None:
                            __df[label+'_'+wl+'_fit_bins'] = specs_df.loc[label][wl+'_fit_bins'].tolist()
                            __df[label+'_'+wl+'_fit_baseline'] = specs_df.loc[label][wl+'_fit_baseline']#.tolist()
                            __df[label+'_'+wl+'_fit_peak'] = specs_df.loc[label][wl+'_fit_peak']#.tolist()
                # find the longest list
                max_len = 0
                for key in __df:
                    if 'bins' in key:
                        if len(__df[key]) > max_len:
                            max_len = len(__df[key])
                for key in __df:
                    if len(__df[key]) < max_len:
                        __df[key] = __df[key] + [None]*(max_len-len(__df[key]))
                st.write(pd.DataFrame(__df))
            if res_comp_check:
                
                results_df = _df[['label', 'true_comp', 'pred_comp', 'areas', 'for_calib', 'area_calc_failed']]
                results_df = results_df.set_index('label')
                # st.write(results_df)
                __df = {}
                __df['true_Si1'] = results_df['true_comp'].apply(lambda x: x['Si1'])
                __df['true_Si2C1'] = results_df['true_comp'].apply(lambda x: x['Si2C1'])
                __df['pred_Si1'] = results_df['pred_comp'].apply(lambda x: x['Si1'])
                __df['pred_Si2C1'] = results_df['pred_comp'].apply(lambda x: x['Si2C1'])
                __df['Si1_area'] = results_df['areas'].apply(lambda x: x['Si1'])
                __df['Si2C1_area'] = results_df['areas'].apply(lambda x: x['Si2C1'])
                __df['for_calib'] = results_df['for_calib']
                __df['area_calc_failed'] = results_df['area_calc_failed']
                st.write(pd.DataFrame(__df))