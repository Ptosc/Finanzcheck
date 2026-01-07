import streamlit.components.v1 as components

def emoji_rain(
    emoji="⏳",
    spawn_interval=200,   # ms → Dichte
    fall_duration=5,      # s → Fallgeschwindigkeit
    rain_duration=10,     # s → Wie lange es regnet
    height=1000
):
    html_code = f"""
    <html>
    <body style="margin:0; overflow:hidden;">
    <script>
        let startTime = Date.now();

        function spawnEmoji() {{
            let e = document.createElement('div');
            e.innerText = "{emoji}";
            e.style.position = "absolute";
            e.style.left = Math.random() * 100 + "%";
            e.style.top = "-50px";
            e.style.fontSize = Math.random() * 30 + 20 + "px";
            e.style.animation = "fall {fall_duration}s linear forwards";

            document.body.appendChild(e);

            e.addEventListener("animationend", () => e.remove());
        }}

        let interval = setInterval(() => {{
            if ((Date.now() - startTime) / 1000 > {rain_duration}) {{
                clearInterval(interval);
            }} else {{
                spawnEmoji();
            }}
        }}, {spawn_interval});

        let style = document.createElement('style');
        style.innerHTML = `
            @keyframes fall {{
                from {{ top: -50px; }}
                to {{ top: 100vh; }}
            }}
        `;
        document.head.appendChild(style);
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=height)