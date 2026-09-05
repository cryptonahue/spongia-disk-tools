# -*- coding: utf-8 -*-

import unicodedata
"""Traducciones para Spongia (español, inglés, portugués de Brasil)."""

MESSAGES = {
    # Descripción general
    "desc_find": {
        "es": "Encuentra archivos/carpetas pesadas",
        "en": "Find heavy files/folders",
        "pt": "Encontra arquivos/pastas pesados",
    },
    "desc_remove": {
        "es": "Borra archivos/carpetas (a la papelera)",
        "en": "Delete files/folders (to trash)",
        "pt": "Apaga arquivos/pastas (para a lixeira)",
    },
    # find
    "dir_help": {
        "es": "Directorio a analizar (default: .)",
        "en": "Directory to analyze (default: .)",
        "pt": "Diretório a analisar (padrão: .)",
    },
    "min_size_help": {
        "es": "Tamaño mínimo (ej: 50MB, 1GB). Default: 10MB",
        "en": "Minimum size (e.g. 50MB, 1GB). Default: 10MB",
        "pt": "Tamanho mínimo (ex.: 50MB, 1GB). Padrão: 10MB",
    },
    "top_help": {
        "es": "Cantidad de resultados (default: 20)",
        "en": "Number of results (default: 20)",
        "pt": "Quantidade de resultados (padrão: 20)",
    },
    "mode_help": {
        "es": "files=archivos, dirs=carpetas (default: files)",
        "en": "files=files, dirs=folders (default: files)",
        "pt": "files=arquivos, dirs=pastas (padrão: files)",
    },
    "min_size_invalid": {
        "es": "--min-size inválido: {value}",
        "en": "Invalid --min-size: {value}",
        "pt": "--min-size inválido: {value}",
    },
    "description": {
        "es": "Herramientas para analizar y liberar espacio en disco.",
        "en": "Tools to analyze and free disk space.",
        "pt": "Ferramentas para analisar e liberar espaço em disco.",
    },
    "table_header": {
        "es": "#   Tamaño     Archivo",
        "en": "#   Size       File",
        "pt": "#   Tamanho    Arquivo",
    },
    "exclude_help": {
        "es": "Patrón a excluir; se puede repetir (ej: .git, *.pyc)",
        "en": "Pattern to exclude; may be repeated (e.g. .git, *.pyc)",
        "pt": "Padrão a excluir; pode ser repetido (ex.: .git, *.pyc)",
    },
    "top_invalid": {
            "es": "--top debe ser mayor que cero: {value}",
            "en": "--top must be greater than zero: {value}",
            "pt": "--top deve ser maior que zero: {value}",
        },
        "dir_not_found": {
        "es": "❌ Directorio no existe: {dir}",
        "en": "❌ Directory does not exist: {dir}",
        "pt": "❌ Diretório não existe: {dir}",
    },
    "scan_progress": {
        "es": "🔄 Revisados: {files} archivos | Carpeta: {dir}",
        "en": "🔄 Checked: {files} files | Directory: {dir}",
        "pt": "🔄 Verificados: {files} arquivos | Pasta: {dir}",
    },
    "scan_complete": {
        "es": "✅ Escaneo terminado: {files} archivos revisados.",
        "en": "✅ Scan complete: {files} files checked.",
        "pt": "✅ Varredura concluída: {files} arquivos verificados.",
    },
    "searching_files": {
        "es": "🔍 Buscando archivos pesados ≥ {min} MB...",
        "en": "🔍 Searching heavy files ≥ {min} MB...",
        "pt": "🔍 Procurando arquivos pesados ≥ {min} MB...",
    },
    "directory": {
        "es": "📁 Directorio: {dir}",
        "en": "📁 Directory: {dir}",
        "pt": "📁 Diretório: {dir}",
    },
    "top_title": {
        "es": "TOP {n} ARCHIVOS MÁS PESADOS ({time:.1f}s, {files} archivos)",
        "en": "TOP {n} HEAVIEST FILES ({time:.1f}s, {files} files)",
        "pt": "TOP {n} ARQUIVOS MAIS PESADOS ({time:.1f}s, {files} arquivos)",
    },
    "total_listed": {
        "es": "📊 Total listado: {size}",
        "en": "📊 Total listed: {size}",
        "pt": "📊 Total listado: {size}",
    },
    "calculating_dirs": {
        "es": "📊 Calculando tamaños de carpetas en: {dir}",
        "en": "📊 Calculating folder sizes in: {dir}",
        "pt": "📊 Calculando tamanhos de pastas em: {dir}",
    },
    "analyzing": {
        "es": "   Analizando {name}...",
        "en": "   Analyzing {name}...",
        "pt": "   Analisando {name}...",
    },
    "dirs_title": {
        "es": "ELEMENTOS MÁS PESADOS EN '{name}'",
        "en": "HEAVIEST ITEMS IN '{name}'",
        "pt": "ITENS MAIS PESADOS EM '{name}'",
    },
    "total_size": {
        "es": "📊 Total: {size}",
        "en": "📊 Total: {size}",
        "pt": "📊 Total: {size}",
    },
    # remove
    "ruta_help": {
        "es": "Archivo o carpeta a borrar",
        "en": "File or folder to delete",
        "pt": "Arquivo ou pasta a apagar",
    },
    "recursive_help": {
        "es": "Permite borrar carpetas (recursivo)",
        "en": "Allow deleting folders (recursive)",
        "pt": "Permite apagar pastas (recursivo)",
    },
    "permanent_help": {
        "es": "Borrado PERMANENTE (no va a la papelera)",
        "en": "PERMANENT deletion (not to trash)",
        "pt": "Exclusão PERMANENTE (não para a lixeira)",
    },
    "force_help": {
        "es": "Omite la confirmación",
        "en": "Skip confirmation",
        "pt": "Ignora confirmação",
    },
    "not_found": {
        "es": "❌ No existe: {ruta}",
        "en": "❌ Does not exist: {ruta}",
        "pt": "❌ Não existe: {ruta}",
    },
    "protected": {
        "es": "⛔ Rechazado: no se puede borrar directorio protegido {dir}",
        "en": "⛔ Rejected: cannot delete protected directory {dir}",
        "pt": "⛔ Rejeitado: não é possível apagar diretório protegido {dir}",
    },
    "is_dir_warning": {
        "es": "⚠️  '{target}' es una carpeta. Usa --recursive para borrarla.",
        "en": "⚠️  '{target}' is a folder. Use --recursive to delete it.",
        "pt": "⚠️  '{target}' é uma pasta. Use --recursive para apagá-la.",
    },
    "target": {
        "es": "📦 Objetivo: {target}",
        "en": "📦 Target: {target}",
        "pt": "📦 Alvo: {target}",
    },
    "method": {
        "es": "🚮 Método  : {method}",
        "en": "🚮 Method  : {method}",
        "pt": "🚮 Método  : {method}",
    },
    "method_trash": {
        "es": "Papelera",
        "en": "Trash",
        "pt": "Lixeira",
    },
    "method_permanent": {
        "es": "Borrado permanente",
        "en": "Permanent deletion",
        "pt": "Exclusão permanente",
    },
    "destination_trash": {
            "es": "la papelera",
            "en": "the trash",
            "pt": "a lixeira",
        },
        "destination_permanent": {
            "es": "PERDERLO para siempre",
            "en": "PERMANENT deletion",
            "pt": "PERDÊ-LO para sempre",
        },
        "confirm_question": {
        "es": "¿Seguro que querés enviar '{name}' a {dest}? [s/N] ",
        "en": "Are you sure you want to send '{name}' to {dest}? [y/N] ",
        "pt": "Tem certeza que deseja enviar '{name}' para {dest}? [s/N] ",
    },
    "cancelled": {
        "es": "⏭️  Cancelado.",
        "en": "⏭️  Cancelled.",
        "pt": "⏭️  Cancelado.",
    },
    "trashed": {
        "es": "✅ Enviado a la papelera: {target}",
        "en": "✅ Sent to trash: {target}",
        "pt": "✅ Enviado para a lixeira: {target}",
    },
    "no_send2trash": {
        "es": "⚠️  send2trash no instalado. Usando borrado permanente.",
        "en": "⚠️  send2trash not installed. Using permanent deletion.",
        "pt": "⚠️  send2trash não instalado. Usando exclusão permanente.",
    },
    "confirm_permanent": {
        "es": "¿Continuar con BORRADO PERMANENTE? [s/N] ",
        "en": "Continue with PERMANENT deletion? [y/N] ",
        "pt": "Continuar com EXCLUSÃO PERMANENTE? [s/N] ",
    },
    "deleted_perm": {
        "es": "✅ Borrado permanentemente: {target}",
        "en": "✅ Permanently deleted: {target}",
        "pt": "✅ Excluído permanentemente: {target}",
    },
    "permission_denied": {
        "es": "❌ Permiso denegado (probablemente en uso por otro proceso).",
        "en": "❌ Permission denied (probably in use by another process).",
        "pt": "❌ Permissão negada (provavelmente em uso por outro processo).",
    },
    "permission_hint": {
        "es": "💡 Cerrá el programa que lo usa, o ejecutá como administrador.",
        "en": "💡 Close the program using it, or run as administrator.",
        "pt": "💡 Feche o programa que o usa, ou execute como administrador.",
    },
    "error": {
        "es": "❌ Error: {error}",
        "en": "❌ Error: {error}",
        "pt": "❌ Erro: {error}",
    },
    "lang_help": {
        "es": "Idioma: es, en, pt (default: en)",
        "en": "Language: es, en, pt (default: en)",
        "pt": "Idioma: es, en, pt (padrão: en)",
    },


}


def text(lang, key, **kwargs):
    """Traduce y formatea un mensaje."""
    template = MESSAGES[key][lang]
    return template.format(**kwargs)


def confirm_si(value, lang="en"):
    """Devuelve True si el valor ingresado es afirmativo."""
    normalized = unicodedata.normalize("NFKD", value.strip().lower())
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    if lang == "en":
        return normalized in ("y", "yes")
    return normalized in ("s", "si", "sim", "y", "yes")
