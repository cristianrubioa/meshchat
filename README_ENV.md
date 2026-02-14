# Environment Configuration

## Variables de Entorno

Todas las variables usan el prefijo `MESHCHAT_`:

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `MESHCHAT_PORT` | int | 2323 | Puerto TCP |
| `MESHCHAT_ROOM_NAME` | str | "Chat Room" | Nombre de la sala |
| `MESHCHAT_MAX_USERS` | int | 10 | Usuarios máximos |
| `MESHCHAT_ENABLE_HISTORY` | bool | false | Habilitar historial |
| `MESHCHAT_HISTORY_SIZE` | int | 50 | Tamaño del historial |
| `MESHCHAT_PLAIN_TEXT` | bool | false | Modo texto plano |
| `MESHCHAT_LOG_LEVEL` | str | INFO | Nivel de log |

## Ejemplo .env

```bash
cp .env.example .env
```

Contenido:
```env
MESHCHAT_HOST=0.0.0.0
MESHCHAT_PORT=2323
MESHCHAT_ROOM_NAME="Chat Room"
MESHCHAT_MAX_USERS=10
MESHCHAT_ENABLE_HISTORY=false
MESHCHAT_HISTORY_SIZE=50
MESHCHAT_PLAIN_TEXT=false
MESHCHAT_LOG_LEVEL=INFO
MESHCHAT_MAX_MESSAGE_LENGTH=1000
MESHCHAT_RATE_LIMIT_MAX_MESSAGES=5
MESHCHAT_RATE_LIMIT_WINDOW_SECONDS=5
MESHCHAT_MAX_NICKNAME_LEN=20
MESHCHAT_MIN_NICKNAME_LEN=2
```

## Prioridad de Configuración

1. **Defaults** (definidos en código)
2. **Environment variables** (archivo .env)
3. **CLI arguments** (sobrescriben todo)

## Cache

La configuración se cachea con `@lru_cache` para evitar lecturas repetidas del .env.
