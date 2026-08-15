import math
import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from services.image_processor import load_and_orient_image, apply_fit_mode, add_rounded_corners

logger = logging.getLogger(__name__)

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 1200

def create_collage(
    photo_paths: list[str],
    layout_name: str = "auto",
    bg_color: str = "#FFFFFF",
    spacing: int = 15,
    fit_mode: str = "crop",
    corner_radius: int = 0,
    title: str | None = None,
    output_path: str = "output.jpg"
) -> str:
    """Generates the customizable photo collage and saves it as JPEG."""
    if not photo_paths:
        raise ValueError("No images provided for collage creation.")

    images = [load_and_orient_image(p) for p in photo_paths]
    count = len(images)

    title_height = 80 if title else 0
    total_w = CANVAS_WIDTH
    total_h = CANVAS_HEIGHT + title_height

    canvas = Image.new("RGBA", (total_w, total_h), bg_color)
    draw = ImageDraw.Draw(canvas)

    # Render Title if requested
    if title:
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except OSError:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), title, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((total_w - tw) // 2, (title_height - th) // 2), title, fill="#000000" if bg_color.upper() in ["#FFFFFF", "#D3D3D3"] else "#FFFFFF", font=font)

    content_y_offset = title_height
    usable_h = CANVAS_HEIGHT

    # Calculate sub-box regions based on layout selection
    regions = _get_layout_regions(layout_name, count, total_w, usable_h, spacing, content_y_offset)

    for i, img in enumerate(images):
        if i >= len(regions):
            break
        rx, ry, rw, rh = regions[i]
        processed = apply_fit_mode(img, (rw, rh), fit_mode, bg_color)
        if corner_radius > 0:
            processed = add_rounded_corners(processed, corner_radius)
            canvas.paste(processed, (rx, ry), processed)
        else:
            canvas.paste(processed, (rx, ry))

    # Convert to RGB JPEG format
    final_output = Image.new("RGB", canvas.size, bg_color)
    final_output.paste(canvas, mask=canvas.split()[3])
    final_output.save(output_path, "JPEG", quality=95)
    return output_path

def _get_layout_regions(layout: str, count: int, width: int, height: int, spacing: int, top_offset: int) -> list[tuple[int, int, int, int]]:
    """Determines bounding boxes for each image slot (x, y, w, h)."""
    regions = []

    if layout == "grid_2x2":
        cols, rows = 2, 2
        return _grid_split(cols, rows, width, height, spacing, top_offset)

    elif layout == "grid_3x3":
        cols, rows = 3, 3
        return _grid_split(cols, rows, width, height, spacing, top_offset)

    elif layout == "vertical":
        return _grid_split(1, min(count, 12), width, height, spacing, top_offset)

    elif layout == "horizontal":
        return _grid_split(min(count, 12), 1, width, height, spacing, top_offset)

    elif layout == "1l_2s":
        # 1 Large on Left, 2 Small on Right
        w_left = (width - 3 * spacing) // 2
        w_right = w_left
        h_small = (height - 3 * spacing) // 2
        regions.append((spacing, top_offset + spacing, w_left, height - 2 * spacing))
        regions.append((spacing * 2 + w_left, top_offset + spacing, w_right, h_small))
        regions.append((spacing * 2 + w_left, top_offset + spacing * 2 + h_small, w_right, h_small))
        return regions

    elif layout == "1l_3s":
        # 1 Large on Top, 3 Small on Bottom
        h_top = (height - 3 * spacing) * 2 // 3
        h_bot = (height - 3 * spacing) // 3
        w_small = (width - 4 * spacing) // 3
        regions.append((spacing, top_offset + spacing, width - 2 * spacing, h_top))
        for i in range(3):
            x = spacing + i * (w_small + spacing)
            regions.append((x, top_offset + spacing * 2 + h_top, w_small, h_bot))
        return regions

    elif layout == "2x2_featured":
        # 1 Main Top Center, 4 Grid Bottom
        h_top = (height - 3 * spacing) // 2
        h_bot = h_top
        w_small = (width - 3 * spacing) // 2
        regions.append((spacing, top_offset + spacing, width - 2 * spacing, h_top))
        regions.append((spacing, top_offset + spacing * 2 + h_top, w_small, (h_bot - spacing) // 2))
        regions.append((spacing * 2 + w_small, top_offset + spacing * 2 + h_top, w_small, (h_bot - spacing) // 2))
        return regions

    # Auto Layout algorithm fallback
    cols = math.ceil(math.sqrt(count))
    rows = math.ceil(count / cols)
    return _grid_split(cols, rows, width, height, spacing, top_offset)

def _grid_split(cols: int, rows: int, width: int, height: int, spacing: int, top_offset: int) -> list[tuple[int, int, int, int]]:
    regions = []
    w = (width - (cols + 1) * spacing) // cols
    h = (height - (rows + 1) * spacing) // rows
    for r in range(rows):
        for c in range(cols):
            x = spacing + c * (w + spacing)
            y = top_offset + spacing + r * (h + spacing)
            regions.append((x, y, w, h))
    return regions
