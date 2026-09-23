# Convocatorias del Estado — Perú

Repositorio que descarga automáticamente, todos los días, los **procedimientos de
selección** publicados por el OSCE (Organismo Supervisor de las Contrataciones del
Estado) a través de su Portal de Contrataciones Abiertas (estándar OCDS), y los
muestra en una página web con buscador y filtros.

Fuente oficial de datos: https://contratacionesabiertas.osce.gob.pe/
(datos públicos, publicados sin restricciones por el propio Estado peruano).

## Cómo funciona

1. Un workflow de GitHub Actions (`.github/workflows/actualizar.yml`) se ejecuta
   todos los días automáticamente.
2. Corre `scripts/obtener_datos.py`, que consulta la API oficial del OSCE y guarda
   los resultados en `docs/data/procedimientos.json`.
3. Si hay datos nuevos, el workflow los sube (commit + push) al repositorio.
4. GitHub Pages sirve la carpeta `docs/` como sitio web — `docs/index.html` lee ese
   mismo JSON y lo muestra con buscador por palabra clave y filtros.

## Configuración inicial (una sola vez)

1. Sube este repositorio a tu cuenta de GitHub.
2. Ve a **Settings → Pages** y en "Source" elige la rama `main` y la carpeta `/docs`.
   Esto te da la URL pública de tu web (algo como
   `https://tu-usuario.github.io/tu-repositorio/`).
3. Ve a **Settings → Actions → General → Workflow permissions** y marca
   **"Read and write permissions"** — sin esto, el workflow no puede subir los
   datos nuevos que descarga cada día.
4. Abre `scripts/obtener_datos.py` y confirma la URL exacta del endpoint de la
   API (ver el aviso dentro del archivo — no pude verificarla en vivo yo mismo
   por restricciones de acceso automatizado al sitio, así que revísala
   navegando tú mismo la sección "API" del portal antes de la primera corrida).

## Correrlo manualmente (para probar)

En GitHub, ve a la pestaña **Actions**, elige el workflow "Actualizar
convocatorias" y dale a **Run workflow** — así no tienes que esperar al
horario programado para ver si funciona.
