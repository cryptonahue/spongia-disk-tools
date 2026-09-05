# 🧽 Spongia — Disk Tools

Utilidades de línea de comandos para **analizar el espacio en disco** y **liberar archivos bloqueados**. Una sola herramienta con dos subcomandos.

## ✨ Subcomandos

### 🔍 `find` — Encuentra archivos y carpetas pesadas

Analiza un directorio y muestra los elementos más grandes, con control de tamaño mínimo y cantidad de resultados.

```bash
# Archivos más pesados (≥ 10MB), top 20
python spongia.py find

# Directorio específico
python spongia.py find --dir D:\Descargas

# Tamaño mínimo personalizado
python spongia.py find --dir . --min-size 100MB

# Mostrar las carpetas más pesadas (no archivos)
python spongia.py find dirs --dir .

# Más o menos resultados
python spongia.py find --dir . --top 50
```

### 🗑️ `remove` — Borra archivos que no se pueden borrar

Envía archivos/carpetas a la **papelera** (seguro) o los borra permanentemente. Útil para liberar archivos bloqueados o sin permisos.

```bash
# Borrar a la papelera (con confirmación)
python spongia.py remove archivo_locked.pdf

# Borrar una carpeta (recursivo)
python spongia.py remove ./carpeta -r

# Borrado PERMANENTE (sin papelera)
python spongia.py remove archivo.txt --permanent

# Sin confirmación (scripting)
python spongia.py remove archivo.txt -f
```

> ⚠️ **Seguridad**: el borrado siempre pide confirmación salvo con `-f/--force`, y rechaza borrar directorios del sistema o tu perfil de usuario.

## 🚀 Instalación

```bash
pip install -r requirements.txt
```

### Dependencias

| Paquete | Necesario para | 
|---------|----------------|
| `send2trash` | Borrado seguro a la papelera (opcional) |

## ⚙️ Argumentos

### `find`
| Argumento | Default | Descripción |
|-----------|---------|-------------|
| `mode` | `files` | `files` (archivos) o `dirs` (carpetas) |
| `--dir, -d` | `.` | Directorio a analizar |
| `--min-size` | `10MB` | Tamaño mínimo (ej: `50MB`, `1GB`) |
| `--top` | `20` | Cantidad de resultados |

### `remove`
| Argumento | Default | Descripción |
|-----------|---------|-------------|
| `ruta` | — | Archivo o carpeta a borrar |
| `--recursive, -r` | off | Permite borrar carpetas |
| `--permanent` | off | Borrado permanente (no papelera) |
| `--force, -f` | off | Omite la confirmación |

## 📁 Estructura

```
spongia.py       # CLI principal (toda la lógica)
requirements.txt # Dependencias
LICENSE          # MIT
```

## 📄 Licencia

MIT — ver [LICENSE](LICENSE).
