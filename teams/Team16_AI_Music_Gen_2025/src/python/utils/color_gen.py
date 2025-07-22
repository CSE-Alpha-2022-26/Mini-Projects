import colorsys
import random

def generate_distinct_color(existing_colors, saturation=0.7, lightness=0.5):
    """
    Generate a hex color that is visually distinct from existing_colors.

    Args:
        existing_colors (list of str): List of hex colors already in use.
        saturation (float): Saturation for HSL (0–1).
        lightness (float): Lightness for HSL (0–1).

    Returns:
        str: New hex color code.
    """
    def hsl_to_hex(h, s, l):
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))

    used_hues = set()
    for color in existing_colors:
        color = color.lstrip('#')
        if len(color) == 6:
            r, g, b = tuple(int(color[i:i+2], 16)/255.0 for i in (0, 2, 4))
            h, _, _ = colorsys.rgb_to_hls(r, g, b)
            used_hues.add(round(h, 2))

    max_attempts = 100
    for _ in range(max_attempts):
        h = round(random.random(), 2)
        if h not in used_hues:
            return hsl_to_hex(h, saturation, lightness)

    # Fallback: jitter a bit from used hues
    h = (random.random() + 0.5) % 1.0
    return hsl_to_hex(h, saturation, lightness)
