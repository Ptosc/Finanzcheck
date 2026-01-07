import streamlit as st
import analyse

st.set_page_config(
    initial_sidebar_state='expanded',
    layout='wide'
    )

analyse.render()