import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime



@st.cache_resource
def get_sheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )

    client = gspread.authorize(creds)
    return client.open("Ausgaben Tracker - Amelie (Antworten)").sheet1


def render():

    st.title("Ausgabe eintragen")

    sheet = get_sheet()

    kategorien = [
        "📚 Bildung & Entwicklung",
        "💰 Sparen & Rücklagen",
        "🍽️ Alltag & Essen",
        "🎉 Freizeit & Soziales",
        "👕 Kleidung & Pflege"
    ]

    zahlungsarten = [
        "Bargeld 💵",
        "Karte 🏦",
        "Onlinezahlung 💻",
        "Sonstiges 🌀"
    ]

    with st.form("ausgabe_form"):
        kategorie_raw = st.selectbox("Kategorie", kategorien)
        kategorie = kategorie_raw.split(" ", 1)[1]

        betrag = round(
            st.number_input("Betrag (€)", min_value=0.0, step=0.5),
            2
        )

        beschreibung = st.text_input("Beschreibung")
        zahlungsart = st.selectbox("Zahlungsart", zahlungsarten)

        submitted = st.form_submit_button("Eintragen")

    if submitted:
        # Pflichtfeldprüfung
        if not kategorie or betrag <= 0 or not beschreibung.strip() or not zahlungsart:
            st.warning("Bitte fülle alle Felder aus und gib einen Betrag größer 0 ein 🛑")
        else:
            try:
                sheet.append_row([
                    datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                    kategorie,
                    betrag,
                    beschreibung.strip(),
                    zahlungsart
                ])
                st.success("Ausgabe gespeichert ✅")
            except Exception as e:
                st.error(f"Fehler beim Eintragen: {e}")
            
# import streamlit as st
# import gspread
# from google.oauth2.service_account import Credentials
# from datetime import datetime

# @st.cache_resource
# def get_sheet():
#     scopes = [
#         "https://www.googleapis.com/auth/spreadsheets",
#         "https://www.googleapis.com/auth/drive"
#     ]
#     secret = st.secrets["gcp_service_account"]
#     creds = Credentials.from_service_account_file(secret, scopes=scopes)
#     client = gspread.authorize(creds)
#     return client.open("Ausgaben Tracker - Amelie (Antworten)").sheet1

# def render():
#     st.title("Ausgabe eintragen")

#     sheet = get_sheet()

#     kategorien = [
#         "📚 Bildung & Entwicklung",
#         "💰 Sparen & Rücklagen",
#         "🍽️ Alltag & Essen",
#         "🎉 Freizeit & Soziales",
#         "👕 Kleidung & Pflege"
#     ]

#     zahlungsarten = [
#         'Bargeld 💵',
#         'Karte 🏦',
#         'Onlinezahlung 💻',
#         'Sonstiges 🌀'
#     ]

    
#     kategorie_raw = st.selectbox("Kategorie", kategorien)
#     kategorie = kategorie_raw[2:]  # Emoji + Leerzeichen entfernen

#     betrag = st.number_input("Betrag (€)", min_value=0.0, step=0.5)
#     betrag = round(float(betrag), 2)
#     if betrag == 0:
#         st.warning("Betrag darf nicht 0 sein")
#         st.stop()

#     beschreibung = st.text_input("Beschreibung")

#     zahlungsart = st.selectbox("Zahlungsart", zahlungsarten)

#     if st.button("Eintragen"):
#         try:
#             sheet.append_row([
#                 datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
#                 kategorie,
#                 betrag,
#                 beschreibung,
#                 zahlungsart
#             ])
#             st.success("Ausgabe gespeichert ✅")
#         except Exception as e:
#             st.error(f"Fehler beim Eintragen: {e}")