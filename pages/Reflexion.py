import streamlit as st
import reflexion

st.set_page_config(
    initial_sidebar_state='expanded',
    layout='wide'
    )

reflexion.render()

