import streamlit as st
import os

from back import axidraw_helpers as ah

st.set_page_config(layout="wide")

st.title("Souvenir PyDay Valparaíso - v2")

col1, col2 = st.columns(2)
# Input #1: SVG
svg_fileupload = col1.file_uploader("Carga un archivo svg", type="svg")
svg_file = os.path.join("tmp", "tmp.svg")
if svg_fileupload is not None:
    with open(svg_file, "wb") as f:
        f.write(svg_fileupload.getvalue())

# Input #2: Velocidad del lápiz
speed_pendown = col2.slider("Velocidad del lápiz", min_value=10, max_value=100, value=50, step=10)

# Mostrar el SVG, si se ha cargado
enable_button = False
if svg_fileupload is not None:
    enable_button = True
    st.image(svg_file)

    # Usar 2 columnas, para calcular tiempo de dibujo y dibujar
    col1, col2 = st.columns(2)
    if col1.button("¿Cuánto tomará?"):
        status, draw_time = ah.draw_svg(svg_file, speed_pendown, skip_draw=True)
        if status == "error":
            col1.write("Error conectando con AxiDraw")
        else:
            col1.write(f"Tiempo estimado: {draw_time:.1f} segundos")
    if col2.button("¡Dibújalo!"):
        status, draw_time = ah.draw_svg(svg_file, speed_pendown) # skip_draw=False by default
        if status == "error":
            col2.write("Error conectando con AxiDraw")
        else:
            col2.write(f"Tiempo utilizado: {draw_time:.1f} segundos")
