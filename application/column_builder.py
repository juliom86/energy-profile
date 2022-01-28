import streamlit as st

def run(col, figure, html_markdown):
    if html_markdown:
        st.title(html_markdown['title'])
        st.subheader(html_markdown['subheader'])
        st.write(html_markdown['description'])

    if figure:
        col.plotly_chart(figure)
