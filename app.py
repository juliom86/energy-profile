import streamlit as st
from application import page_config, sidebar, main
from application.functions import convert_df

# PAGE CONFIGURATION and STYLING
page_config.run()

# FUNCTIONS

# SIDEBAR SELECTION
selected_option = sidebar.run()

# MAIN SECTION
main.run(selected_option)
