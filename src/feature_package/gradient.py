import math
from colorsys import rgb_to_hls, hls_to_rgb

from PIL import Image, ImageColor, ImageDraw


def new(mode, size, color1, color2, orientation) -> Image:
    im = Image.new("RGBA", size)
    draw = ImageDraw.Draw(im)

    width, height = size
    if orientation == "Vertical":
        for y in range(height):
            draw.line(
                [(0, y), (width, y)],
                fill=calc_color(mode, y / (height - 1), color1, color2),
            )
    elif orientation == "Horizontal":
        for x in range(width):
            draw.line(
                [(x, 0), (x, height)],
                fill=calc_color(mode, x / (width - 1), color1, color2),
            )

    return im


def calc_color(mode, position, color1, color2) -> tuple:
    if isinstance(color1, str):
        color1, color2 = [ImageColor.getrgb(item) for item in [color1, color2]]

    if mode == "RGB":
        return tuple(
            [int(color1[i] + (color2[i] - color1[i]) * position) for i in range(3)]
        )
    elif mode == "HSL":
        color1, color2 = [
            rgb_to_hls(*[i / 255 for i in item]) for item in [color1, color2]
        ]
        delta = [j - i for i, j in zip(color1, color2)]
        delta[0] -= math.floor(delta[0] + 0.5)
        hls = [i + j * position for i, j in zip(color1, delta)]
        hls[0] -= math.floor(hls[0])
        return tuple([int(i * 255) for i in hls_to_rgb(*hls)])
