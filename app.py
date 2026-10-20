import os

import streamlit as st

from services.knowledge_service import KnowledgeService
from services.prompt_service import PromptService
from llm.groq_service import GroqService



# CONFIGURACIÓN


LOGO_PATH = "assets/logo.png"

st.set_page_config(
    page_title="Luis AI Recruiter",
    page_icon=LOGO_PATH if os.path.exists(LOGO_PATH) else "🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

SUGGESTIONS = [
    "👨‍💻 ¿Cuál es el perfil profesional de Luis?",
    "🛠️ ¿Qué tecnologías domina?",
    "🚀 ¿Qué proyectos ha desarrollado?",
    "🎯 ¿Por qué debería contratarlo?",
]



# ESTADO DE LA APLICACIÓN


if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None



# ESTILO


THEMES = {
    "dark": {
        "bg": "#0b0d12",
        "bg_alt": "#12151c",
        "card": "#161a23",
        "border": "rgba(255,255,255,0.08)",
        "text": "#f2f4f8",
        "muted": "#9aa3b2",
        "accent": "#6c8cff",
        "accent2": "#a26bff",
        "user_bubble": "linear-gradient(135deg, #3b4cca 0%, #6c3fd1 100%)",
        "shadow": "0 8px 30px rgba(0,0,0,0.35)",
    },
    "light": {
        "bg": "#f6f7fb",
        "bg_alt": "#ffffff",
        "card": "#ffffff",
        "border": "rgba(15,23,42,0.08)",
        "text": "#10131a",
        "muted": "#5f6b7d",
        "accent": "#4f6bff",
        "accent2": "#8b5cf6",
        "user_bubble": "linear-gradient(135deg, #4f6bff 0%, #8b5cf6 100%)",
        "shadow": "0 8px 30px rgba(20,30,70,0.10)",
    },
}

t = THEMES["dark" if st.session_state.dark_mode else "light"]

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {{
        --bg: {t['bg']};
        --bg-alt: {t['bg_alt']};
        --card: {t['card']};
        --border: {t['border']};
        --text: {t['text']};
        --muted: {t['muted']};
        --accent: {t['accent']};
        --accent2: {t['accent2']};
        --shadow: {t['shadow']};
    }}

    html, body, [class*="css"], .stApp {{
        font-family: 'Inter', sans-serif;
    }}

    /* Fondo con degradado sutil */
    .stApp {{
        background:
            radial-gradient(900px 400px at 85% -10%, color-mix(in srgb, var(--accent) 18%, transparent), transparent 60%),
            radial-gradient(700px 380px at -10% 0%, color-mix(in srgb, var(--accent2) 14%, transparent), transparent 60%),
            var(--bg);
        color: var(--text);
    }}

    /* Ocultar elementos por defecto de Streamlit */
    #MainMenu, footer, [data-testid="stToolbar"],
    [data-testid="stDecoration"] {{
        display: none !important;
        visibility: hidden;
    }}
    header[data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        max-width: 780px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }}

    /* ---------- HERO ---------- */
    .hero {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 22px;
        padding: 1.6rem 1.8rem;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        margin-bottom: 1.2rem;
    }}
    .hero::before {{
        content: "";
        position: absolute;
        inset: 0 0 auto 0;
        height: 4px;
        background: linear-gradient(90deg, var(--accent), var(--accent2));
    }}
    .badge {{
        display: inline-flex;
        align-items: center;
        gap: .45rem;
        font-size: .75rem;
        font-weight: 600;
        letter-spacing: .02em;
        color: var(--accent);
        background: color-mix(in srgb, var(--accent) 12%, transparent);
        border: 1px solid color-mix(in srgb, var(--accent) 30%, transparent);
        padding: .25rem .7rem;
        border-radius: 999px;
        margin-bottom: .8rem;
    }}
    .badge .dot {{
        width: 7px; height: 7px; border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 0 0 rgba(34,197,94,.6);
        animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
        0%   {{ box-shadow: 0 0 0 0 rgba(34,197,94,.55); }}
        70%  {{ box-shadow: 0 0 0 8px rgba(34,197,94,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(34,197,94,0); }}
    }}
    .main-title {{
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.15;
        margin: 0 0 .4rem 0;
        background: linear-gradient(90deg, var(--text) 30%, var(--accent) 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
        color: var(--muted);
        font-size: 1rem;
        margin: 0;
    }}

    /* ---------- LOGO ---------- */
    [data-testid="stImage"] img {{
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        background: transparent !important;
        {"mix-blend-mode: screen;" if st.session_state.dark_mode else ""}
    }}

    /* ---------- SUGERENCIAS ---------- */
    .section-label {{
        color: var(--muted);
        font-size: .78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: .08em;
        margin: .6rem 0 .5rem 0;
    }}
    .stButton > button {{
        width: 100%;
        text-align: left;
        justify-content: flex-start;
        background: var(--card);
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: .75rem 1rem;
        font-weight: 500;
        font-size: .92rem;
        transition: all .18s ease;
    }}
    .stButton > button:hover {{
        border-color: var(--accent);
        color: var(--accent);
        transform: translateY(-2px);
        box-shadow: var(--shadow);
    }}

    /* ---------- CHAT ---------- */
    [data-testid="stChatMessage"] {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1rem 1.2rem;
        margin-bottom: .8rem;
        box-shadow: 0 2px 10px rgba(0,0,0,.06);
    }}
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
        background: {t['user_bubble']};
        border: none;
        color: #ffffff;
    }}
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) * {{
        color: #ffffff !important;
    }}
    [data-testid="stChatMessage"] p {{
        line-height: 1.65;
        font-size: .98rem;
    }}
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] td,
    [data-testid="stChatMessage"] th,
    [data-testid="stChatMessage"] strong,
    [data-testid="stChatMessage"] h1,
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3,
    [data-testid="stChatMessage"] h4,
    [data-testid="stMarkdownContainer"] {{
        color: var(--text);
    }}
    [data-testid="stChatMessage"] table {{
        color: var(--text);
        border-color: var(--border);
    }}
    [data-testid="stChatMessage"] th,
    [data-testid="stChatMessage"] td {{
        border-color: var(--border) !important;
    }}
    [data-testid="stChatMessage"] code {{
        color: var(--accent);
    }}

    /* ---------- INPUT ---------- */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div {{
        background: transparent !important;
    }}
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] div[data-baseweb="textarea"],
    [data-testid="stChatInput"] div[data-baseweb="base-input"],
    [data-testid="stChatInput"] textarea {{
        background: var(--card) !important;
        background-color: var(--card) !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
        caret-color: var(--accent);
    }}
    [data-testid="stChatInput"] {{
        border: 1px solid var(--border);
        border-radius: 18px;
        box-shadow: var(--shadow);
    }}
    [data-testid="stChatInput"] textarea::placeholder {{
        color: var(--muted) !important;
        -webkit-text-fill-color: var(--muted) !important;
        opacity: 1;
    }}
    [data-testid="stChatInput"] button {{
        background: transparent !important;
        color: var(--accent) !important;
    }}
    [data-testid="stChatInput"]:focus-within {{
        border-color: var(--accent);
    }}

    /* ---------- VARIOS ---------- */
    hr {{
        border-color: var(--border) !important;
    }}
    .footer-note {{
        text-align: center;
        color: var(--muted);
        font-size: .75rem;
        margin-top: 1.5rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)



# ENCABEZADO


top_left, top_right = st.columns([6, 1])

with top_right:
    dark = st.toggle("🌙", value=st.session_state.dark_mode)
    if dark != st.session_state.dark_mode:
        st.session_state.dark_mode = dark
        st.rerun()

if os.path.exists(LOGO_PATH):
    logo_col, hero_col = st.columns([1, 4], vertical_alignment="center")
    with logo_col:
        st.image(LOGO_PATH, use_container_width=True)
else:
    hero_col = st.container()

with hero_col:
    st.markdown(
        """
        <div class="hero">
            <div class="badge"><span class="dot"></span> Asistente disponible</div>
            <h1 class="main-title">Luis AI Recruiter</h1>
            <p class="subtitle">
                Portfolio inteligente de <b>Luis Fernando González Molina</b>.
                Pregunta lo que quieras sobre su experiencia, habilidades y proyectos.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )



# BACKEND


@st.cache_resource
def load_backend():
    knowledge = KnowledgeService()
    prompt_service = PromptService()
    llm = GroqService()
    data = knowledge.load_all()

    with open("prompts/system_prompt.txt", "r", encoding="utf-8") as file:
        system_prompt = file.read()

    return data, prompt_service, llm, system_prompt


data, prompt_service, llm, system_prompt = load_backend()



# SUGERENCIAS (solo cuando el chat está vacío)


if not st.session_state.messages:
    st.markdown(
        '<div class="section-label">Prueba preguntando</div>',
        unsafe_allow_html=True,
    )
    cols = st.columns(2)
    for i, suggestion in enumerate(SUGGESTIONS):
        with cols[i % 2]:
            if st.button(suggestion, key=f"sug_{i}"):
                st.session_state.pending_question = suggestion
                st.rerun()



# HISTORIAL DEL CHAT


AVATARS = {
    "user": "🧑‍💼",
    "assistant": LOGO_PATH if os.path.exists(LOGO_PATH) else "🤖",
}

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=AVATARS[message["role"]]):
        st.markdown(message["content"])


# --------------------------------------------------
# CHAT
# --------------------------------------------------

typed = st.chat_input("Pregúntame sobre la experiencia de Luis...")
question = typed or st.session_state.pending_question
st.session_state.pending_question = None

if question:

    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user", avatar=AVATARS["user"]):
        st.markdown(question)

    with st.chat_message("assistant", avatar=AVATARS["assistant"]):
        with st.spinner("Analizando la información..."):
            prompt = prompt_service.build_prompt(
                context=data,
                question=question,
            )
            response = llm.ask(
                prompt=prompt,
                system_prompt=system_prompt,
            )
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})


st.markdown(
    '<p class="footer-note">⚠️ Esta IA es una herramienta de apoyo y no sustituye una entrevista directa con Luis Fernando González Molina.</p>',
    unsafe_allow_html=True,
)