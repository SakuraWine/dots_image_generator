import cv2
import cv2.typing
import numpy as np


class DotsImageGenerator(object):
    def __init__(self) -> None:
        pass

    def generate(self, source_path: str, output_directory: str, output_filename: str, level: int) -> None:
        # read
        image = cv2.imread(source_path, cv2.IMREAD_COLOR)
        # resize
        image_resized = cv2.resize(image, None, None, 1.0, 0.5)
        # to grayscale
        image_gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
        self.to_dots(image=image_gray, level=level, output_path=output_directory+output_filename)

    def to_dots(self, image: cv2.typing.MatLike, level: int, output_path: str) -> np.ndarray:
        source = self.resize_image(image=image, level=level)
        cv2.imwrite(output_path, source)
        for column in source:
            row_str = []
            for row in column:
                # row_str.append(self.get_dot(row))
                print(self.get_dot(row), end="")
            print()

    def get_dot(self, brightness: int) -> str:
        if brightness < 10:
            return "⣿"
        elif brightness < 64:
            return "⠿"
        elif brightness < 128:
            return "⠇"
        elif brightness < 224:
            return "⠂"
        else:
            return " "

    def resize_image(self, image: cv2.typing.MatLike, level: int) -> cv2.typing.MatLike:
        image_rescaled = cv2.resize(image, None, None, 1.0, 0.5)
        if level == 4:
            image_resized = cv2.resize(image_rescaled, None, None, 0.25, 0.25)
        elif level == 3:
            image_resized = cv2.resize(image_rescaled, None, None, 0.5, 0.5)
        elif level == 2:
            image_resized = cv2.resize(image_rescaled, None, None, 0.75, 0.75)
        elif level == 1:
            image_resized = image_rescaled
        else:
            print("Invalid level.")
            image_resized = image_rescaled
        return image_resized


# 読み込み → リサイズ → グレスケ → 点群画像生成 → 書き出し

generator = DotsImageGenerator()
generator.generate("/home/sakura/workspace/image_to_dots_image_converter/data/sample_miyako.png",
                  "/home/sakura/workspace/image_to_dots_image_converter/output/",  "sample_miyako.png", 3)
