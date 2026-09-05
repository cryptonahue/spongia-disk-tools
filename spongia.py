#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Spongia — Disk Tools: análisis y limpieza de espacio en disco.

Consolida las herramientas de "archivos pesados" y agrega una
utilidad para liberar archivos bloqueados.
Idiomas soportados: español (es), inglés (en), portugués de Brasil (pt).

Subcomandos:
    find     Encuentra y analiza archivos/carpetas pesadas
    remove   Borra (a la papelera) archivos que no se pueden borrar
             normalmente (en uso, sin permisos, etc.)

Uso:
    python spongia.py find --dir . --min-size 100MB --lang pt
    python spongia.py find --dir . --top 20
    python spongia.py find dirs            # muestra carpetas más pesadas
    python spongia.py remove <ruta>

Idiomas soportados (--lang | -L): es, en, pt (default: en)
"""

import argparse
import fnmatch
import heapq
import os
import sys
import time
from pathlib import Path

# Forzar UTF-8 en consolas Windows para poder mostrar emojis/acentos
if sys.platform == "win32":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

from spongia_translations import confirm_si, text  # noqa: E402

SUPPORTED_LANGS = {
    "es": "es", "español": "es", "spanish": "es",
    "en": "en", "english": "en", "inglés": "en", "ingles": "en",
    "pt": "pt", "pt-br": "pt", "pt_br": "pt", "brasil": "pt", "brazilian": "pt",
}


def resolve_lang(value):
    """Normaliza el valor --lang a es/en/pt (por defecto inglés)."""
    return SUPPORTED_LANGS.get(str(value).strip().lower(), "en")


# ---------------------------------------------------------------------------
# Colores ANSI para terminal
# ---------------------------------------------------------------------------
class Colores:
    ROJO = "\033[91m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    AZUL = "\033[94m"
    MAGENTA = "\033[95m"
    CIAN = "\033[96m"
    BLANCO = "\033[97m"
    RESET = "\033[0m"
    NEGRITA = "\033[1m"
    DIM = "\033[2m"


def format_size(size: float) -> str:
    """Convierte bytes a formato legible (B, KB, MB, GB, TB...)."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"


def parse_size(text: str) -> int:
    """Convierte una cadena como '100MB' o '2GB' a bytes."""
    text = text.strip().upper()
    units = {
        "B": 1,
        "KB": 1024,
        "MB": 1024 ** 2,
        "GB": 1024 ** 3,
        "TB": 1024 ** 4,
    }
    for unit, mult in sorted(units.items(), key=lambda x: len(x[0]), reverse=True):
        if text.endswith(unit):
            return int(float(text[: -len(unit)].strip()) * mult)
    return int(float(text))


def is_excluded(path, patterns):
    """Return True when a file or directory matches an exclusion pattern."""
    path = Path(path)
    candidates = {path.name, str(path), path.as_posix(), *path.parts}
    return any(fnmatch.fnmatch(candidate, pattern) for pattern in patterns for candidate in candidates)


def matches_extension(path, extensions):
    """Return True when a file matches one of the requested extensions."""
    if not extensions:
        return True
    suffix = Path(path).suffix.lower()
    normalized = {ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in extensions}
    return suffix in normalized


# ---------------------------------------------------------------------------
# Subcomando: find — archivos pesados
# ---------------------------------------------------------------------------
def find_largest_files(directory, top_n=20, min_size_mb=10, lang="en", excludes=(), extensions=()):
    """Encuentra los N archivos más pesados ≥ min_size usando un heap."""
    root = Path(directory).resolve()
    if not root.is_dir():
        print(f"{Colores.ROJO}{text(lang, 'dir_not_found', dir=directory)}{Colores.RESET}")
        return

    min_bytes = min_size_mb * 1024 * 1024
    heap = []
    files_checked = 0

    print(f"{Colores.CIAN}{text(lang, 'searching_files', min=min_size_mb)}{Colores.RESET}")
    print(f"{Colores.MAGENTA}{text(lang, 'directory', dir=root)}{Colores.RESET}")
    inicio = time.time()

    last_report = time.monotonic()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames
                       if not is_excluded(Path(dirpath) / name, excludes)]
        for name in filenames:
            if is_excluded(Path(dirpath) / name, excludes):
                continue
            files_checked += 1
            now = time.monotonic()
            if files_checked == 1 or now - last_report >= 1:
                print(f"\r{Colores.CIAN}{text(lang, 'scan_progress', files=files_checked, dir=dirpath)}{Colores.RESET}", end="", flush=True)
                last_report = now
            filepath = os.path.join(dirpath, name)
            try:
                size = os.path.getsize(filepath)
            except (OSError, PermissionError):
                continue
            if size >= min_bytes:
                if len(heap) < top_n:
                    heapq.heappush(heap, (size, filepath))
                elif size > heap[0][0]:
                    heapq.heappushpop(heap, (size, filepath))

    print(f"\r{Colores.VERDE}{text(lang, 'scan_complete', files=files_checked)}{Colores.RESET}")
    top = sorted(heap, key=lambda x: x[0], reverse=True)
    elapsed = time.time() - inicio

    print(f"\n{Colores.AMARILLO}{'=' * 78}{Colores.RESET}")
    print(f"{Colores.NEGRITA}{text(lang, 'top_title', n=len(top), time=elapsed, files=files_checked)}{Colores.RESET}")
    print(f"{Colores.AMARILLO}{'=' * 78}{Colores.RESET}")
    print(text(lang, 'table_header'))

    total = 0
    for i, (size, path) in enumerate(top, 1):
        total += size
        try:
            rel = os.path.relpath(path, root)
        except ValueError:
            rel = path
        print(f"{i:<3} {format_size(size):<10} {rel}")

    print(f"{Colores.AMARILLO}{'=' * 78}{Colores.RESET}")
    print(f"{Colores.AZUL}{text(lang, 'total_listed', size=format_size(total))}{Colores.RESET}")


def find_largest_dirs(directory, top_n=15, lang="en", excludes=(), min_size_mb=0, extensions=()):
    """Muestra las carpetas de un nivel con mayor tamaño total."""
    root = Path(directory).resolve()
    if not root.is_dir():
        print(f"{Colores.ROJO}{text(lang, 'dir_not_found', dir=directory)}{Colores.RESET}")
        return

    items = []
    print(f"{Colores.CIAN}{text(lang, 'calculating_dirs', dir=root)}{Colores.RESET}")

    def dir_size(path):
        total = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                dirnames[:] = [name for name in dirnames
                               if not is_excluded(Path(dirpath) / name, excludes)]
                for name in filenames:
                    file_path = Path(dirpath) / name
                    if is_excluded(file_path, excludes) or not matches_extension(file_path, extensions):
                        continue
                    try:
                        size = file_path.stat().st_size
                        if size >= min_size_mb * 1024 * 1024:
                            total += size
                    except OSError:
                        pass
        except OSError:
            pass
        return total

    for entry in root.iterdir():
        if is_excluded(entry, excludes):
            continue
        if entry.is_dir():
            print(text(lang, "analyzing", name=entry.name))
            items.append((dir_size(entry), entry.name))
        elif entry.is_file() and matches_extension(entry, extensions):
            try:
                size = entry.stat().st_size
                if size >= min_size_mb * 1024 * 1024:
                    items.append((size, entry.name))
            except OSError:
                pass


    items.sort(key=lambda x: x[0], reverse=True)
    print(f"\n{Colores.AMARILLO}{'=' * 78}{Colores.RESET}")
    print(f"{Colores.NEGRITA}{text(lang, 'dirs_title', name=root.name)}{Colores.RESET}")
    total = sum(s for s, _ in items)
    for i, (size, name) in enumerate(items[:top_n], 1):
        print(f"{i:2}. {format_size(size):>12} - {name}")
    print(f"\n{Colores.AZUL}{text(lang, 'total_size', size=format_size(total))}{Colores.RESET}")


# ---------------------------------------------------------------------------
# Subcomando: remove — liberar archivos bloqueados
# ---------------------------------------------------------------------------
def _puede_borrar_permisos(path: Path) -> bool:
    """Intenta comprobar si el archivo/carpeta es accesible para borrado."""
    return os.access(path, os.W_OK)


def remove_path(ruta, to_trash=True, recursive=False, force=False,
                protected_dirs=None, lang="en"): 
    """
    Borra un archivo o carpeta. Por defecto va a la PAPELERA (seguro).
    force=True omite la confirmación interactiva.
    """
    if protected_dirs is None:
        protected_dirs = [os.path.expanduser("~"), os.environ.get("SystemRoot", "C:\\Windows")]

    target = Path(ruta).expanduser().absolute()

    if not target.exists() and not target.is_symlink():
        print(f"{Colores.ROJO}{text(lang, 'not_found', ruta=ruta)}{Colores.RESET}")
        return 1

    # No permitir borrar el perfil, el sistema ni sus descendientes.
    target_real = target.resolve()
    for prot in protected_dirs:
        if not prot:
            continue
        protected_real = Path(prot).expanduser().resolve()
        if target_real == protected_real or protected_real in target_real.parents:
            print(f"{Colores.ROJO}{text(lang, 'protected', dir=target_real)}{Colores.RESET}")
            return 1

    if target.is_dir() and not target.is_symlink() and not recursive:
        print(f"{Colores.AMARILLO}{text(lang, 'is_dir_warning', target=target)}{Colores.RESET}")
        return 1

    print(f"{Colores.CIAN}{text(lang, 'target', target=target)}{Colores.RESET}")
    method_key = "method_trash" if to_trash else "method_permanent"
    print(f"{Colores.CIAN}{text(lang, 'method', method=text(lang, method_key))}{Colores.RESET}")

    if not force:
        destination_key = "destination_trash" if to_trash else "destination_permanent"
        confirmar = input(text(lang, "confirm_question", name=target.name,
                               dest=text(lang, destination_key))).strip()
        if not confirm_si(confirmar, lang):
            print(f"{Colores.AMARILLO}{text(lang, 'cancelled')}{Colores.RESET}")
            return 0

    try:
        if to_trash:
            try:
                from send2trash import send2trash
                send2trash(str(target))
                print(f"{Colores.VERDE}{text(lang, 'trashed', target=target)}{Colores.RESET}")
            except ImportError:
                print(f"{Colores.AMARILLO}{text(lang, 'no_send2trash')}{Colores.RESET}")
                if not force:
                    c = input(text(lang, "confirm_permanent")).strip()
                    if not confirm_si(c, lang):
                        return 0
                if target.is_dir() and not target.is_symlink():
                    import shutil
                    shutil.rmtree(target)
                else:
                    target.unlink()
                print(f"{Colores.VERDE}{text(lang, 'deleted_perm', target=target)}{Colores.RESET}")
        else:
            if target.is_dir() and not target.is_symlink():
                import shutil
                shutil.rmtree(target)
            else:
                target.unlink()
            print(f"{Colores.VERDE}{text(lang, 'deleted_perm', target=target)}{Colores.RESET}")
        return 0
    except PermissionError:
        print(f"{Colores.ROJO}{text(lang, 'permission_denied')}{Colores.RESET}")
        print(f"{Colores.AMARILLO}{text(lang, 'permission_hint')}{Colores.RESET}")
        return 1
    except OSError as e:
        print(f"{Colores.ROJO}{text(lang, 'error', error=e)}{Colores.RESET}")
        return 1


# ---------------------------------------------------------------------------
# CLI principal
# ---------------------------------------------------------------------------
def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="spongia",
        description=text("en", "description"),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # find
    find_p = subparsers.add_parser("find", help=text("en", "desc_find"))
    find_p.add_argument("--dir", "-d", default=".", help=text("en", "dir_help"))
    find_p.add_argument("--min-size", type=str, default="10MB", help=text("en", "min_size_help"))
    find_p.add_argument("--top", type=int, default=20, help=text("en", "top_help"))
    find_p.add_argument("--exclude", action="append", default=[],
        help=text("en", "exclude_help"))
    find_p.add_argument("mode", nargs="?", default="files", choices=["files", "dirs"],
                        help=text("en", "mode_help"))
    find_p.add_argument("--lang", "-L", default="en", choices=sorted(SUPPORTED_LANGS.keys()),
                        help=text("en", "lang_help"))

    # remove
    rm_p = subparsers.add_parser("remove", help=text("en", "desc_remove"))
    rm_p.add_argument("ruta", help=text("en", "ruta_help"))
    rm_p.add_argument("--recursive", "-r", action="store_true", help=text("en", "recursive_help"))
    rm_p.add_argument("--permanent", action="store_true", help=text("en", "permanent_help"))
    rm_p.add_argument("--force", "-f", action="store_true", help=text("en", "force_help"))
    rm_p.add_argument("--lang", "-L", default="en", choices=sorted(SUPPORTED_LANGS.keys()),
                           help=text("en", "lang_help"))

    args = parser.parse_args(argv)

    lang = resolve_lang(getattr(args, "lang", "en"))

    if args.command == "find":
        try:
            min_bytes = parse_size(args.min_size)
        except (TypeError, ValueError):
            parser.error(text(lang, "min_size_invalid", value=args.min_size))
        if min_bytes < 0:
            parser.error(text(lang, "min_size_invalid", value=args.min_size))
        if args.top < 1:
            parser.error(text(lang, "top_invalid", value=args.top))
        min_mb = min_bytes / (1024 * 1024)
        if args.mode == "dirs":
            find_largest_dirs(args.dir, top_n=args.top, lang=lang, excludes=args.exclude, min_size_mb=min_mb, extensions=args.extension)
        else:
            find_largest_files(args.dir, top_n=args.top, min_size_mb=min_mb, lang=lang, excludes=args.exclude, extensions=args.extension)
        return 0

    if args.command == "remove":
        return remove_path(
            args.ruta,
            to_trash=not args.permanent,
            recursive=args.recursive,
            force=args.force,
            lang=lang,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())


