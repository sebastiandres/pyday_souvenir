import streamlit as st
import os

# Configure pages
pages = [
    os.path.join("front", "v1.py"),
    os.path.join("front", "v2.py"),
    os.path.join("front", "v3.py"),
    os.path.join("front", "v4.py"),
    os.path.join("front", "code_explorer.py"),
]

# Use navigation to show the page
pg = st.navigation(pages)
pg.run()

