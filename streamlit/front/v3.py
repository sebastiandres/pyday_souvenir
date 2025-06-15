import streamlit as st
import os

from back import axidraw_helpers as ah

st.set_page_config(layout="wide")

st.title("Souvenir PyDay Valparaíso - v3")

# Create columns to place the content
col1, col2 = st.columns(2)
text_1 = col1.text_input("Texto a reemplazar en svg", value="Valparaíso 2025")
text_2 = col2.text_input("Texto a reemplazar en svg", value="¡Gracias!")

# Velocidad del lápiz
speed_pendown = col2.slider("Velocidad del lápiz", min_value=10, max_value=100, value=50, step=10)

# Update the svg file with the text

sel = col1.radio("Imagen a mostrar", ["Modificado", "Original"], horizontal=True)
default_svg_file = os.path.join("assets", "pyday_logo.svg")
updated_svg_file = os.path.join("tmp", "text_tmp.svg")
plain_svg_file = os.path.join("tmp", "text_tmp_plain.svg")

with open(default_svg_file, "r") as f:
    default_svg_content = f.read()
    # Replace the text with the text from the text area
    updated_svg_content = default_svg_content.replace("PLACEHOLDER_1", text_1)
    updated_svg_content = updated_svg_content.replace("PLACEHOLDER_2", text_2)

# Save the svg content to a new file
with open(updated_svg_file, "w") as f:
    f.write(updated_svg_content)

# Clean the svg files
ah.clean_svg(updated_svg_file, plain_svg_file)

# Show the svg file
if sel == "Modificado":
    st.image(updated_svg_file)
else:
    st.image(plain_svg_file)

# Print the svg file
col1, col2 = st.columns(2)
if col1.button("¿Cuánto tomará?"):
    status, draw_time = ah.draw_svg(plain_svg_file, speed_pendown, skip_draw=True)
    if status == "error":
        col1.error("Error conectando con AxiDraw")
    else:
        col1.info(f"Tiempo estimado: {draw_time:.1f} segundos")
if col2.button("¡Dibújalo!"):
    status, draw_time = ah.draw_svg(plain_svg_file, speed_pendown) # skip_draw=False by default
    if status == "error":
        col2.error("Error conectando con AxiDraw")
    else:
        col2.info(f"Tiempo estimado: {draw_time:.1f} segundos")
