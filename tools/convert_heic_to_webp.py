from pillow_heif import register_heif_opener
from PIL import Image
import sys
from pathlib import Path

register_heif_opener()

def convert(input_path, output_path=None, quality=90):
    p = Path(input_path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if output_path is None:
        output_path = p.with_suffix('.webp')
    im = Image.open(p)
    im.save(output_path, format='WEBP', quality=quality)
    return output_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: convert_heic_to_webp.py <input.heic> [output.webp] [quality]')
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) >= 3 else None
    quality = int(sys.argv[3]) if len(sys.argv) >= 4 else 90
    out = convert(input_path, output_path, quality)
    print(f'Converted to {out}')
