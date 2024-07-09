import streamlit as st

def file_options(uploaded_file):
    file_options = {}
    with st.expander('File Information'):
        # default options
        st.write('MCTAL Default Options:')

        tally = st.number_input('Tally', 0, None, 8)
        time = st.number_input('Time', 0, None, 0)
        nps = st.number_input('NPS', 0, None, 1000000000)
        defaul_mctal_options = {'tally': tally, 'time': time, 'nps': nps}
        if uploaded_file is not None:
            for file in uploaded_file:
                filename = file.name
                ext = filename.split('.')[-1]
                if ext == 'mctal':
                    # horizontal dividers
                    st.divider()
                    col0, col1, col2 = st.columns(3)
                    with col0:
                        st.write(f"{file.name}")
                    with col1:
                        st.write(f"File size: {file.size} bytes")
                    with col2:
                        st.write(f"File extension: {file.name.split('.')[-1]}")
                    # vertical columns
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write('tally:')
                        tally = st.number_input(f"{file.name} Tally", 0, None, defaul_mctal_options['tally'], label_visibility='collapsed')
                    with col2:
                        st.write('time:')
                        time = st.number_input(f"{file.name} Time", 0, None, defaul_mctal_options['time'], label_visibility='collapsed')
                    with col3:
                        st.write('nps:')
                        nps = st.number_input(f"{file.name} NPS", 0, None, defaul_mctal_options['nps'], label_visibility='collapsed')
                    
                    file_options[filename] = {'tally': tally, 'start_time_bin': time, 'nps': nps}
                else:
                    st.write(f"{file.name}")
    return file_options