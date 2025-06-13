import streamlit as st

st.title("Celsius a Fahrenheit")

T_fahrenheit = st.number_input("Temperatura en Fahrenheit", value=50)

T_celsius = (T_fahrenheit - 32) * 5/9

T_celsius_str = f"{T_celsius:.1f} °C"
st.metric(label="Temperatura en Celsius", value=T_celsius_str)

if T_celsius < 0:
    st.write("¡Está helado, Juan!")
    
if T_celsius >= 35:
    st.write("¡A la piscina, Juancho!")
    
