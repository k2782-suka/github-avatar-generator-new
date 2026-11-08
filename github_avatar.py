#!/usr/bin/env python3
"""
github_avatar.py — генерирует 10 случайных аватаров (identicon) в SVG и PNG.
Не требует сторонних библиотек. Запуск: python github_avatar.py
"""

import colorsys
import hashlib
import math
import secrets
import struct
import zlib
from pathlib import Path

# ---- Настройки -------------------------------------------------------------
COUNT = 10             # сколько аватаров создать
SIZE = 420             # размер в пикселях
CELLS = 5              # размер сетки (нечётное число, не меньше 3)
OUT_DIR = Path("avatars")
BACKGROUND = (0xF6, 0xF8, 0xFA)
# ----------------------------------------------------------------------------


def make_hash(seed: str) -> bytes:
    """Хэш строки (SHA-256)."""
    return hashlib.sha256(seed.encode("utf-8")).digest()


def make_color(h: bytes) -> tuple[int, int, int]:
    """Цвет в HSL: оттенок из первого байта, яркость и насыщенность в комфортном диапазоне."""
    hue = h[0] / 255.0
    lightness = 0.40 + (h[1] / 255.0) * 0.20   # 0.40–0.60
    saturation = 0.55 + (h[2] / 255.0) * 0.30  # 0.55–0.85
    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    return round(r * 255), round(g * 255), round(b * 255)


def make_grid(h: bytes, cells: int) -> list[list[bool]]:
    """Сетка, симметричная по вертикали: левая половина из хэша, правая — зеркало."""
    half = (cells + 1) // 2
    bits = [(byte >> i) & 1 for byte in h[3:] for i in range(8)]
    grid = [[False] * cells for _ in range(cells)]
    idx = 0
    for y in range(cells):
        for x in range(half):
            filled = bool(bits[idx % len(bits)])
            idx += 1
            grid[y][x] = filled
            grid[y][cells - 1 - x] = filled
    return grid


def build_svg(grid, color, size: int, cells: int) -> str:
    """SVG-разметка аватара."""
    hex_color = "#{:02x}{:02x}{:02x}".format(*color)
    bg = "#{:02x}{:02x}{:02x}".format(*BACKGROUND)
    cell = size / (cells + 2)  # отступ в одну клетку с каждой стороны

    rects = []
    for y, row in enumerate(grid):
        for x, filled in enumerate(row):
            if filled:
                rx = cell + x * cell
                ry = cell + y * cell
                rects.append(
                    f'  <rect x="{rx:.2f}" y="{ry:.2f}" '
                    f'width="{cell:.2f}" height="{cell:.2f}" fill="{hex_color}"/>'
                )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 {size} {size}">\n'
        f'  <rect width="{size}" height="{size}" fill="{bg}"/>\n'
        + "\n".join(rects)
        + "\n</svg>\n"
    )


def _png_chunk(tag: bytes, data: bytes) -> bytes:
    """Один блок PNG: длина, тип, данные, CRC."""
    crc = zlib.crc32(tag + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)


def build_png(grid, color, size: int, cells: int) -> bytes:
    """Рисует аватар напрямую в пиксели и упаковывает в PNG (RGB, 8 бит)."""
    cell = size / (cells + 2)
    raw = bytearray()
    for y in range(size):
        raw.append(0)  # фильтр «None» для строки
        gy = math.floor(y / cell) - 1
        for x in range(size):
            gx = math.floor(x / cell) - 1
            if 0 <= gx < cells and 0 <= gy < cells and grid[gy][gx]:
                raw.extend(color)
            else:
                raw.extend(BACKGROUND)

    ihdr = struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)  # 8 бит, RGB
    return (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", ihdr)
        + _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + _png_chunk(b"IEND", b"")
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for i in range(1, COUNT + 1):
        seed = secrets.token_hex(8)  # случайная строка -> случайный аватар
        h = make_hash(seed)
        color = make_color(h)
        grid = make_grid(h, CELLS)

        name = f"avatar_{i:02d}_{seed[:8]}"
        svg_path = OUT_DIR / f"{name}.svg"
        png_path = OUT_DIR / f"{name}.png"

        svg_path.write_text(build_svg(grid, color, SIZE, CELLS), encoding="utf-8")
        png_path.write_bytes(build_png(grid, color, SIZE, CELLS))

        print(f"[{i}/{COUNT}] {png_path}")

    print(f"\nГотово: {COUNT} аватаров (SVG и PNG), папка: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
