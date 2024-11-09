import streamlit as st

def obtener_datos_paciente():
    """Obtiene los datos del paciente a través de una interfaz."""

    st.title("Formulario de Datos del Paciente")

    dni = st.text_input("Ingrese el DNI del paciente:")

    tiene_obra_social = st.radio("¿Tiene obra social?", ("Sí", "No"))

    if tiene_obra_social == "Sí":
        tipo_afiliacion = st.radio("Tipo de afiliación:", ("Voluntario", "Obligatorio"))
        numero_afiliado = st.text_input("Ingrese el número de afiliado:")

    # Aquí puedes agregar más campos si necesitas capturar otra información

    # Retorna un diccionario con los datos ingresados
    datos = {
        "dni": dni,
        "tiene_obra_social": tiene_obra_social,
        "tipo_afiliacion": tipo_afiliacion if tiene_obra_social == "Sí" else None,
        "numero_afiliado": numero_afiliado if tiene_obra_social == "Sí" else None
    }

    return datos

# Llama a la función para obtener los datos
datos_paciente = obtener_datos_paciente()

# Imprime los datos obtenidos (solo para demostración)
st.write("Datos ingresados:")
st.write(datos_paciente)