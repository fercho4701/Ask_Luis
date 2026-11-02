import streamlit as st
from pathlib import Path

st.title("Prueba del logo de Ask Luis")
logo = Path(__file__).resolve().parent / "assets" / "logo.png"
st.write("Archivo encontrado:", logo.exists())
st.image(str(logo), caption="Logo de Ask Luis")
