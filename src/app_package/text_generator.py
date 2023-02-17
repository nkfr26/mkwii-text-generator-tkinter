from PIL import Image, ImageChops, ImageEnhance


class TextGenerator:
    def __init__(self, user_interface) -> None:
        self.file_names = user_interface.file_names
        self.slider = user_interface.var_scale.get() / 10 + 1
        self.selectbox = user_interface.var_combobox.get()

        value = user_interface.gradient_widget.var_radio.get()
        self.radio = "Vertical" if value == 0 else "Horizontal"

        self.color = user_interface.color_widget.label_button.button.color
        self.colors = user_interface.colorful_widget.label_button.button.colors
        self.top_color = (
            user_interface.gradient_widget.left_label_button.button.top_color
        )
        self.btm_color = (
            user_interface.gradient_widget.right_label_button.button.btm_color
        )

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

    # https://stackoverflow.com/questions/32530345/pil-generating-vertical-gradient-image/
    def gradient(self, size: tuple[int, int], top_color, btm_color) -> Image:
        base = Image.new("RGBA", size, top_color)
        top = Image.new("RGBA", size, btm_color)
        mask = Image.new("L", size)
        mask_data, width, height = [], *size  # アンパック
        for y in range(height):
            mask_data.extend([int(255 * (y / height))] * width)
        mask.putdata(mask_data)
        base.paste(top, mask=mask)
        return base

    def multiply_char(self) -> list:
        images = self.create_images()
        # 「Colorful」と「Gradient(Vertical)」以外は早期リターン
        if not (
            self.selectbox in ["Colorful", "Gradient"] and self.radio == "Vertical"
        ):
            return images

        for i, image1 in enumerate(images):
            if image1 == "LF":
                continue

            if self.selectbox == "Colorful":
                image2 = Image.new("RGBA", image1.size, self.colors[i])
            elif self.selectbox == "Gradient":
                image2 = self.gradient(image1.size, self.top_color, self.btm_color)
            images[i] = ImageChops.multiply(image1, image2)

        return images

    def adjust_x_coordinate(self, x, image_width, file_name) -> int:
        # 50: 0～9 & SLASH, 42: - & +
        if image_width in [50, 42] or file_name in ["PERIOD", "CORON"]:
            image_width -= 4
        else:
            image_width -= 12

        if file_name in ["T", "7_"]:
            image_width -= 6
        elif file_name in ["I", "M", "CORON"]:
            image_width -= 2
        elif file_name in ["L", "Q"]:
            image_width += 2

        x += image_width
        return x

    def concat_image(self) -> Image:
        images = self.multiply_char()
        y, is_LF = 0, False
        concated_image = Image.open("Fonts/Yellow/SPACE.png")  # エラー防止
        for i, image in enumerate(images):  # 画像の結合
            if image == "LF":  # 改行処理
                y += 64
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
                        "RGBA", (max(concated_image.width, image_width), y + 64)
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
                    "RGBA", (max(concated_image.width, x + image_width), y + 64)
                )
                bg.paste(concated_image)
                fg = Image.new("RGBA", bg.size)
                fg.paste(image, (x, y))
                concated_image = Image.alpha_composite(bg, fg)

        return concated_image

    def multiply_str(self) -> Image:
        concated_image = self.concat_image()
        # 「Color」と「Gradient(Horizontal)」以外は早期リターン
        if not (self.selectbox == "Color" or self.radio == "Horizontal"):
            return concated_image

        if self.selectbox == "Color":
            image2 = Image.new("RGBA", concated_image.size, self.color)
        elif self.radio == "Horizontal":
            image2 = self.gradient(
                (concated_image.height, concated_image.width),
                self.top_color, self.btm_color,
            )
            image2 = image2.transpose(Image.Transpose.ROTATE_90)
        return ImageChops.multiply(concated_image, image2)

    def generate_image(self) -> Image:
        color_image = self.multiply_str()
        enhancer = ImageEnhance.Brightness(color_image)  # 輝度調整
        return enhancer.enhance(self.slider)
