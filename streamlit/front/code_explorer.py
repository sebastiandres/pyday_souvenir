import streamlit as st
import glob
import os


st.set_page_config(layout="wide")

st.title("Explorador de código")

current_dir = os.path.dirname(os.path.abspath(__file__))

filepaths = sorted(glob.glob(os.path.join(current_dir, "v*.py")))
filenames = [os.path.basename(filepath) for filepath in filepaths]

file_sel = st.selectbox("Selecciona un archivo", filenames)

st.code(open(os.path.join(current_dir, file_sel)).read(), language="python")
