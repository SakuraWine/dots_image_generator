import cv2
import cv2.typing
import numpy as np
import numpy._typing
from typing import List
import glob
import argparse


class DotsImageGenerator(object):
    def __init__(self) -> None:
        """constructor
        """
        pass

    def to_dots(self, image: cv2.typing.MatLike, level: int) -> None:
        """get dots image from normal image

        Args:
            image (cv2.typing.MatLike): source
            level (int): level
        """
        # 元画像のサイズを覚えとく
        height, width, channels = image.shape[:3]
        # 輝度値を見るための形式へ変換
        image_resized = cv2.resize(image, None, None, 1.0, 0.5)
        image_gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
        source = self.resize_image(image=image_gray, level=level)
        # 輝度値を点字に変換
        dots_lines: List[str] = []
        for column in source:
            dots_list: List[str] = []
            for row in column:
                dots = self.get_dots(row)
                dots_list.append(dots)
            # 一文字ずつの文字の配列を一続きの文字列へ変換する
            dots_str = "".join(dots_list)
            dots_lines.append(dots_str)
        # 出力
        for line in dots_lines:
            print(line)
        blank_image = np.zeros((height, width, 1))
        self.draw_dots(blank_image, dots_lines)

    def draw_dots(self, image: numpy._typing.NDArray, dots_lines: List[str]) -> bool:
        # TODO: drawing dots to blank image is not implemented.
        return True

    def get_dots(self, brightness: int) -> str:
        """convert brightness to dots

        Args:
            brightness (int): brightness

        Returns:
            str: dots
        """
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
        """resize image

        Args:
            image (cv2.typing.MatLike): source
            level (int): level

        Returns:
            cv2.typing.MatLike: resized image
        """
        image_rescaled = cv2.resize(image, None, None, 1.0, 0.7)
        if level == 1:
            image_resized = cv2.resize(image_rescaled, None, None, 0.15, 0.15)
        elif level == 2:
            image_resized = cv2.resize(image_rescaled, None, None, 0.25, 0.25)
        elif level == 3:
            image_resized = cv2.resize(image_rescaled, None, None, 0.5, 0.5)
        elif level == 4:
            image_resized = cv2.resize(image_rescaled, None, None, 0.75, 0.75)
        elif level == 5:
            image_resized = image_rescaled
        else:
            print("Invalid level.")
            image_resized = image_rescaled
        return image_resized

    def generate(self, source_path: str, level: int) -> None:
        """execute

        Args:
            source_path (str): source path
            level (int): _description_
        """
        # read
        image = cv2.imread(source_path, cv2.IMREAD_COLOR)
        # to grayscale
        self.to_dots(image=image, level=level)


parser = argparse.ArgumentParser(description="generate dots image from .png")
parser.add_argument("-s", "--source_image")
args = parser.parse_args()
generator = DotsImageGenerator()
sources = glob.glob("./data/" + args.source_image)
for source in sources:
    generator.generate(source, 1)
