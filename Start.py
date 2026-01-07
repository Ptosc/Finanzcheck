import streamlit as st
from random import choice

# --- Page Config ---
st.set_page_config(
    page_title="Finanz-Dashboard",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Quotes ---
MONEY_QUOTES = [
    "Jeder Euro ist ein Samen für deine Freiheit.",
    "Klarheit im Geld bringt Ruhe im Geist.",
    "Du bestimmst, wohin dein Geld fließt.",
    "Selbstkontrolle ist Freiheit, kein Verzicht.",
    "Dein Geld folgt deiner Aufmerksamkeit."
]

# --- Global Styles (Dark-Mode safe) ---
st.markdown("""
<style>
/* Remove top padding and header */
.block-container {
    padding-top: 1.5rem !important;
}
header {
    visibility: hidden;
}

/* Titles */
.big-title {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.3em;
    text-align: center;
    color: var(--text-color);
}
.subtitle {
    font-size: 1.25rem;
    color: var(--text-color);
    opacity: 0.7;
    text-align: center;
    margin-bottom: 2em;
}

/* Quote card */
.quote {
    font-size: 1.35rem;
    font-style: italic;
    text-align: center;
    background-color: var(--secondary-background-color);
    color: var(--text-color);
    padding: 1.25em 1.5em;
    border-radius: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    margin-bottom: 2em;
}

/* Section cards */
.section-card {
    padding: 1.5em;
    border-radius: 16px;
    background-color: var(--background-color);
    box-shadow: 0 8px 20px rgba(0,0,0,0.05);
    border: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 1.5em;
    text-align: center;
}

.section-card h3 {
    margin-bottom: 0.5em;
    color: var(--text-color);
}

.section-card p {
    color: var(--text-color);
    opacity: 0.8;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown(
    '<div class="big-title">💸 Dein Finanz-Überblick</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Bewusst ausgeben. Klar entscheiden. Ruhiger leben.</div>',
    unsafe_allow_html=True
)

# --- Random Quote ---
st.markdown(
    f'<div class="quote">“{choice(MONEY_QUOTES)}”</div>',
    unsafe_allow_html=True
)

# --- Navigation Hint ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.info("⬅️ Wähle links eine Seite, um deine Ausgaben zu analysieren.")

# --- Sections ---
st.markdown("---")
c1, c2, c3 = st.columns(3)

# 📊 Analyse
with c1:
    st.markdown("""
    <div class="section-card">
        <h3>📊 Analyse</h3>
        <p>Verstehe, <b>wo</b> dein Geld hingeht – nach Monat, Kategorie und Verlauf.</p>
    </div>
    """, unsafe_allow_html=True)

# 🧠 Reflexion
with c2:
    st.markdown("""
    <div class="section-card">
        <h3>🧠 Reflexion</h3>
        <p>Erkenne Muster, Impulse und Gewohnheiten hinter deinen Ausgaben.</p>
    </div>
    """, unsafe_allow_html=True)

# 🎯 System
with c3:
    st.markdown("""
    <div class="section-card">
        <h3>🎯 System</h3>
        <p>Setze Grenzen, triff ruhige Entscheidungen und schütze dein zukünftiges Ich.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- Footer ---
st.caption(
    "Gebaut mit Fokus auf Klarheit statt Kontrolle. Weniger Lärm, mehr Urteilskraft."
)
