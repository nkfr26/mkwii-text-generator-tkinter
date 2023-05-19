import numpy as np
from PIL import Image, ImageChops, ImageEnhance

from . import gradient


class TextImageGenerator:
    def __init__(self, user_interface) -> None:
        self.file_names = user_interface.text.file_names
        self.slider = user_interface.scale.value.get() / 10 + 1
        self.selectbox = user_interface.combobox.value.get()

        orientation_value = user_interface.gradient.orientation.value.get()
        self.orientation = "Vertical" if orientation_value == 0 else "Horizontal"
        mode_value = user_interface.gradient.mode.value.get()
        self.mode = "RGB" if mode_value == 0 else "HSL"

        self.should_invert = int(user_interface.checkbutton.value.get())

        self.color = self.invert_hex(user_interface.single.spframe.button.color)
        self.colors = [
            self.invert_hex(color)
            for color in user_interface.multi.mpframe.button.colors
        ]
        self.top_color = self.invert_hex(user_interface.gradient.tpframe.button.color)
        self.btm_color = self.invert_hex(user_interface.gradient.bpframe.button.color)

    def invert_hex(self, color) -> str:
        if not self.should_invert:
            return color

        r, g, b = [255 - int(color[i:i + 2], 16) for i in range(1, 6, 2)]
        return f"#{r:02x}{g:02x}{b:02x}"

    def create_images(self) -> list:
        images = []
        for file_name in self.file_names:
            if file_name == "\n":
                images.append("LF")  # LF: Line Feed (改行)
                continue

            if self.selectbox == "Yellow":
                images.append(Image.open(f"Fonts/Yellow/{file_name}.png"))
            else:
                images.append(Image.open(f"Fonts/White/{file_name}.png"))

        return images

    def multiply_char(self) -> list:
        images = self.create_images()
        if not self.selectbox == "Multi Color":
            return images

        for i, image1 in enumerate(images):
            if image1 == "LF":
                continue

            image2 = Image.new("RGBA", image1.size, self.colors[i])
            images[i] = ImageChops.multiply(image1, image2)

        return images

    def adjust_x_coordinate(self, x, image_width, file_name) -> int:
        # time 00:00.000, lap " 1"  , "km/h"
        position_mapping = {
            "T": -5, "I": +2, "M": -1, "L": +2, "A": +8, "P": +1,
            "COLON": -1, "PERIOD": -2, "K": +1, "Z": -4, "Q": +4,
            "F": -5, "V": -5, "W": -6, "Y": -8, "C": -5, "G": -2, "LEFT": -2,
        }
        image_width += position_mapping.get(file_name, 0)

        if not file_name in [*map(str, range(10)), "COLON", "PERIOD", "SPACE", "SPACE_", "LEFT", "RIGHT"]:
            image_width -= 16

        x += image_width
        return x

    def concat_images(self) -> Image:
        images = self.multiply_char()
        y, is_LF = 0, False
        concated_image = Image.open("Fonts/Yellow/SPACE.png")  # エラー防止
        for i, image in enumerate(images):  # 画像の結合
            if image == "LF":  # 改行処理
                y += 88
                is_LF = True
                continue

            if i == 0 or is_LF:
                x = 0
                image_width = image.width
                file_name = self.file_names[i]
                if i == 0:  # 1文字目
                    concated_image = image
                elif is_LF:  # 改行直後
                    bg = Image.new(
                        "RGBA", (max(concated_image.width, image_width), y + 84)
                    )
                    bg.paste(concated_image)
                    bg.paste(image, (0, y))
                    concated_image = bg
                    is_LF = False
            else:
                x = self.adjust_x_coordinate(x, image_width, file_name)
                image_width = image.width
                file_name = self.file_names[i]
                bg = Image.new(
                    "RGBA", (max(concated_image.width, x + image_width), y + 84)
                )
                bg.paste(concated_image)
                fg = Image.new("RGBA", bg.size)
                fg.paste(image, (x, y))
                concated_image = Image.alpha_composite(bg, fg)

        return concated_image

    def multiply_str(self) -> Image:
        concated_image = self.concat_images()
        if not self.selectbox in ["Single Color", "Gradient"]:
            return concated_image

        if self.selectbox == "Single Color":
            image2 = Image.new(
                "RGBA", concated_image.size, self.color
            )
        elif self.selectbox == "Gradient":
            image2 = gradient.new(
                self.mode, concated_image.size,
                self.top_color, self.btm_color, self.orientation,
            )

        return ImageChops.multiply(concated_image, image2)

    def invert_image(self) -> Image:
        multiplied_image = self.multiply_str()
        if not self.should_invert:
            return multiplied_image

        im_arr = np.array(multiplied_image)
        im_arr[:, :, :3] = 255 - im_arr[:, :, :3]
        inverted_image = Image.fromarray(im_arr)

        # width, height = multiplied_image.size
        # inverted_image = Image.new("RGBA", (width, height))
        # for x in range(width):
        #     for y in range(height):
        #         r, g, b, a = multiplied_image.getpixel((x, y))
        #         inverted_image.putpixel((x, y), (255 - r, 255 - g, 255 - b, a))

        return inverted_image

    def generate_image(self) -> Image:
        inverted_image = self.invert_image()
        enhancer = ImageEnhance.Brightness(inverted_image)  # 輝度調整
        return enhancer.enhance(self.slider)
