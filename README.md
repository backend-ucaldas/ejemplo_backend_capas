# API de usuarios por capas

Ejemplo de una API REST construida con Flask y organizada en capas:

- `presentation`: rutas y respuestas HTTP.
- `business`: reglas y operaciones de negocio.
- `dataaccess`: lectura y escritura de `data.json`.
- `models`: entidades `User` y `Post`.

## Crear el entorno virtual

Desde esta carpeta, ejecuta:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activacion de scripts, ejecuta PowerShell como usuario y usa:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Instalar dependencias

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Ejecutar la API

Ejecuta desde la raiz del proyecto:

```bash
python -m presentation.app
```

La API quedara disponible en `http://127.0.0.1:5000`.

## Endpoints

- `GET /users`
- `GET /users/<user_id>`
- `POST /users` con `{ "name": "Ana", "email": "ana@example.com" }`
- `PUT /users/<user_id>`
- `DELETE /users/<user_id>`
- `POST /users/<user_id>/posts` con `{ "title": "Titulo", "content": "Contenido" }`

Los datos se guardan en `data.json`.
