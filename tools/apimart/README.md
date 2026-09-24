# APIMart — Artidoro Hero Lab

Tooling local con Node core, sin dependencias adicionales. CP04 utiliza **Nano Banana Pro** (`gemini-3-pro-image-preview`). El video **no forma parte del alcance actual**.

## Configuración

Desde la raíz del repo, copiar `tools/apimart/.env.example` a `tools/apimart/.env` y completar `APIMART_API_KEY`. El archivo `.env` no se versiona; no imprimir ni compartir la clave.

- `TOTAL_BUDGET_USD`: techo total de gasto proyectado para imágenes, sin excepción; por defecto, `5.00` USD.
- `IMAGE_AUTO_BUDGET_USD`: umbral acumulado para imágenes sin `--override-budget "<motivo>"`; por defecto, `1.00` USD. El motivo queda registrado en el ledger y no elimina el techo total.

## Generar y editar imágenes

`generate-image` y `edit-image` usan el mismo endpoint: `POST /v1/images/generations`. Ambos requieren `--model` y `--prompt`; editar exige al menos una referencia mediante `--image-files` o `--image-urls`.

```sh
node tools/apimart/cli.cjs generate-image --model gemini-3-pro-image-preview --prompt "<descripción conceptual>" --resolution 2K --size 16:9
node tools/apimart/cli.cjs edit-image --model gemini-3-pro-image-preview --prompt "<instrucciones de edición>" --image-files "ruta/imagen.png" --resolution 2K --size 16:9
```

`--image-files` acepta rutas locales JPG, JPEG, PNG o WebP separadas por comas, relativas al directorio desde el que se ejecuta el comando; se envían como referencias en base64. `--resolution` indica la resolución (`1K`, `2K` o `4K` para CP04) y `--size`, la relación de aspecto, por ejemplo `1:1` o `16:9`.

## Estado, descarga y ledger

Con el `task_id` devuelto, consultar el estado manualmente; no hay polling automático:

```sh
node tools/apimart/cli.cjs status --task-id <task_id>
node tools/apimart/cli.cjs download --task-id <task_id>
```

Descargar cuando la tarea esté completada: las URLs de resultado expiran en 24 horas. El destino predeterminado es `tools/apimart/data/downloads/<task_id>/`; `--out <carpeta>` permite elegir otro.

El ledger local se guarda en `tools/apimart/data/ledger.json`: registra operaciones, costes estimados, costes reales comunicados al consultar el estado y descargas. Todo `tools/apimart/data/`, incluido el ledger, queda fuera del versionado.
