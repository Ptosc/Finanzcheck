import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
from random import choice
from data import load_data, create_fake_data


MONEY_QOUTES = [
    "Jeder Euro ist ein Samen für deine Freiheit.",
    "Impulse verblassen, Ziele bleiben.",
    "Klarheit im Geld bringt Ruhe im Geist.",
    "Automatisch sparen, entspannt gewinnen.",
    "Dein Geld folgt deiner Aufmerksamkeit.",
    "Hürden schützen vor flüchtigen Versuchungen.",
    "Jeder bewusste Euro ist ein Anker.",
    "Vision übertrifft den flüchtigen Glanz.",
    "Investiere in Morgen, nicht im Jetzt gefangen.",
        "Sparen heißt: Dein Konto soll wachsen, nicht dein Stress.",
    "Jeder Euro, den du nicht ausgibst, freut sich heimlich.",
    "Dein Konto liebt dich mehr, wenn du ihm Pausen gönnst.",
    "Jeder Euro, den du behältst, ist ein Mini-Superheld.",
    "Geld, das du siehst, rennt nicht weg – es posiert.",
    "Sparen ist wie Yoga für dein Bankkonto – flexibel bleiben!",
    "Impulse haben kurze Beine, dein Konto lange Arme.",
        "Jeder Euro ist ein Pixel in deinem Lebenskunstwerk.",
    "Sparen ist wie Origami – falte dein Geld in Form.",
    "Dein Konto kann fliegen, wenn du die Fesseln löst.",
    "Impulse sind Wolken, Ziele der blaue Himmel.",
    "Jedes bewusste Ausgeben ist ein kleiner Zaubertrick.",
    "Dein Geld erzählt Geschichten – lass es episch werden.",
    "Sparen ist wie Schach: ein Zug heute, ein Sieg morgen.",
    "Jeder Euro ist ein kleiner Stern in deinem Finanz-Universum.",
    "Hürden sind magische Portale für kluge Entscheidungen.",
        "Kontrolle beginnt, wo Klarheit wohnt.",
    "Jeder bewusste Euro zeigt deine Stärke.",
    "Du bist Architekt deiner Mittel, nicht Sklave der Versuchung.",
    "Dein Konto folgt deinem Willen, nicht deinen Impulsen.",
    "Sparen ist ein Ausdruck deiner Selbstachtung.",
    "Du bestimmst, wohin dein Geld fließt.",
    "Jede Entscheidung stärkt deine finanzielle Identität.",
    "Du bist nicht Opfer deiner Wünsche, du bist ihr Kapitän.",
    "Selbstkontrolle ist ein Zeichen deiner Freiheit, nicht Verzicht."
]

ZAHL_ZU_MONAT = {
    1: "Januar",
    2: "Februar",
    3: "März",
    4: "April",
    5: "Mai",
    6: "Juni",
    7: "Juli",
    8: "August",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Dezember"
}

MONAT_ZU_ZAHL = {value: key for key, value in ZAHL_ZU_MONAT.items()}

# Berechnet datum der ersten Ausgabe
def calc_months(df):
    now = datetime.now()

    # datum der ersten Ausgabe finden
    df.sort_values(by="Zeitstempel", inplace=True)
    zeitstempel = df.loc[0, "Zeitstempel"]
    jahr = zeitstempel.year
    monat = zeitstempel.month

    datum = {ZAHL_ZU_MONAT[monat]: jahr}

    while not (monat == now.month and jahr == now.year):
        monat += 1
        if monat > 12:
            monat = 1
            jahr += 1
            
        datum[ZAHL_ZU_MONAT[monat]] = jahr

    return datum

# Filtere df nach diesem Monat
def this_months_expences(df):
    now = datetime.now()
    
    df = df.loc[df['Zeitstempel'].dt.month == now.month]

    return df

def has_expenses_this_month(df):
    df_m = this_months_expences(df)
    return not df_m.empty

# Diesen Monat in einem Satz
def scentence_of_month(df):
    df = this_months_expences(df).sort_values(by='Betrag', ascending=False)

    if df.empty:
        st.info(
            "Diesen Monat hast du noch **keine Ausgaben eingetragen**.\n\n"
            "Das ist entweder Disziplin 🧘‍♂️ oder ein leerer Zettel 📄 – "
            "du entscheidest."
        )
        st.metric(
            label="Gesamtausgaben diesen Monat",
            value="0,00 €"
        )
        return
    
    total_this_month = df['Betrag'].sum()
    single_expence = df.iloc[0]
    # die teuerste kategorie ist 
    expence_per_category = (
        df.groupby('Kategorie', as_index=False)['Betrag']
          .sum()
          .sort_values(by='Betrag', ascending=False)
    )

    most_expensive_category = expence_per_category.iloc[0]
    percentage = most_expensive_category['Betrag'] / total_this_month * 100

    st.markdown(
        f'''
        Diesen Monat hast du insgesamt **{total_this_month:.2f} €** ausgegeben.  
        Der größte Kostenblock war **{most_expensive_category["Kategorie"]}** ({percentage:.0f} %),  
        deine teuerste Einzelzahlung **{single_expence["Beschreibung"]}** ({single_expence["Betrag"]:.2f} €).
        '''
    )

    st.metric(
    label="Gesamtausgaben diesen Monat",
    value=f"{total_this_month:,.2f} €"
    )

# Wo dein Geld wirklich hingeht
def plot_categories(df):
    now = datetime.now()

    df = this_months_expences(df)

    # df gruppiert nach monat und sortiert absteigend nach ausgaben
    df = (
        df.groupby('Kategorie', as_index=False)['Betrag']
        .sum()
        .sort_values(by='Betrag', ascending=False)
    )

    if df.empty:
        st.markdown('Diesen Monat hast du noch keine Ausgaben eingetragen.')
        st.empty
        return

	# Berechne den kumulierten Prozentanteil
    total = df['Betrag'].sum()
    df['cum_percent'] = df['Betrag'].cumsum() / total * 100

    # Finde die erste spalte, mit kommulierter Wahrscheinlichkeit über 70 %
    spalte = df.loc[df['cum_percent'] >= 70].iloc[[0]]

    # Finde den index dieser spalte
    index = spalte.index[0]
    # Kleinste Anzahl an Kategrien mit kommulierter Wahrscheinlichkeit über 70 %
    anzahl = int(index + 1)
    # Anteil an Gesamtausgaben
    anteil = df.iloc[index]["cum_percent"]

	# --** Klassifizierung **--

    top1 = df.iloc[0]["Betrag"] / total * 100
    top3 = df.iloc[:3]["Betrag"].sum() / total * 100

    if top1 >= 60:
        text = (
            f'Deine Ausgaben sind diesen Monat extrem konzentriert. '
            f'Eine einzige Kategorie schluckt {top1:.1f} % des Budgets. '
            f'Das ist ein klarer Hebel, falls du sparen willst.'
        )

    elif top1 >= 45:
        text = (
            f'Deine Ausgaben sind deutlich konzentriert. '
            f'Die größte Kategorie macht {top1:.1f} % aus und prägt den Monat spürbar.'
        )

    elif top3 >= 70:
        text = (
            f'Deine Ausgaben sind moderat gebündelt. '
            f'Drei Kategorien vereinen zusammen {top3:.1f} % deiner Ausgaben. '
            f'Der Rest verteilt sich vergleichsweise ruhig.'
        )

    else:
        text = (
            f'Deine Ausgaben sind diesen Monat recht ausgewogen. '
            f'Keine einzelne Kategorie dominiert, Entscheidungen verteilen sich breit.'
        )

    st.markdown(text)

    st.header(f'{ZAHL_ZU_MONAT[now.month]} {now.year}')
    st.bar_chart(
        df,
        x='Kategorie',
        y='Betrag',
        x_label='Betrag (€)',
        horizontal=True,
        height=350
    )

    st.markdown('Das ist weder gut noch schlecht. Es zeigt, wo Hebel liegen.')

# Datum des vergangenen Monats ermitteln
def date_last_month(df):
    now = datetime.now()
    
    if now.month == 1:
        p_month = 12 
        p_m_year = now.year - 1 
    else:
        p_month = now.month - 1 
        p_m_year = now.year

    return p_month, p_m_year

# Ist ein Monatsvergleich sinnvoll
def abweichungen(df):
    now = datetime.now()
    p_month, p_m_year = date_last_month(df)

    df_t_m = df.loc[(df['Zeitstempel'].dt.month == now.month) & (df['Zeitstempel'].dt.year == now.year)].groupby('Kategorie', as_index=False)['Betrag'].sum()
    df_p_m = df.loc[(df['Zeitstempel'].dt.month == p_month) & (df['Zeitstempel'].dt.year == p_m_year)].groupby('Kategorie', as_index=False)['Betrag'].sum()

    # Index setzen und fehlende Kategorien auffüllen
    df_t_m = df_t_m.set_index('Kategorie')
    df_p_m = df_p_m.set_index('Kategorie')
    categories = df_t_m.index.union(df_p_m.index)
    df_t_m = df_t_m.reindex(categories, fill_value=0)
    df_p_m = df_p_m.reindex(categories, fill_value=0)

    abweichungen_dict = {}
    for cat in categories:
        value_t_m = df_t_m.at[cat, 'Betrag']
        value_p_m = df_p_m.at[cat, 'Betrag']
        abw = (value_t_m - value_p_m) / value_p_m * 100 if value_p_m > 0 else None
        status = "neu" if value_p_m == 0 and value_t_m > 0 else ("irrelevant" if value_p_m == 0 else "ok")
        abweichungen_dict[cat] = {"status": status, "abweichung": abw}

    # Relevant ab einer Abweichung von 10%
    relevant = any(abw["abweichung"] is not None and abw["abweichung"] > 10 for abw in abweichungen_dict.values())
    
    if relevant:
        big_abw, categorie = 0, None
        for cat, abw in abweichungen_dict.items():
            if abw["abweichung"] is not None and abw["abweichung"] > big_abw:
                big_abw, categorie = abw["abweichung"], cat
        st.markdown(f'Im Vergleich zum Vormonat hast du {big_abw:.0f} % mehr für {categorie} ausgegeben.')
    
    return abweichungen_dict

# Barplot: summe Kategorie
def plot_monats_vergleich(df): 
    now = datetime.now()

    expences_this_month = this_months_expences(df)
    p_month, p_m_year = date_last_month(df)

    with st.container():
        st.subheader("🔍 Vergleich zum Vormonat")
        abweichungen(df)

    # nach letztem monat filtern
    expences_last_month = df.loc[(df['Zeitstempel'].dt.month == p_month) & (df['Zeitstempel'].dt.year == p_m_year)]

    # nach Ausgaben pro Kategorie sortieren
    this_month = expences_this_month.groupby('Kategorie', as_index=False)['Betrag'].sum().sort_values("Betrag", ascending=False)
    last_month = expences_last_month.groupby('Kategorie', as_index=False)['Betrag'].sum().sort_values("Betrag", ascending=False)

    # Monat Auschreiben für den plot
    this_month["Monat"] = ZAHL_ZU_MONAT[now.month]
    last_month["Monat"] = ZAHL_ZU_MONAT[p_month]

    months_combined = pd.concat([this_month, last_month], ignore_index=True)

    # Bar chart
    fig, ax = plt.subplots(figsize=(7, 4))

    sns.barplot( 
    data=months_combined,
    y='Kategorie',   
    x='Betrag', 
    hue='Monat',
    palette='muted'
    ) 

    plt.ylabel('Summe')

    current_month, current_year = ZAHL_ZU_MONAT[now.month], now.year
    previous_month = ZAHL_ZU_MONAT[p_month]
    if now.month == 1:
        plt.title(f"{previous_month} {p_m_year} vs {current_month} {current_year}" )
    else: 
        plt.title(f"{previous_month} vs {current_month} {current_year}")
    st.pyplot(fig)

# Lineplot: Monatliche gesamtausgaben 
def plot_gesamt(df):
    # df mit monat und den Gesamtausgaben 
    gesamt_pro_monat = df.groupby('Monat', as_index=False)['Betrag'].sum()
    
    fig, ax = plt.subplots(figsize=(9, 4))

    sns.lineplot(
        gesamt_pro_monat,
        x='Monat',
        y='Betrag'
    )
    plt.ylabel('Total (€)')

    st.pyplot(fig)

# Top-5 Einzeltransaktionen
def top_ten(df):
    st.markdown('Einzelausgaben sagen oft mehr über Impulse als Kategorien.')

    top5_einzel = df.sort_values(by='Betrag', ascending=False).head(5)

    st.bar_chart(
        top5_einzel,
        x='Beschreibung',
        y='Betrag',
        x_label='Betrag (€)',
        y_label='',
        height=350,
        horizontal=True,
        sort=False
    )

    st.write('Diese Ausgaben sind keine Fehler – sie sind Hinweise.')

# Heatmap dieser Monat (sidebar: monat auswählbar)
def plot_heatmap(df):

        # --- Jahr-Monat Spalte erstellen ---
    if not pd.api.types.is_datetime64_any_dtype(df['Zeitstempel']):
        df['Zeitstempel'] = pd.to_datetime(df['Zeitstempel'], format="%d.%m.%Y %H:%M:%S")

    df["Monat & Jahr"] = df["Zeitstempel"].dt.strftime("%m/%Y")  # z.B. 12/2025

    # --- Monatsliste nur aus Daten ---
    monate = df.groupby("Monat & Jahr")["Betrag"].sum().loc[lambda x: x != 0].index.tolist()
    monate = ["Alle anzeigen"] + monate  # explizite Option
    monat = st.selectbox("Monat", monate, index=0)

    # --- Daten filtern ---
    if monat != "Alle anzeigen":
        df_plot = df[df["Monat & Jahr"] == monat]
        titel = f"Ausgaben nach Kategorie – {monat}"
        fig_height = 4
    else:
        df_plot = df
        titel = "Heatmap nach Kategorie"
        fig_height = 6

    # --- Pivot erstellen ---
    pivot = df_plot.pivot_table(
        index="Monat & Jahr",  # eindeutige Jahr-Monat-Kombination
        columns="Kategorie",
        values="Betrag",
        aggfunc="sum"
    )

    # --- Leere Pivot abfangen ---
    pivot = pivot.dropna(how="all")
    if pivot.empty:
        st.info("Für die Auswahl sind keine Ausgaben vorhanden.")
        return

    # Optional: schöne Beschriftung auf Monat + Jahr, z.B. Dez 2025
    pivot.index = pd.to_datetime(pivot.index).strftime("%b %Y")  

    # --- Heatmap plotten ---
    sns.set_context("notebook", font_scale=1.2)
    plt.figure(figsize=(12, fig_height))
    ax = sns.heatmap(
        pivot,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=0,
        cbar_kws={"label": "Summe (€)"},
        annot_kws={"fontsize": 16}
    )

    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        ha="right",
        fontsize=16
    )
    ax.set_yticklabels(
        ax.get_yticklabels(), 
        rotation=0,
        fontsize=14
    )
    ax.set_ylabel("")

    plt.title(titel, fontsize=18)
    plt.tight_layout()
    st.pyplot(plt)
    plt.close()

def show_quote():
    st.markdown("---")
    st.subheader("💡 Gedanke zum Mitnehmen")
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown(
            f'''
            <div style="
                text-align:center; 
                font-size:22px; 
                font-style:italic; 
                color: var(--text-color);
                background-color: var(--secondary-background-color);
                padding: 1em 1.5em;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            ">
                "{choice(MONEY_QOUTES)}"
            </div>
            ''',
            unsafe_allow_html=True
        )
    st.markdown("---\n")

# Prüfe aktuellen Theme-Modus
# Prüfen, falls theme None ist
theme = st.get_option("theme.base") or "dark"

# # Wenn sich theme ändert, session_state updaten
# if "theme" not in st.session_state or st.session_state["theme"] != theme:
#     st.session_state["theme"] = theme
#     st.rerun() 

# def color_categories(row):
#     # Soft, moderne Palette für Light & Dark, immer harmonisch
#     colors = {
#         "Bildung & Entwicklung": "#6C7A89",   # Soft Slate
#         "Sparen & Rücklagen": "#82B366",      # Soft Grün
#         "Alltag & Essen": "#F1C40F",          # Sand / Gold
#         "Freizeit & Soziales": "#9B59B6",     # Soft Lila
#         "Kleidung & Pflege": "#95A5A6"        # Grau-Blau
#     }

#     # leicht transparent für Dark-Mode Effekt
#     if theme == "dark":
#         def to_rgba(hex_color, alpha=0.15):
#             hex_color = hex_color.lstrip('#')
#             r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
#             return f"rgba({r}, {g}, {b}, {alpha})"
#         colors = {k: to_rgba(v) for k, v in colors.items()}
#     return [f'background-color: {colors.get(row["Kategorie"], "")}' for _ in row]

# Pastellige, halbtransparente Highlight-Farbe

# Style-Funktion 
def highlight_expenses(val):
    highlight_color = "rgba(255, 158, 158, 0.4)"  # Pastell-Rot
    try:
        # Betrag extrahieren
        num = float(str(val).replace(" €",""))
        return f"background-color: {highlight_color}" if num > st.session_state.mark else ""
    except:
        return ""

def render():
    df = load_data()
    tab1, tab2 = st.tabs(['Monat', 'Daten'])

    with tab1:
        # --- Überschrift und Einleitung ---
        st.title("💵 Monatsausgaben")
        st.markdown(
            "Hier siehst du, wie dein Geld fließt, welche Kategorien dominieren "
            "und wo du Hebel zum Sparen findest."
        )
        st.markdown("---")

        # --- Diesen Monat in einem Satz ---
        with st.container():
            st.subheader("📌 Monatsüberblick")
            scentence_of_month(df)

        st.markdown("---")

        # --- Wo dein Geld wirklich hingeht ---
        with st.container():
            st.subheader("📊 Ausgaben nach Kategorie")
            plot_categories(df)
            st.markdown("💡 Tipp: Konzentrierte Ausgaben zeigen, wo du sparen könntest.")

        now = datetime.now()
        prev_month = now.month - 1 if now.month > 1 else 12

        if prev_month in df['Monat'].values:
            st.markdown("---")
        
            # --- Vergleich zum Vormonat (nur wenn relevant) ---
            with st.container():
                plot_monats_vergleich(df)

        st.markdown("---")

        # --- Top 5 Einzelausgaben ---
        with st.container():
            st.subheader("🏆 Top Einzelausgaben")
            top_ten(df)

        st.markdown("---")

        # --- Heatmap als Rückblick ---
        with st.container():
            st.subheader("🌡️ Rückblick: Heatmap der Ausgaben")
            st.markdown(
                "Über mehrere Monate betrachtet zeigen sich Muster – unabhängig von einzelnen Ausreißern."
            )
            plot_heatmap(df)

        # --- Inspirierendes Zitat ---
        show_quote()

    with tab2:
        
        with st.expander("🪜 Kurzer Einstieg"):
            st.write("""
            🔹 Verschiebe den Slider um Teure Käufe zu markieren  
            🔹 Klick auf die Spalten, um die Ausgaben zu sortieren  
            🔹 Du kannst nach Betrag, Datum oder Kategorie filtern
            """)

        # Spalten sortieren: Wichtiges zuerst


        cols_order = ["Zeitstempel", "Tag", "Kategorie", "Beschreibung", "Betrag", "Zahlungsart", "Woche", "Monat", "Stunde", "Monat & Jahr"]
        df = df[cols_order]
        # Zahlen formatieren
        df["Betrag"] = df["Betrag"].map(lambda x: f"{x:.2f} €")

        # Slider erstellen, initial mit session_state
        mark = st.slider(f'Kosten', min_value=0, max_value=50, value=25, step=1)
        st.session_state.mark = mark

        color = 'background-color: #ffcccc' if mark > st.session_state.mark else ''

        sorted_df = df.sort_values(by='Zeitstempel', ascending=False)

        styled_df = sorted_df.style.map(highlight_expenses, subset=['Betrag'])


        st.markdown("## 💸 Alle Ausgaben im Überblick")
        
        st.dataframe(styled_df, height=400)

        st.caption("Tipp: Einmal auf eine Spalte tippen, sortiert sie auf- oder absteigend")

    # # --- Optional: Verlauf der Monatsausgaben ---
    # if len(df['Monat'].unique()) > 1:
    #     st.markdown("---")
    #     st.subheader("📉 Verlauf deiner Monatsausgaben")
    #     plot_gesamt(df)




