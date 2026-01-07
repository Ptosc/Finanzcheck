import streamlit as st
from data import load_data
import random
import streamlit.components.v1 as components
from utils.emoji_effects import emoji_rain

reflexion_subheader = [
    # Existenzielle / Tiefgründige Texte
    "> **Pause.**  \n> Nicht zum Optimieren. Nur ein ehrlicher Blick.",
    "> **Stopp.**  \n> Nicht um produktiv zu sein. Sondern um zu fühlen, was diese Zeit wirklich wert ist.",
    "> **Das ist deine Zeit.**  \n> Jede Minute zählt. Wie viel davon war diese Ausgabe wert?",
    "> Stell dir vor, du könntest die Zeit zurückdrehen.  \n> Würdest du diese Ausgabe gleich wieder tätigen? Denk kurz nach.",
    "> Ein Moment für dich.  \n> Nimm wahr, was wirklich zählt. Nicht die Zahlen, nur die Wirkung.",
    "> **Zeit ist die einzige Währung, die du nie zurückbekommst.**  \n> Wie hast du sie ausgegeben?",
    "> Hier geht es nicht ums Optimieren.  \n> Hier geht es um Wahrheit – deine Wahrheit.",

    # Provokativ / Herausfordernd
    "> Ein Moment für dich.  \n> Würdest du diese Stunde zurückhaben, wenn du könntest? Sei ehrlich.",
    "> Hast du gerade etwas getan, das deinen Lebenswert wirklich steigert?",
    "> Wenn diese Minute dein letztes Geschenk wäre – würdest du es so ausgeben?",
    "> Blicke nicht weg.  \n> Diese Zeit ist unwiederbringlich. Wie hast du sie genutzt?",
    "> Kein Filter, keine Rechtfertigung – nur du und diese Entscheidung.",

    # Meditativ / Achtsam
    "> Atme tief ein.  \n> Beobachte ohne Urteil. Nur ein Blick auf die Wahrheit.",
    "> Ruhig werden.  \n> Hinschauen. Wahrnehmen, was diese Ausgabe bedeutet.",
    "> Lass die Zahlen los.  \n> Fühle die Zeit, die dahinter steckt.",
    "> Nur einen Moment.  \n> Kein Urteil. Nur ein ehrlicher Blick auf dein Handeln.",
    "> Spüre, ohne zu rechtfertigen.  \n> Jede Minute zählt.",

    # Emotional / Persönlich
    "> Deine Zeit ist kostbar.  \n> Diese Ausgabe ist ein Teil davon. Wie fühlst du dich damit?",
    "> Ein Moment der Ehrlichkeit.  \n> Für dich, nicht für andere.",
    "> Jede Ausgabe erzählt eine Geschichte.  \n> Welche Geschichte willst du wirklich schreiben?",
    "> Deine Lebenszeit, deine Verantwortung.  \n> War es es wert?",
    "> Manchmal sind es die kleinen Entscheidungen,  \n> die die größte Wirkung auf dein Leben haben.",

    # Kurz & Prägnant
    "> **Pause. Fühle. Reflektiere.**",
    "> Nur ein Moment. Keine Rechtfertigung.",
    "> Reflektiere. Nicht optimieren.",
    "> Hier und jetzt. Dein Blick auf deine Zeit.",
    "> Eine Minute. Deine Entscheidung."
]

reflexions_prompts = [
    "Ein ruhiger Moment.\nInmitten von Zahlen.\nEine Einladung, kurz ehrlich zu sein.",

    "Ein kleiner Bruch im Fluss.\nDamit etwas sichtbar wird.",

    "Eine offene Einladung.\nEhrlich hinzuschauen.",

    "Ein Moment Aufmerksamkeit.\nMehr nicht.",

    "Ein ruhiger Moment.\nNicht außerhalb.\nMitten im Jetzt.",

    "Ein kurzer Halt.\nZwischen Rechnen\nund Verstehen.",

    "Ein leiser Zwischenraum.\nOhne Druck.\nOhne Ziel.",

    "Ein Atemzug.\nBevor es weitergeht.",

    "Ein ruhiger Übergang.\nVon Tun\nzu Wahrnehmen.",

    "Ein kleiner Abstand.\nZum eigenen Handeln.",

    "Ein stiller Moment.\nInmitten von Entscheidungen.",

    "Ein kurzes Verweilen.\nOhne Bewertung.",

    "Ein bewusster Augenblick.\nNur dafür.",

    "Ein Schritt zur Seite.\nUm klarer zu sehen.",

    "Ein Raum zum Nachspüren.\nOhne Erklärung.",

    "Ein Moment Klarheit.\nNicht erzwungen.",

    "Ein leiser Fokuswechsel.\nWeg vom Müssen.",

    "Ein Innehalten.\nZwischen Impuls\nund Reaktion.",

    "Ein ruhiger Schnitt.\nIm Strom der Gewohnheit.",

    "Ein Augenblick Präsenz.\nMehr ist nicht nötig.",

    "Ein Zwischenmoment.\nBevor Bedeutung entsteht.",

    "Ein kurzes Stillwerden.\nMitten im Ablauf.",

    "Ein Ort ohne Urteil.\nNur Wahrnehmung.",

    "Ein leiser Rahmen.\nFür einen ehrlichen Blick.",

    "Ein Moment Abstand.\nDer Nähe schafft.",

    "Ein kurzes Ankommen.\nHier.",

    "Ein bewusster Einschnitt.\nOhne Konsequenz.",

    "Ein Moment Offenheit.\nOhne Antwortdruck.",

    "Ein Innehalten.\nNicht um zu ändern.\nSondern um zu sehen.",

    "Ein ruhiger Punkt.\nIm Satz deines Tages."
]

reflexions_textbausteine = {
    "❌ Nein": [
        "⚠️ Überlege: Hättest du diese Ausgabe anders priorisieren können?",
        "📉 Fast nichts gewonnen. Welche Alternative wäre wertvoller gewesen?",
        "🛑 Stopp. War das notwendig oder nur Gewohnheit?",
        "💭 Reflektiere: Würdest du diese Ausgabe noch einmal tätigen?"
    ],
    "🤔 Kaum": [
        "🤔 Ein kleiner Nutzen. Kannst du daraus lernen?",
        "🔎 Fast neutral. Welche kleine Anpassung hätte mehr gebracht?",
        "💡 Denke nach: Wo steckt noch ungenutztes Potenzial?",
        "🧐 Nicht schlecht, aber es geht vielleicht noch besser."
    ],
    "😐 Unklar": [
        "😐 Unklar, ob es wertvoll war. Lass es kurz sacken.",
        "📝 Neutral. Überlege, was du daraus lernen kannst.",
        "⚖️ Weder gut noch schlecht – eine Chance für Reflexion.",
        "👁️ Beobachte dich: Warum hast du diese Ausgabe gewählt?"
    ],
    "🙂 Ein bisschen": [
        "🙂 Ein kleiner Gewinn. Merke dir den Effekt für die Zukunft.",
        "👍 Positiv, wenn auch gering. Kann öfter vorkommen.",
        "🚶‍♂️ Ein Schritt in die richtige Richtung. Beachte die Wirkung.",
        "👏 Gut gemacht – aber gibt es noch mehr Wert?"
    ],
    "✅ Deutlich": [
        "✅ Top! Das hat wirklich Mehrwert gebracht.",
        "🏆 Klare Entscheidung. Wiederholen lohnt sich.",
        "🎯 Perfekt genutzt. Merke dir dieses Muster.",
        "🌟 Hervorragend! Genau so kannst du öfter handeln."
    ]
}

markdown_texte = [
    """Diese Ausgabe entspricht etwa  
**{fall} deiner Lebenszeit.**""",

    """Umgerechnet sind das rund  
**{fall} Zeit.**""",

    """Zeitlich betrachtet ergibt das  
**{fall}.**""",

    """Das entspricht in etwa  
**{fall} Lebenszeit.**""",

    """In Zeit gemessen sind das  
**{fall}.**""",

    """Rein zeitlich entspricht das  
**{fall}.**""",

    """Diese Ausgabe lässt sich beziffern auf  
**{fall}.**""",

    """In Lebenszeit übersetzt sind das  
**{fall}.**""",

    """Ein Blick auf die Zeit dahinter:  
**{fall}.**""",

    """Diese Ausgabe steht für  
**{fall} Zeit.**""",

    """Wenn man es in Zeit denkt, sind das  
**{fall}.**""",

    """Zeitlich gesehen entspricht das  
**{fall}.**""",

    """Diese Ausgabe kostet  
**{fall} Lebenszeit.**""",

    """Der Zeitpreis dieser Ausgabe beträgt  
**{fall}.**""",

    """In Zeit umgerechnet ergibt sich  
**{fall}.**""",

    """Als Zeit betrachtet sind das  
**{fall}.**""",

    """Zeit ist die stille Währung – hier  
**{fall}.**""",

    """Auch Zeit fließt hier hinein:  
**{fall}.**"""
]
    # Selectbox: nur das Label anzeigen, intern Index behalten

def format_label(option):
    return option[1]

def sidebar(df):

    sorted_df = df.sort_values(by='Betrag', ascending=False)

    # Zufällige Zeile im sessionstate speichern
    if 'ausgabe' not in st.session_state:
        st.session_state.ausgabe = df.sample()

    # Button für neue zufällige Ausgabe
    if st.sidebar.button('Überrasch mich'):
        st.session_state.ausgabe = df.sample()

    ausgabe = st.session_state.ausgabe
    default_index = int(ausgabe.index[0])

    
 
    # Eindeutige Labels: "Beschreibung (X €)"
    options = [(idx, f" {row['Beschreibung']} ({row['Betrag']}) €") 
            for idx, row in sorted_df.iterrows()]

    gewählter_index, _ = st.sidebar.selectbox(
        'Ausgabe',
        options,
        index=[i for i, (idx, _) in enumerate(options) if idx == default_index][0],
        format_func=format_label
    )

    # Session State aktualisieren
    if gewählter_index != default_index:
        st.session_state.ausgabe = df.loc[[gewählter_index]]

    # Stundenlohn
    st.session_state.stundenlohn = st.sidebar.number_input(
    "Stundenlohn",
    min_value=1,          
    value=15,        
    )
    stundenlohn = st.session_state.stundenlohn

    if st.sidebar.button('Neuer Reflexionstext'):
        st.session_state.text = random.choice(reflexion_subheader)
        st.session_state.prompt = random.choice(reflexions_prompts)
        st.session_state.markdown_text = random.choice(markdown_texte)

def content():
    # soll ausgabe lokal speichern, um weniger schreiben zu müssen 
    ausgabe = st.session_state.ausgabe
    stundenlohn = st.session_state.stundenlohn

    st.title("🧠 Reflexion")

    if 'text' not in st.session_state:
        st.session_state.text = random.choice(reflexion_subheader)
    st.markdown(st.session_state.text)

    # --- Arbeitszeit berechnen ---
    arbeitszeit = float(ausgabe['Betrag'].iloc[0]) / stundenlohn

    if arbeitszeit < 1:
        arbeitszeit = arbeitszeit * 60
        einheit = "Minuten"
    elif arbeitszeit == 1:
        einheit = 'Stunde'
    elif arbeitszeit % 1 == 0:
        einheit = 'Stunden' 
    else:
        teile = str(arbeitszeit).split('.')
        stunden = int(teile[0])
        minuten = float('0.' + teile[1]) * 60
        s_einheit = 'Stunde' if stunden == 1 else 'Stunden'
        einheit = 'Gemischt'

    st.markdown("---")

    if einheit == 'Gemischt':
        fall = f'{stunden} {s_einheit} und {minuten:.0f} Minuten'

    else:
        fall = f'{arbeitszeit:.0f} {einheit}'


    if 'markdown_text' not in st.session_state:
        st.session_state.markdown_text = random.choice(markdown_texte)

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(f"""
    ### {ausgabe['Beschreibung'].iloc[0]} (für {ausgabe['Betrag'].iloc[0]} €)

    {st.session_state.markdown_text.format(
        fall=fall
    )}
    """)

    st.markdown("---")

    # --- Reflexionsfrage ---
    if 'prompt' not in st.session_state:
        st.session_state.prompt = random.choice(reflexions_prompts)

    st.markdown(f"""
    ### {st.session_state.prompt}
    """)

    st.session_state.bewertung = st.select_slider(
        "Hat diese Ausgabe mein Leben real verbessert?",
        [
            "❌ Nein",
            "🤔 Kaum",
            "😐 Unklar",
            "🙂 Ein bisschen",
            "✅ Deutlich"
        ],
        value="😐 Unklar"
    )

    st.session_state.textbaustein = random.choice(reflexions_textbausteine[st.session_state.bewertung])

    if st.session_state.bewertung in ["❌ Nein", "🤔 Kaum"]:
        st.info(st.session_state.textbaustein)
    elif st.session_state.bewertung in ["🙂 Ein bisschen", "✅ Deutlich"]:
        st.success(st.session_state.textbaustein)

    st.markdown("")

    # --- Regen-Intensität je nach Bewertung ---
    regen_intensität = {
        "❌ Nein": {"spawn_interval": 300, "duration": 2},
        "🤔 Kaum": {"spawn_interval": 250, "duration": 2.5},
        "😐 Unklar": {"spawn_interval": 200, "duration": 4},
        "🙂 Ein bisschen": {"spawn_interval": 150, "duration": 7},
        "✅ Deutlich": {"spawn_interval": 100, "duration": 8}
    }

    if st.button("Reflexion abschließen"):
        params = regen_intensität[st.session_state.bewertung]
        emoji_rain(
            emoji=st.session_state.bewertung[0],
            spawn_interval=params["spawn_interval"],
            rain_duration=params["duration"]
        )

        st.markdown(f"""
        <div style="text-align:center; opacity:0.8; margin-top:1rem;">
            {("Danke für deine Ehrlichkeit!" if st.session_state.bewertung not in ['😐 Unklar'] else "Reflexion abgeschlossen.")}
        </div>
        """, unsafe_allow_html=True)

def render():
    df = load_data()

    sidebar(df)
    
    content()