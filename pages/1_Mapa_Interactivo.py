import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(page_title = "Mapa Interactivo")
def main():
    st.title('Mapa interactivo de la accidentalidad en la ciudad de Medellín')

    with open("maps/map.html", "r") as f:
        map_html = f.read()
    
    components.html(map_html, width=700, height=500)


if __name__ == '__main__':
    main()
