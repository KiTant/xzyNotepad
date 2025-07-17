import math


def rgb_to_hsv(r: int, g: int, b: int):
    r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
    max_rgb = max(r_norm, g_norm, b_norm)
    min_rgb = min(r_norm, g_norm, b_norm)
    difference = max_rgb - min_rgb
    h = 0
    if difference == 0:
        h = 0
    elif max_rgb == r_norm:
        h = (60 * ((g_norm - b_norm) / difference) + 360) % 360
    elif max_rgb == g_norm:
        h = (60 * ((b_norm - r_norm) / difference) + 120) % 360
    else:  # max_rgb == b_norm
        h = (60 * ((r_norm - g_norm) / difference) + 240) % 360
    s = 0 if max_rgb == 0 else (difference / max_rgb) * 100
    v = max_rgb * 100
    return round(h), round(s), round(v)


def hsv_to_rgb(h: int, s: int, v: int):
    s_norm, v_norm = s / 100.0, v / 100.0

    c = v_norm * s_norm
    x = c * (1 - abs(math.fmod(h / 60.0, 2) - 1))
    m = v_norm - c

    r_prime, g_prime, b_prime = 0, 0, 0

    if 0 <= h < 60:
        r_prime, g_prime, b_prime = c, x, 0
    elif 60 <= h < 120:
        r_prime, g_prime, b_prime = x, c, 0
    elif 120 <= h < 180:
        r_prime, g_prime, b_prime = 0, c, x
    elif 180 <= h < 240:
        r_prime, g_prime, b_prime = 0, x, c
    elif 240 <= h < 300:
        r_prime, g_prime, b_prime = x, 0, c
    elif 300 <= h < 360:
        r_prime, g_prime, b_prime = c, 0, x
    r = round((r_prime + m) * 255)
    g = round((g_prime + m) * 255)
    b = round((b_prime + m) * 255)

    return max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))


def rgb_to_hsl(r: int, g: int, b: int):
    r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
    max_rgb = max(r_norm, g_norm, b_norm)
    min_rgb = min(r_norm, g_norm, b_norm)
    difference = max_rgb - min_rgb
    h = 0
    l = (max_rgb + min_rgb) / 2
    if difference == 0:
        h = 0
        s = 0
    else:
        s = difference / (1 - abs(2 * l - 1)) * 100
        if max_rgb == r_norm:
            h = (60 * ((g_norm - b_norm) / difference) + 360) % 360
        elif max_rgb == g_norm:
            h = (60 * ((b_norm - r_norm) / difference) + 120) % 360
        else:  # max_rgb == b_norm
            h = (60 * ((r_norm - g_norm) / difference) + 240) % 360
    return round(h), round(s), round(l * 100)


def hsl_to_rgb(h: int, s: int, l: int):
    s_norm, l_norm = s / 100.0, l / 100.0
    c = (1 - abs(2 * l_norm - 1)) * s_norm
    x = c * (1 - abs(math.fmod(h / 60.0, 2) - 1))
    m = l_norm - c / 2
    r_prime, g_prime, b_prime = 0, 0, 0
    if 0 <= h < 60:
        r_prime, g_prime, b_prime = c, x, 0
    elif 60 <= h < 120:
        r_prime, g_prime, b_prime = x, c, 0
    elif 120 <= h < 180:
        r_prime, g_prime, b_prime = 0, c, x
    elif 180 <= h < 240:
        r_prime, g_prime, b_prime = 0, x, c
    elif 240 <= h < 300:
        r_prime, g_prime, b_prime = x, 0, c
    elif 300 <= h < 360:
        r_prime, g_prime, b_prime = c, 0, x
    r = round((r_prime + m) * 255)
    g = round((g_prime + m) * 255)
    b = round((b_prime + m) * 255)
    return max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))

__all__ = ["rgb_to_hsv", "hsv_to_rgb", "rgb_to_hsl", "hsl_to_rgb"]
