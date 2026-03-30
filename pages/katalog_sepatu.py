import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="KlikSepatu | Katalog",
    page_icon="👟",
    layout="wide"
)

st.title("Selamat datang di Katalog KlikSepatu!")
st.write("""
Temukan koleksi sepatu *sneakers*, *boots*, hingga sepatu olahraga terbaik di sini. 
""")

data = pd.read_csv("data/products_table.csv")
st.write(data)