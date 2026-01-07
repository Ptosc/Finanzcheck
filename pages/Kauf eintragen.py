import streamlit as st
import ausgabe

st.set_page_config(
    initial_sidebar_state='expanded',
    layout='wide'
    )

ausgabe.render()