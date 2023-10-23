import streamlit as st

st.set_page_config(page_title = "Inicio")

    # #### Características Principales:
    # - **Predicciones Temporales:** Analiza las tendencias de accidentalidad a nivel diario, semanal y mensual, permitiendo una planificación proactiva y toma de decisiones informada para las autoridades y entidades interesadas.
    # - **Análisis de Factores Relevantes:** Descubre qué variables influyen más en la ocurrencia de accidentes, proporcionando pistas sobre posibles puntos de intervención.
    # - **Desgloses por Tipos de Accidente:** Conoce cómo diferentes tipos de incidentes como choques, atropellos y volcamientos distribuyen en el tiempo y espacio.
    # - **Visualizaciones Interactivas:** Explora mapas y gráficos que facilitan la comprensión de la dinámica de la accidentalidad en la ciudad.
def main():
    st.title('Predicción de incidentes viales en la ciudad de Medellin')
    st.write('''
    Bienvenidos a esta herramienta interactiva que busca ofrecer insights y predicciones sobre la accidentalidad vial en Medellín. Mediante el uso de técnicas avanzadas de análisis de datos y aprendizaje automático, hemos entrenado modelos que permiten entender y prever la dinámica de los accidentes en la ciudad. 



    Esta plataforma ha sido desarrollada utilizando datos abiertos proporcionados por la Alcaldía de Medellín, y tiene como objetivo ser una herramienta valiosa para la prevención y gestión de la seguridad vial en la ciudad.
    ''')

if __name__ == '__main__':
    main()