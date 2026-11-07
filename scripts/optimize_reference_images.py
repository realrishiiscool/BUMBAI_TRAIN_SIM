# Keep editable PNG sources in _source_images/; Jekyll excludes that folder from the published site.
# Install Pillow once with: python -m pip install Pillow
# Then regenerate published WebP assets with: python scripts/optimize_reference_images.py
from pathlib import Path
from PIL import Image

SOURCE_DIR = Path(__file__).resolve().parents[1] / "_source_images"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "image"
MAX_DIMENSION = 2200
QUALITY = 96


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for source in sorted(SOURCE_DIR.glob("*.png")):
        with Image.open(source) as original:
            image = original.convert("RGBA") if "A" in original.getbands() else original.convert("RGB")
            image.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.Resampling.LANCZOS)
            output = OUTPUT_DIR / f"{source.stem}.webp"
            image.save(output, "WEBP", quality=QUALITY, method=4)
            print(f"{source.name} -> image/{output.name} ({output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
