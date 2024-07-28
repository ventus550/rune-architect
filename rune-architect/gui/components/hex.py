def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)

def adjust_brightness(hex_color, brightness_factor=1.0):
    if brightness_factor < 0:
        raise ValueError("Brightness factor must be non-negative")

    rgb = hex_to_rgb(hex_color)
    adjusted_rgb = tuple(min(max(int(c * brightness_factor), 0), 255) for c in rgb)
    return rgb_to_hex(adjusted_rgb)