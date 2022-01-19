import streamlit as st
import time

def run():
    api_request_progress_bar = st.progress(0)
    col1, col2, col3 = st.columns(3)

    if st.sidebar.button('Solicitar información'):
        for percent_complete in range(100):
            time.sleep(0.01)
            api_request_progress_bar.progress(percent_complete + 1)

        api_request_progress_bar.empty()

        with col1:
            st.header("Grafico 1")
            st.write('Seleccionado')

        with col2:
            st.header("Grafico 1")
            st.write('Seleccionado')

        with col3:
            st.header("Grafico 1")
            st.write('Seleccionado')
            # st.download_button(
            #     label="Download data as CSV",
            #     data={'data': convert_df(df)},
            #     file_name='large_df.csv',
            #     mime='text/csv',
            # )

    else:
        st.write('')
