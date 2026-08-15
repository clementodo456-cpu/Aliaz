import logging
from PIL import Image, ImageOps, ImageDraw

logger = logging.getLogger(__name__)

MAX_SINGLE_DIMENSION = 2048  # Prevent OOM crashes on high-res input photos

def load_and_orient_image(file_path: str) -> Image.Image:
    """Loads image, fixes EXIF orientation, converts to RGB, downscales if huge."""
    img = Image.open(file_path)
    img = ImageOps.exif_transpose(img)
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    # Restrict memory footprint
    if max(img.size) > MAX_SINGLE_DIMENSION:
        img.thumbnail((MAX_SINGLE_DIMENSION, MAX_SINGLE_DIMENSION), Image.Resampling.LANCZOS)
    return img

def apply_fit_mode(img: Image.Image, target_size: tuple[int, int], fit_mode: str, bg_color: str) -> Image.Image:
    """Resizes/crops image to fit target bounds based on crop/fit/stretch."""
    tw, th = target_size
    iw, ih = img.size

    if fit_mode == "stretch":
        return img.resize((tw, th), Image.Resampling.LANCZOS)

    if fit_mode == "fit":
        canvas = Image.new("RGB", (tw, th), bg_color)
        scale = min(tw / iw, th / ih)
        nw, nh = int(iw * scale), int(ih * scale)
        resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
        offset = ((tw - nw) // 2, (th - nh) // 2)
        canvas.paste(resized, offset)
        return canvas

    # Default: "crop" (Center Fill & Crop)
    scale = max(tw / iw, th / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return resized.crop((left, top, left + tw, top + th))

def add_rounded_corners(img: Image.Image, radius: int) -> Image.Image:
    """Adds smooth rounded corners to an image if radius > 0."""
    if radius <= 0:
        return img

    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)

    result = img.convert("RGBA")
    result.putalpha(mask)
    return result
