from __future__ import annotations

from collections.abc import Iterable
from pathlib import PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile
from io import BytesIO


def format_bytes(size: int) -> str:
    if size < 0:
        raise ValueError("size must not be negative")

    value = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.0f} {unit}" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1024
    raise AssertionError("unreachable")


def get_file_category(filename: str) -> str:
    suffix = PurePosixPath(filename.replace("\\", "/")).suffix.lower()
    return suffix[1:] if suffix else "No extension"


def _safe_archive_name(filename: str) -> str:
    basename = PurePosixPath(filename.replace("\\", "/")).name
    sanitized = "".join(character for character in basename if character.isprintable())
    return sanitized.strip() or "unnamed-file"


def _unique_name(filename: str, used_names: set[str]) -> str:
    safe_name = _safe_archive_name(filename)
    candidate = safe_name
    counter = 2
    while candidate.casefold() in used_names:
        path = PurePosixPath(safe_name)
        candidate = f"{path.stem} ({counter}){path.suffix}"
        counter += 1
    used_names.add(candidate.casefold())
    return candidate


def build_zip(files: Iterable[tuple[str, bytes]]) -> bytes:
    archive = BytesIO()
    used_names: set[str] = set()

    with ZipFile(archive, mode="w", compression=ZIP_DEFLATED) as zip_file:
        for filename, contents in files:
            archive_name = _unique_name(filename, used_names)
            zip_file.writestr(archive_name, contents)

    return archive.getvalue()
