import streamlit as st
import os

from pyaxidraw import axidraw
import sys

def draw_svg(svg_filepath, speed_pendown):
    ad = axidraw.AxiDraw()      # Initialize class
    ad.interactive()            # Enter interactive mode
    connected = ad.connect()    # Open serial port to AxiDraw
    ad.moveto(0, 0)             # Move to the origin
    ad.plot_setup(svg_filepath)     # plot the document
    ad.options.speed_pendown = speed_pendown # Set maximum pen-down speed to 50%
    ad.plot_run()               # plot the document
    return

st.set_page_config(layout="wide")

st.title("Souvenir PyDay Valparaíso - v1")

# Upload a svg file
svg_fileupload = st.file_uploader("Carga un archivo svg", type="svg")

# Slider para setear la velocidad de la lápiz
speed_pendown = st.slider("Velocidad del lápiz", min_value=10, max_value=100, value=50, step=10)

# Button to print the svg file
if svg_fileupload is not None:
    svg_file = os.path.join("tmp", "tmp.svg")
    with open(svg_file, "wb") as f:
        f.write(svg_fileupload.getvalue())
    st.image(svg_file)
    if st.button("Dibujar"):
        draw_svg(svg_file, speed_pendown)