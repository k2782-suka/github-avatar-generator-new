# GitHub Avatar Generator

This script creates unique avatars (identicons) in the form of symmetrical, colored patterns.
Each time it is run, it generates **10 random avatars**—no configuration or user input required.

## Use Cases

- **Avatars for projects or bots** when you don’t have a logo or don’t want to design one manually.
- **Placeholders for user interfaces**: a better alternative to a generic gray silhouette for users without a profile picture.
- **Demo data**: quickly generate a variety of images for mockups, testing, or presentations.
- **String-based avatars**: the `build_png(grid, color, ...)` function can be called using a username or email address, ensuring that the same input always produces the same avatar.

## Features

- Generates exactly 10 random avatars per run.
- Features a 5×5 symmetrical pattern, similar to GitHub’s standard identicons.
- Supports two formats: **PNG** (ready for upload to GitHub) and **SVG** (vector-based, scalable without loss of quality).
- No command-line arguments or interactive menus.
- **No external dependencies**: uses only standard Python modules.

## Requirements

- Python 3.8 or newer.

No additional packages need to be installed. ## Getting Started

```bash
git clone https://github.com/your-name/github-avatar-generator.git
cd github-avatar-generator
python github_avatar.py
```

Once run, files like the following will appear in the `avatars/` directory:

```
avatars/avatar_01_3f9a2c1b.png
avatars/avatar_01_3f9a2c1b.svg
...
avatars/avatar_10_c04d8e77.png
avatars/avatar_10_c04d8e77.svg
```

## Configuration

All parameters can be found at the beginning of the `github_avatar.py` file:

| Constant | Default | Description |
|---|---|---|
| `COUNT` | `10` | Number of avatars to generate |
| `SIZE` | `420` | Image size in pixels |
| `CELLS` | `5` | Grid size (must be an odd number, 3 or greater) |
| `OUT_DIR` | `avatars` | Directory for saving output files |
| `BACKGROUND` | `(0xF6, 0xF8, 0xFA)` | Background color in RGB format |

## How to set your avatar on GitHub

1. Run the script and open the `avatars/` directory.
2. Choose a `.png` file that you like.
3. Go to GitHub → **Settings** → **Public profile**.
4. Click on your current profile photo and upload the PNG file.

> GitHub does not support SVG files for profile avatars, so please use the PNG version.

## How it works

1. A random string of 16 hexadecimal characters is generated.
2. This string is converted into an SHA-256 hash.
3. The first three bytes of the hash are used to determine the color in the HSL color model. 4. The following bytes determine which cells in the left half of the grid are filled.
5. The right half is a mirror image of the left, so the pattern is symmetrical.
6. The grid is rendered into pixels, which are then packed into a PNG file using `zlib`. An SVG is also created from the same data.
The project was written using Claude.
