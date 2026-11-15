"""
Image Optimizer & Comic Visual Enhancement Engine
- Applies cinematic contrast & saturation grading to comic art
- Fits aspect ratio to Instagram guidelines (4:5 to 1.91:1) with blurred background padding
- Saves high-res JPEG optimized for social feeds
"""

from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter


def optimize_comic_image(
    input_path: str | Path,
    output_path: str | Path | None = None,
    for_instagram: bool = True
) -> Path:
    """
    Optimizes a comic panel image for maximum visual punch on social feeds.
    If for_instagram is True, ensures aspect ratio is within Instagram limits (4:5 to 1.91:1)
    by adding clean, blurred-margin padding if the image is too tall.
    """
    in_p = Path(input_path)
    if not in_p.exists():
        raise FileNotFoundError(f"Image not found: {input_path}")

    out_p = Path(output_path) if output_path else in_p.parent / f"{in_p.stem}_opt.jpg"
    out_p.parent.mkdir(parents=True, exist_ok=True)

    im = Image.open(in_p).convert("RGB")
    w, h = im.size

    # 1. Subtle comic visual grading: punch up contrast and colors slightly
    im = ImageEnhance.Contrast(im).enhance(1.10)
    im = ImageEnhance.Color(im).enhance(1.12)
    im = ImageEnhance.Sharpness(im).enhance(1.08)

    # 2. Instagram aspect ratio constraint: min aspect = 4/5 (0.80), max aspect = 1.91
    if for_instagram:
        aspect = w / h
        # If taller than 4:5 (e.g. aspect < 0.8), pad to 4:5 with blurred background
        if aspect < 0.80:
            target_h = h
            target_w = int(h * 0.80)
            
            # Create blurred background
            bg_scale = max(target_w / w, target_h / h)
            nw, nh = int(w * bg_scale), int(h * bg_scale)
            bg = im.resize((nw, nh), Image.Resampling.LANCZOS)
            left = (nw - target_w) // 2
            top = (nh - target_h) // 2
            bg = bg.crop((left, top, left + target_w, top + target_h))
            bg = bg.filter(ImageFilter.GaussianBlur(30))
            bg = ImageEnhance.Brightness(bg).enhance(0.45)

            # Paste original image centered
            pos_x = (target_w - w) // 2
            bg.paste(im, (pos_x, 0))
            im = bg
        elif aspect > 1.91:
            # If wider than 1.91:1, pad vertically to 1.91:1
            target_w = w
            target_h = int(w / 1.91)
            bg = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
            bg = bg.filter(ImageFilter.GaussianBlur(30))
            bg = ImageEnhance.Brightness(bg).enhance(0.45)
            pos_y = (target_h - h) // 2
            bg.paste(im, (0, pos_y))
            im = bg

    # 3. Ensure maximum width of 2048px (Meta maximum photo resolution)
    if im.width > 2048:
        scale = 2048 / im.width
        im = im.resize((2048, int(im.height * scale)), Image.Resampling.LANCZOS)

    im.save(out_p, "JPEG", quality=95, optimize=True)
    return out_p
