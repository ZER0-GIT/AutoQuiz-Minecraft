import json
import os
import time
import pyperclip
import keyboard

def cargar_configuracion():
    ruta_config = "C:/Users/Administrador/Desktop/Yep/config.json"
    with open(ruta_config, "r") as config_file:
        config = json.load(config_file)
        return config

def cargar_respuestas():
    ruta_respuestas = "C:/Users/Administrador/Desktop/Yep/respuestas.json"
    with open(ruta_respuestas, "r") as respuestas_file:
        respuestas = json.load(respuestas_file)
        return respuestas

def leer_ultima_linea(archivo):
    with open(archivo, "r") as f:
        lineas = f.readlines()
        if lineas:
            return lineas[-1].strip()
        else:
            return None

def leer_nuevas_lineas(archivo, posicion_anterior):
    with open(archivo, "r") as f:
        f.seek(posicion_anterior)
        nuevas_lineas = f.readlines()
        posicion_actual = f.tell()
        return nuevas_lineas, posicion_actual

def buscar_respuesta(entrada, respuestas):
    for clave, valor in respuestas.items():
        if clave in entrada:
            return valor
    return None

def interactuar_teclado(respuesta):
    pyperclip.copy(respuesta)
    time.sleep(0.5)
    keyboard.press_and_release('T')
    time.sleep(1)
    keyboard.press_and_release('ctrl+v, enter')

def main():
    config = cargar_configuracion()
    ruta_log = config.get("ruta_log")
    ruta_respuestas = config.get("ruta_respuestas")

    if not os.path.exists(ruta_log) or not os.path.exists(ruta_respuestas):
        print("Error: Las rutas especificadas en el archivo de configuración no son válidas.")
        return

    respuestas = cargar_respuestas()

    # Leer la última línea existente al inicio
    ultima_linea = leer_ultima_linea(ruta_log)
    if ultima_linea:
        entrada = ultima_linea.strip()
        respuesta = buscar_respuesta(entrada, respuestas)

        if respuesta:
            print(f"{time.ctime()}: {respuesta}")
            interactuar_teclado(respuesta)

    posicion_anterior = os.path.getsize(ruta_log)

    while True:
        nuevas_lineas, posicion_actual = leer_nuevas_lineas(ruta_log, posicion_anterior)

        for nueva_linea in nuevas_lineas:
            entrada = nueva_linea.strip()

            respuesta = buscar_respuesta(entrada, respuestas)

            if respuesta:
                print(f"{time.ctime()}: {respuesta}")
                interactuar_teclado(respuesta)

        posicion_anterior = posicion_actual
        time.sleep(1)

if __name__ == "__main__":
    main()