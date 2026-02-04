import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
from datetime import datetime

def obtener_datos_paciente():
    """Obtiene los datos del paciente a través de una interfaz."""

    st.title("Formulario de Datos del Paciente")

    dni = st.text_input("Ingrese el DNI del paciente:")
    prestacion_seleccionada = st.radio("Ingrese la prestación realizada:",("Coseguro", "Consulta por Guardia",
                                                                           "Colocacion Inyectable", "Consulta Psiquiatría", 
                                                                           "Consulta Psicología", "Otra" ))
    if prestacion_seleccionada == "Otra":
        prestacion = st.text_input("Ingrese otra prestación:")
    else:
        prestacion = prestacion_seleccionada
    
    # Selector de fecha de consulta
    seleccionar_fecha = st.checkbox("Elegir fecha de consulta")
    
    if seleccionar_fecha:
        fecha_consulta = st.date_input(
            "Fecha de consulta:",
            value=datetime.today(),
            format="DD/MM/YYYY"
        )
        fecha_str = fecha_consulta.strftime("%d/%m/%Y")
        prestacion_con_fecha = f"{prestacion} Consulta {fecha_str}"
    else:
        prestacion_con_fecha = prestacion
    
    tiene_obra_social = st.radio("¿Tiene obra social?", ("Sí", "No"))

    if tiene_obra_social == "Sí":
        obra_social_seleccionada = st.radio("Ingrese la obra social:", ("Apross", "Daspu", "Ospedyc","Otra"))

        if obra_social_seleccionada == "Otra":
           obra_social = st.text_input("Ingrese otra obra social:")
        else:
            obra_social = obra_social_seleccionada
        #obra_social = st.radio("Ingrese la obra social:",("Apross", "Daspu", "Ospedyc",st.text_input("Otra")))
        tipo_afiliacion = st.radio("Tipo de afiliación:", ("Obligatorio", "Voluntario"))
        numero_afiliado = st.text_input("Ingrese el número de afiliado:")
        condicion_iva = "IVA EXENTO" if tipo_afiliacion == "Obligatorio" else "IVA GRAVADO 10.5%"
    else:
        obra_social = "Particular"
        numero_afiliado = ""
        condicion_iva = "IVA GRAVADO 21%"

    # Concatenar los datos para formar el detalle
    #detalle = f"{prestacion} {obra_social} {numero_afiliado} {condicion_iva}"
    if tiene_obra_social == "Sí":
        detalle = f"{prestacion_con_fecha} - Afiliado {obra_social} ({numero_afiliado}) - {condicion_iva}"
    else:
        detalle = f"{prestacion_con_fecha} - {obra_social} - DNI ({dni}) - {condicion_iva}"

    # Crear un botón para copiar el detalle
    if st.button("Copiar al portapapeles"):
     st_copy_to_clipboard(detalle)
     st.success("¡El detalle de facturación se ha copiado al portapapeles!")

    return detalle

# Llama a la función para obtener los datos y el detalle
detalle_facturacion = obtener_datos_paciente()

# Imprime el detalle obtenido
st.write("Detalle de facturación:")
st.write(detalle_facturacion)
