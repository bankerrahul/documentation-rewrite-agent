"""
Annotation module for screenshot images.
Draws red arrows and green highlight boxes on PIL images.

Arrow style: bright red, thick shaft, large triangular arrowhead.
Matches the exact reference arrow provided by the user.
"""

import math
from typing import Tuple, Optional, Dict
from PIL import Image, ImageDraw


# Arrow styling constants (in CSS pixels — will be multiplied by scale_factor)
# These values are tuned to match the user's reference arrow exactly:
# - Bright saturated red (237, 28, 36)
# - Thick shaft (~9px CSS)
# - Large prominent arrowhead (~35px side length, 30° spread)
# - Long shaft (~150px CSS)
ARROW_COLOR = (237, 28, 36)   # Bright saturated red — matches reference
ARROW_WIDTH_CSS = 9            # Shaft thickness (thick and bold)
ARROW_LENGTH_CSS = 150         # Shaft length (ideal)
MIN_ARROW_LENGTH_CSS = 60      # Minimum arrow length to keep it visible
ARROW_GAP_CSS = 14             # Gap between tip and element edge
ARROWHEAD_LENGTH_CSS = 35      # Length of arrowhead triangle sides (large/prominent)
ARROWHEAD_ANGLE = math.pi / 6  # 30 degrees — matching reference arrowhead spread

# Layout constants for Thrive Apprentice UI
TA_SIDEBAR_WIDTH_CSS = 100    # TA icon sidebar is ~100px wide
WP_SIDEBAR_WIDTH_CSS = 160    # WP admin sidebar is ~160px wide
WP_TOOLBAR_HEIGHT_CSS = 32    # WP admin top toolbar is ~32px


def draw_arrow(
    image: Image.Image,
    start: Tuple[float, float],
    end: Tuple[float, float],
    color: Tuple[int, int, int] = ARROW_COLOR,
    width: int = 10,
    head_length: int = 36,
    head_angle: float = ARROWHEAD_ANGLE,
) -> None:
    """Draw an arrow with a filled triangular arrowhead on the image.

    Args:
        image: PIL Image to draw on.
        start: (x, y) tail of the arrow.
        end: (x, y) tip of the arrow (where arrowhead points).
        color: RGB tuple.
        width: Shaft thickness in pixels.
        head_length: Side length of arrowhead triangle in pixels.
        head_angle: Half-angle of arrowhead spread.
    """
    draw = ImageDraw.Draw(image)

    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)

    if length < 5:
        return  # Arrow too short to draw

    angle = math.atan2(dy, dx)

    # Shorten the line so it doesn't poke through the arrowhead
    base_offset = head_length * math.cos(head_angle)
    shaft_end_x = end[0] - base_offset * math.cos(angle)
    shaft_end_y = end[1] - base_offset * math.sin(angle)

    # Draw the shaft line
    draw.line(
        [(int(start[0]), int(start[1])), (int(shaft_end_x), int(shaft_end_y))],
        fill=color,
        width=width,
    )

    # Arrowhead triangle points
    tip = (int(end[0]), int(end[1]))
    left_x = end[0] - head_length * math.cos(angle - head_angle)
    left_y = end[1] - head_length * math.sin(angle - head_angle)
    right_x = end[0] - head_length * math.cos(angle + head_angle)
    right_y = end[1] - head_length * math.sin(angle + head_angle)

    draw.polygon(
        [tip, (int(left_x), int(left_y)), (int(right_x), int(right_y))],
        fill=color,
    )


def draw_highlight_box(
    image: Image.Image,
    bbox: Tuple[float, float, float, float],
    color: str = "#2ECC40",
    width: int = 3,
) -> None:
    """Draw a rectangle outline around a bounding box region.

    Args:
        bbox: (x, y, w, h) in image pixel coordinates.
    """
    draw = ImageDraw.Draw(image)
    x, y, w, h = bbox
    draw.rectangle([x, y, x + w, y + h], outline=color, width=width)


def auto_arrow_position(
    element_cx: float,
    element_cy: float,
    element_left: float,
    element_right: float,
    element_top: float,
    element_bottom: float,
    viewport_width: float,
    viewport_height: float,
) -> str:
    """Choose optimal arrow position based on element location in viewport.

    Smart rules:
    1. Elements in the WP/TA sidebar (left < 200px) → arrow from RIGHT
       (sidebars have no open space to the left)
    2. Elements near the right edge → arrow from LEFT
    3. For centered elements → pick side with most open space
    4. Prefer horizontal arrows (matching Thrive doc style)
    5. Fall back to vertical only if no horizontal space

    Returns one of: 'left', 'right', 'top', 'bottom'.
    """
    # Space available on each side (in CSS pixels)
    space_left = element_left
    space_right = viewport_width - element_right
    space_top = element_top
    space_bottom = viewport_height - element_bottom

    # Minimum space needed for a visible arrow
    ideal_space = 140   # For a full-length arrow
    min_space = 70      # Absolute minimum for a short arrow

    # --- Rule 1: Sidebar elements always get arrows from the right ---
    # Thrive Apprentice sidebar is on the left (~100px), WP admin sidebar ~160px
    # Elements whose right edge is < 200px are "in the sidebar zone"
    if element_right < 200 and space_right >= min_space:
        return "right"

    # --- Rule 2: Elements near the top toolbar get arrows from below ---
    if element_bottom < 50 and space_bottom >= min_space:
        return "bottom"

    # --- Rule 3: Pick horizontal direction with most space ---
    # Prefer horizontal (matching Thrive documentation style)
    if space_left >= ideal_space and space_left >= space_right:
        return "left"
    if space_right >= ideal_space:
        return "right"
    if space_left >= ideal_space:
        return "left"

    # --- Rule 4: If neither side has ideal space, pick whichever has more ---
    if space_left >= min_space and space_left >= space_right:
        return "left"
    if space_right >= min_space:
        return "right"
    if space_left >= min_space:
        return "left"

    # --- Rule 5: Fall back to vertical if not enough horizontal space ---
    if space_top >= ideal_space and space_top >= space_bottom:
        return "top"
    if space_bottom >= ideal_space:
        return "bottom"
    if space_top >= min_space and space_top >= space_bottom:
        return "top"
    if space_bottom >= min_space:
        return "bottom"

    # Last resort: whichever side has most space
    sides = {
        "left": space_left,
        "right": space_right,
        "top": space_top,
        "bottom": space_bottom,
    }
    return max(sides, key=sides.get)


def _compute_arrow_points(
    position: str,
    left_edge: float, right_edge: float,
    top_edge: float, bottom_edge: float,
    cx: float, cy: float,
    arrow_len: float, gap: float,
    img_w: float, img_h: float,
    element_height: float,
) -> Tuple[float, float, float, float]:
    """Compute arrow tail (start) and tip (end) in image coordinates.

    Handles edge cases:
    - Clamps tail to image bounds
    - Uses diagonal offset when space is extremely tight
    - Ensures minimum arrow length for visibility

    Returns: (tail_x, tail_y, tip_x, tip_y)
    """
    margin = 30  # Minimum distance from image edge

    if position == "left":
        tip_x = left_edge - gap
        tip_y = cy
        tail_x = tip_x - arrow_len
        tail_y = cy
    elif position == "right":
        tip_x = right_edge + gap
        tip_y = cy
        tail_x = tip_x + arrow_len
        tail_y = cy
    elif position == "top":
        tip_x = cx
        tip_y = top_edge - gap
        tail_x = cx
        tail_y = tip_y - arrow_len
    elif position == "bottom":
        tip_x = cx
        tip_y = bottom_edge + gap
        tail_x = cx
        tail_y = tip_y + arrow_len
    else:
        # Fallback: right (most common useful direction)
        tip_x = right_edge + gap
        tip_y = cy
        tail_x = tip_x + arrow_len
        tail_y = cy

    # Clamp tail within image bounds (keep margin from edge)
    tail_x = max(margin, min(img_w - margin, tail_x))
    tail_y = max(margin, min(img_h - margin, tail_y))

    # Clamp tip within image bounds
    tip_x = max(margin, min(img_w - margin, tip_x))
    tip_y = max(margin, min(img_h - margin, tip_y))

    # Check if arrow is too short after clamping — add diagonal offset
    actual_len = math.hypot(tail_x - tip_x, tail_y - tip_y)
    min_len = MIN_ARROW_LENGTH_CSS * 2  # In image coords (scale_factor=2 typical)

    if actual_len < min_len:
        # Add a diagonal component to gain length
        diag_offset = (min_len - actual_len) * 0.8
        if position in ("left", "right"):
            # Shift tail vertically (upward if element is in bottom half)
            if cy > img_h / 2:
                tail_y = max(margin, tail_y - diag_offset)
            else:
                tail_y = min(img_h - margin, tail_y + diag_offset)
        else:
            # Shift tail horizontally
            if cx > img_w / 2:
                tail_x = max(margin, tail_x - diag_offset)
            else:
                tail_x = min(img_w - margin, tail_x + diag_offset)

    return tail_x, tail_y, tip_x, tip_y


def annotate_screenshot(
    image: Image.Image,
    element_box: Dict[str, float],
    scroll_offset: Tuple[float, float] = (0, 0),
    scale_factor: int = 2,
    position: Optional[str] = None,
    arrow_color: Tuple[int, int, int] = ARROW_COLOR,
    arrow_length_css: int = ARROW_LENGTH_CSS,
    gap_css: int = ARROW_GAP_CSS,
    arrow_width_css: int = ARROW_WIDTH_CSS,
    arrowhead_length_css: int = ARROWHEAD_LENGTH_CSS,
    highlight: bool = False,
    highlight_color: str = "#2ECC40",
) -> Image.Image:
    """Annotate a screenshot with an arrow pointing at the target element.

    Coordinate flow:
        Playwright bounding_box() returns CSS pixels relative to viewport.
        The screenshot image is (viewport_w * scale_factor) pixels wide.
        So: image_x = (css_x - scroll_x) * scale_factor

    Args:
        image: PIL Image of the screenshot (at scale_factor resolution).
        element_box: Dict with 'x', 'y', 'width', 'height' in CSS pixels
                     (as returned by Playwright's bounding_box()).
        scroll_offset: (scroll_x, scroll_y) in CSS pixels.
        scale_factor: DPI scale (2 for Retina).
        position: Arrow direction ('left', 'right', 'top', 'bottom') or None for auto.
        arrow_color: RGB color tuple for the arrow.
        arrow_length_css: Length of arrow shaft in CSS pixels.
        gap_css: Gap between arrow tip and element edge in CSS pixels.
        arrow_width_css: Width of arrow shaft in CSS pixels.
        arrowhead_length_css: Side length of arrowhead triangle in CSS pixels.
        highlight: If True, also draw a highlight box around the element.
        highlight_color: Color of the highlight box.

    Returns:
        Annotated PIL Image (same object, mutated).
    """
    sf = scale_factor
    ox, oy = scroll_offset

    # Element bounds in CSS pixels (relative to viewport)
    el_left_css = element_box["x"] - ox
    el_top_css = element_box["y"] - oy
    el_right_css = el_left_css + element_box["width"]
    el_bottom_css = el_top_css + element_box["height"]
    el_cx_css = el_left_css + element_box["width"] / 2
    el_cy_css = el_top_css + element_box["height"] / 2

    # Viewport dimensions in CSS pixels
    img_w, img_h = image.size
    vw_css = img_w / sf
    vh_css = img_h / sf

    # Sanity check: skip if element is way off-screen
    if (el_bottom_css < -50 or el_top_css > vh_css + 50 or
            el_right_css < -50 or el_left_css > vw_css + 50):
        return image

    # Auto-select position if not specified
    if position is None:
        position = auto_arrow_position(
            el_cx_css, el_cy_css,
            el_left_css, el_right_css,
            el_top_css, el_bottom_css,
            vw_css, vh_css,
        )

    # Element edges in image coordinates
    left_edge = el_left_css * sf
    right_edge = el_right_css * sf
    top_edge = el_top_css * sf
    bottom_edge = el_bottom_css * sf
    cx = el_cx_css * sf
    cy = el_cy_css * sf

    # Arrow dimensions in image coordinates
    arrow_len = arrow_length_css * sf
    gap = gap_css * sf
    width = arrow_width_css * sf
    head_len = arrowhead_length_css * sf

    # Adaptive gap: for very small elements, reduce the gap so arrow stays close
    element_size = min(element_box["width"], element_box["height"])
    if element_size < 30:
        gap = min(gap, 8 * sf)

    # Compute arrow endpoints with smart edge handling
    tail_x, tail_y, tip_x, tip_y = _compute_arrow_points(
        position, left_edge, right_edge, top_edge, bottom_edge,
        cx, cy, arrow_len, gap, img_w, img_h,
        element_box["height"] * sf,
    )

    # Draw the arrow
    draw_arrow(
        image,
        start=(tail_x, tail_y),
        end=(tip_x, tip_y),
        color=arrow_color,
        width=int(width),
        head_length=int(head_len),
    )

    # Optionally draw highlight box
    if highlight:
        box_in_img = (left_edge, top_edge, element_box["width"] * sf, element_box["height"] * sf)
        draw_highlight_box(image, box_in_img, color=highlight_color, width=int(3 * sf))

    return image
