"""
Descarga los procedimientos de selección más recientes desde el Portal de
Contrataciones Abiertas del OSCE (estándar OCDS) y los guarda como JSON
para que la página web (docs/index.html) los muestre.

*** AVISO IMPORTANTE ***
No pude verificar en vivo la URL exacta del endpoint porque el sitio del
OSCE bloquea el acceso automatizado a su página principal para herramientas
como la mía. Antes de tu primera corrida:

  1. Entra tú mismo, en tu navegador, a https://contratacionesabiertas.osce.gob.pe/
  2. Ve a la sección "API" del portal (documentación de endpoints "release",
     "record" y "files").
  3. Copia ahí la URL base exacta del endpoint de "release" (o el que uses
     para traer procedimientos recientes) y reemplaza la variable
     URL_BASE_API de abajo con esa URL real.
  4. Revisa también qué parámetros acepta para filtrar por fecha (puede
     llamarse dateFrom/dateTo, updatedFrom, o algo similar) y ajusta la
     función construir_parametros() según lo que documente el portal.

Mientras no confirmes esa URL, el script no funcionará — está escrito con
la estructura típica de una API OCDS, pero el detalle exacto depende de
cómo lo implementó el OSCE.
"""

import json
import os
from datetime import datetime, timedelta, timezone

import requests

# TODO: reemplaza esto con la URL real que confirmes en el portal
URL_BASE_API = "https://contratacionesabiertas.osce.gob.pe/api/v1/release"

RUTA_SALIDA = "docs/data/procedimientos.json"
DIAS_HACIA_ATRAS = 7  # trae lo publicado/actualizado en los últimos N días


def construir_parametros():
    """
    Ajusta estos nombres de parámetros según la documentación real de la API.
    Este es un punto de partida típico para una API que sigue el estándar OCDS.
    """
    desde = (datetime.now(timezone.utc) - timedelta(days=DIAS_HACIA_ATRAS)).strftime("%Y-%m-%d")
    return {
        "dateFrom": desde,
        "pageSize": 500,
    }


def obtener_datos():
    parametros = construir_parametros()
    print(f"Consultando: {URL_BASE_API} con parámetros {parametros}")

    respuesta = requests.get(URL_BASE_API, params=parametros, timeout=60)
    respuesta.raise_for_status()
    datos = respuesta.json()

    # La forma de la respuesta depende de si es un "release package" o "record package".
    # Ajusta esta línea según lo que realmente devuelva el endpoint.
    procedimientos = datos.get("releases", datos.get("records", []))

    resultado = {
        "actualizado_el": datetime.now(timezone.utc).isoformat(),
        "cantidad": len(procedimientos),
        "procedimientos": procedimientos,
    }
    return resultado


def guardar(datos):
    os.makedirs(os.path.dirname(RUTA_SALIDA), exist_ok=True)
    with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"Guardados {datos['cantidad']} procedimientos en {RUTA_SALIDA}")


if __name__ == "__main__":
    datos = obtener_datos()
    guardar(datos)
