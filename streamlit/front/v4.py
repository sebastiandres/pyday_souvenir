import streamlit as st
import os
from PIL import Image

st.set_page_config(layout="wide")

st.title("Souvenir PyDay Valparaíso - v4")

# Tomar una foto y guardarla en tmp
photo = st.camera_input("Toma una foto")
if photo is not None:
    png_file = os.path.join("tmp", "tmp.png")
    with open(png_file, "wb") as f:
        f.write(photo.getvalue())

    # Convertir la foto a blanco y negro
    bn_png_file = os.path.join("tmp", "tmp_bn.png")
    nb_png_data = Image.open(png_file).convert("L")
    nb_png_data.save(bn_png_file)

    # Mostrar la foto
    st.image(png_file)
    st.image(bn_png_file)

    # Convertir la foto a svg
    #svg_file = os.path.join("tmp", "tmp.svg")

    # Save the svg content to a new file
    #with open(updated_svg_file, "w") as f:
    #    f.write(updated_svg_content)

    #st.write(default_svg_content)
    #st.write(updated_svg_content)

    # Show the svg file

    # Print the svg file
    col1, col2 = st.columns(2)
    if col1.button("¿Cuánto tomará?", use_container_width=True):
        col1.write("8 minutos")
    if col2.button("¡Dibújalo!", use_container_width=True):
        col2.write("biiiip")
