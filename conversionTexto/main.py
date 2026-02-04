import unicodedata
import re
import os
import tkinter as tk
from tkinter import messagebox
import platform # Necesario para identificar el SO
import subprocess # Necesario para abrir archivos en macOS y Linux

# --- Configuración de Archivos ---
NOMBRE_ARCHIVO_SALIDA = "texto_transformado.txt"

# ----------------------------------------------------------------------
# LÓGICA DE TRANSFORMACIÓN
# ----------------------------------------------------------------------

def transformar_texto_numerico(texto_original):
    """
    Transforma un texto: 
    1. Elimina tildes. 
    2. Reemplaza comas decimales por puntos. 
    3. Reemplaza comillas dobles (rectas y tipográficas) por asteriscos.
    4. Reemplaza doble espacio ('  ') por un espacio.
    """
    # 1. Eliminar tildes (acentos)
    texto_sin_tildes = ''.join(
        c for c in unicodedata.normalize('NFD', texto_original)
        if unicodedata.category(c) != 'Mn'
    )

    # 2. Reemplazar comas con puntos SOLO si están entre dígitos
    texto_con_puntos_decimales = re.sub(r'(\d+),(\d+)', r'\1.\2', texto_sin_tildes)

    # 3. Reemplazar comillas dobles (rectas y tipográficas/curvas) con asteriscos (CORREGIDO)
    # Esto busca comillas rectas ("), curvas izquierdas (“) y curvas derechas (”).
    comillas_a_reemplazar = r'[“”"]'
    texto_con_asterisco_comillas = re.sub(comillas_a_reemplazar, '*', texto_con_puntos_decimales)
    
    # 4. Reemplazar doble espacio ('  ') con asteriscos
    texto_final = texto_con_asterisco_comillas.replace('  ', ' ')
    
    return texto_final

# ----------------------------------------------------------------------
# LÓGICA DE INTERFAZ GRÁFICA (GUI)
# ----------------------------------------------------------------------

def abrir_archivo_sistema(filepath):
    """Intenta abrir el archivo con la aplicación predeterminada del sistema operativo."""
    try:
        ruta_absoluta = os.path.abspath(filepath)
        sistema = platform.system()

        if sistema == "Windows":
            # Comando específico de Windows
            os.startfile(ruta_absoluta)
        elif sistema == "Darwin": # macOS
            # Comando específico de macOS
            subprocess.Popen(['open', ruta_absoluta])
        else: # Linux/Otros (usa xdg-open)
            # Comando específico de Linux (ej. Ubuntu, Debian)
            subprocess.Popen(['xdg-open', ruta_absoluta])
            
    except Exception as e:
        # Imprime una advertencia en la consola si falla, pero no interrumpe el flujo.
        print(f"ADVERTENCIA: No se pudo abrir el archivo automáticamente. Detalle: {e}")


def guardar_texto(texto_transformado, ventana_principal):
    """Guarda el texto transformado, notifica al usuario y abre el archivo."""
    
    try:
        # Exportación al archivo .txt
        with open(NOMBRE_ARCHIVO_SALIDA, 'w', encoding='utf-8') as archivo_salida:
            archivo_salida.write(texto_transformado)
        
        # Verificación explícita de la existencia
        if os.path.exists(NOMBRE_ARCHIVO_SALIDA):
            ruta_absoluta = os.path.abspath(NOMBRE_ARCHIVO_SALIDA)
            
            messagebox.showinfo(
                "✅ Éxito",
                f"¡Texto transformado y guardado correctamente!\n\n"
                f"Archivo: {NOMBRE_ARCHIVO_SALIDA}\n"
                f"Ubicación: {ruta_absoluta}"
            )
            
            # --- Abrir el archivo inmediatamente después del mensaje ---
            abrir_archivo_sistema(NOMBRE_ARCHIVO_SALIDA)
            # -----------------------------------------------------------------
            
            # Cierra la ventana después de guardar exitosamente
            ventana_principal.destroy()
        else:
            messagebox.showwarning("Advertencia", "Se intentó guardar, pero no se pudo confirmar la existencia del archivo.")

    except IOError as e:
        messagebox.showerror("❌ Error de Escritura", f"Falló la escritura del archivo.\nDetalle: {e}")


def procesar_y_guardar(text_widget, ventana_principal):
    """Obtiene el texto del widget, lo transforma y lo guarda."""
    
    # Obtener todo el contenido del widget de texto
    texto_input = text_widget.get("1.0", tk.END)
    
    # Si después de strip() la cadena sigue vacía, entonces realmente no hay texto útil.
    if not texto_input.strip():
        messagebox.showerror("Error de Entrada", "Por favor, pega el texto que deseas transformar en el área de texto.")
        return

    # Transformar
    texto_transformado = transformar_texto_numerico(texto_input)
    
    # Guardar y notificar
    guardar_texto(texto_transformado, ventana_principal)


def iniciar_gui():
    """Crea y ejecuta la ventana principal de la aplicación."""
    
    # 1. Configuración de la Ventana Principal
    root = tk.Tk()
    root.title("Text Transformer (GUI) V2.1")
    
    # 2. Etiqueta de Instrucción
    tk.Label(
        root, 
        text="Pega tu texto multilinea en la caja de abajo y haz clic en 'Transformar y Guardar':",
        pady=10
    ).pack(padx=10)

    # 3. Área de Texto para Pegar (Text Widget)
    text_area = tk.Text(root, wrap=tk.WORD, width=80, height=20, font=("Arial", 10))
    text_area.pack(padx=10, pady=5)

    # 4. Botón de Procesamiento
    tk.Button(
        root, 
        text="🚀 Transformar y Guardar", 
        command=lambda: procesar_y_guardar(text_area, root),
        bg='green', 
        fg='white', 
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    # Iniciar el bucle principal de la GUI
    root.mainloop()


# Ejecuta la función principal para iniciar la aplicación de ventana
if __name__ == "__main__":
    iniciar_gui()
