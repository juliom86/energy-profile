import streamlit as st

TABS = ['one', 'two', 'three', 'four']

def tabs():
    st.markdown(
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
        unsafe_allow_html=True,
    )
    query_params = st.experimental_get_query_params()
    if "tab" in query_params:
        active_tab = query_params["tab"][0]
    else:
        active_tab = "one"

    if active_tab not in TABS:
        st.experimental_set_query_params(tab="one")
        active_tab = "one"

    li_items = "".join(f"""
        <li class="nav-item">
            <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
        </li>
        """ for t in TABS)
    tabs_html = f"""
        <ul class="nav nav-tabs">
        {li_items}
        </ul>
    """

    st.markdown(tabs_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if active_tab == "one":
        st.write("Tab one")
    elif active_tab == "two":
        st.write("Tab two")
    elif active_tab == "three":
        st.write("Tab three")
    elif active_tab == "four":
        st.write("Tab four")
    else:
        st.error("Information needed.")
