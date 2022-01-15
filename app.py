import streamlit as st
import pandas as pd
import datetime
import time

# SETTING PAGE CONFIGURATION
st.set_page_config(
            page_title="Energy Profile",
            page_icon="🐍",
            layout="wide",
            initial_sidebar_state="auto")

# FUNCTIONS
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


# MAIN SECTION
col1, col2, col3 = st.columns(3)

# SIDEBAR SELECTION

st.sidebar.markdown(f"""
    # Energy Profile
    """)

st.sidebar.multiselect('Seleccione el lugar de búsqueda', [
    'Argentina', 'Misiones', 'Chubut', 'Santa Cruz', 'Neuquen',
    'Buenos Aires'
], ['Argentina'])


st.sidebar.date_input("Seleccione la fecha de inicio",
                      datetime.date(2022, 1, 1))

st.sidebar.date_input("Seleccione la fecha de fin", datetime.date(2022, 1, 1))


FONT_SIZE_CSS = f"""
<style>
h1 {{
    font-size: 40px !important;
    margin-top: 0px !important;
    padding-top: 0px !important;
}}
</style>
"""
st.write(FONT_SIZE_CSS, unsafe_allow_html=True)


# DATA DISPLAY PAGE

my_bar = st.progress(0)



if st.sidebar.button('Solicitar información'):
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1)

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
