import streamlit as st
from time import sleep
from datetime import datetime

KATEGORIEN = [
    "Alltag & Essen",
    "Freizeit & Soziales",
    "Kleidung & Pflege",
    "Bildung & Entwicklung",
    "Sparen & Rücklagen"
]
# -------------------------
# Helper: zentrale Initialisierung
# -------------------------
def init_state():
    # setdefault ist idempotent und sicher bei mehrfachen Aufrufen
    st.session_state.setdefault("page", "system")
    st.session_state.setdefault("kaufimpulse", [])
    st.session_state.setdefault("cooling_off_betrag", 30)

# -------------------------
# Sidebar Navigation
# -------------------------
def sidebar():
    st.sidebar.title("Navigation")

    pages = ["system", "kaufimpuls", "rules"]
    labels = {
        "system": "System-Übersicht",
        "kaufimpuls": "Kaufimpuls eintragen",
        "rules": "Regeln anpassen"
    }

    # Radio direkt mit Keys
    selected_key = st.sidebar.radio(
        "Seite wählen",
        options=pages,
        format_func=lambda x: labels[x],  # zeigt Labels an
        index=pages.index(st.session_state.page)
    )

    # Page-State synchronisieren
    if st.session_state.page != selected_key:
        st.session_state.page = selected_key
        st.rerun()

# -------------------------
# System Page
# -------------------------
def render_system():
    st.title("💸 Dein Finanzsystem")
    st.caption("Klare Zahlen. Klarer Überblick.")

    # defensive Zugriffe
    kaufimpulse = st.session_state.get("kaufimpulse", [])
    eingefroren = [i for i in kaufimpulse if i.get("status") == "eingefroren"]

    st.markdown("### 📊 System-Zustand")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        label="Cooling-Off ab",
        value=f"{st.session_state.get('cooling_off_betrag', 30)} €"
    )

    col2.metric(
        label="Eingefrorene Käufe",
        value=len(eingefroren)
    )

    col3.metric(
        label="Impulskäufe gesamt",
        value=len(kaufimpulse)
    )

    st.markdown("---")

    st.markdown(
        "> **Leitsatz**  \n"
        "> Ich entscheide nicht unter Dopamin."
    )


    st.markdown("<br><br>", unsafe_allow_html=True) 

    st.info(
        "Navigation läuft vollständig über die Sidebar. "
        "Diese Seite gibt dir nur den Überblick, keine Aktionen."
    )
# -------------------------
# Kaufimpuls Page
# -------------------------
def render_kaufimpuls():
    st.title("Kaufimpuls eintragen")
    betrag = st.number_input("Betrag (€)", min_value=0.0, step=1.0)
    zustand = "eingefroren" if betrag >= st.session_state.cooling_off_betrag else "flüssig"
    kategorie = st.selectbox("Kategorie", KATEGORIEN)
    warum = st.text_area("Warum willst du das gerade?", max_chars=200)

    if st.button("Absenden"):
        # sichere Append: hole Referenz (get) und ändere sie
        impulse = st.session_state.get("kaufimpulse", [])
        impulse.append({
            "betrag": betrag,
            "kategorie": kategorie,
            "warum": warum,
            "status": zustand,
            "timestamp": datetime.now()
        })
        st.session_state.kaufimpulse = impulse  # sicher zurückschreiben
        if zustand == "eingefroren":
            st.success("Impuls eingetragen und eingefroren!")
        else:
            st.success("Impuls eingetragen!")
        sleep(1)
        st.session_state.page = "system"
        st.rerun()

# -------------------------
# Regeln Page
# -------------------------
def render_rules():
    st.title("Regeln anpassen")
    current = st.session_state.get("cooling_off_betrag", 30)
    neuer_betrag = st.number_input("Neue Cooling-Off Grenze (€)", value=current)
    if st.button("Speichern"):
        st.session_state.cooling_off_betrag = neuer_betrag
        st.success(f"Neue Grenze gesetzt: {neuer_betrag} €")
        st.session_state.page = "system"
        sleep(1.1)
        st.rerun()

# -------------------------
# Main Render
# -------------------------
def render():
    # zwingend zuerst: State initialisieren
    init_state()

    sidebar()

    page = st.session_state.get("page", "system")
    if page == "system":
        render_system()
    elif page == "kaufimpuls":
        render_kaufimpuls()
    elif page == "rules":
        render_rules()
