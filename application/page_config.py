import streamlit as st

def run():
    st.set_page_config(page_title="Energy Profile",
                        page_icon="🐍",
                        layout="wide",
                        initial_sidebar_state="auto")

    # STYILING

    FONT_SIZE_CSS = f"""
    <style>
    h1 {{
        font-size: 40px !important;
        margin-top: 0px !important;
        padding-top: 0px !important;
    }}
    .js-plotly-plot.plotly.modebar {{
        right: 120px !important;
    }}
    .modebar.modebar--hover.ease-bg {{
        right: 120px !important;
    }}
    .css-6awftf.e19lei0e0 {{
        position: absolute !important;
        right: 85px !important;
    }}
    </style>
    """

    st.write(FONT_SIZE_CSS, unsafe_allow_html=True)
