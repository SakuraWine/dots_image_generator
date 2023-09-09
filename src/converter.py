import cv2
import cv2.typing
import numpy as np
import numpy._typing
from typing import List, Optional
import argparse
import os
from PIL import Image, ImageDraw, ImageFont
import math


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
        # 輝度値を見るための形式へ変換
        image_resized = cv2.resize(image, None, None, 1.0, 0.5)
        image_gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
        source = self.resize_image(image=image_gray, level=level)
        if source is None:
            return
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
        self.output_dots_image(dots_lines, level)

    def output_dots_image(self, dots_lines: List[str], level: int) -> None:
        """点字データから点字風画像を生成する

        Args:
            width (int): 元画像の横
            height (int): 元画像の縦
            dots_lines (List[str]): 点字データ
        """
        # NOTE: フォントの読み込みだけ色々大変だった
        #       これはWSL2環境用で、それ以外で動くようにはなっていない
        #       また、別途WSL2上からWindowsのフォントが参照できるように設定する必要がある()
        font = ImageFont.truetype(font="/mnt/c/Windows/Fonts/seguisym.ttf", size=10, encoding="utf-8")
        dots = ""
        for line in dots_lines:
            dots += "\n" + line
        dots = dots[1:]     # 先頭の改行だけ削除
        # 1文字あたりの縦横のpixel数（結構適当に数えて決めた）
        # NOTE: 多少大きめに取る
        horizontal_character_px = 4
        vertical_px = 8
        horizontal_blank_px = 4
        vertical_blank_px = 8
        num_characters_one_line = len(dots_lines[0])
        num_lines = len(dots_lines)
        # 点字風画像を生成
        output_image = Image.new("L", (horizontal_character_px * num_characters_one_line + horizontal_blank_px * num_characters_one_line,
                                       vertical_px * num_lines + vertical_blank_px * num_lines), color=0)
        draw = ImageDraw.Draw(output_image)
        draw.text((0, 0), dots, "white", font=font, spacing=4)
        output = os.path.join(os.path.dirname(__file__), "../output/", "output.png")
        output_image.save(output)

    def get_dots(self, brightness: int) -> str:
        """convert brightness to dots

        Args:
            brightness (int): brightness

        Returns:
            str: dots
        """
        # TODO: 調整するかも
        if brightness < 10:
            return "⣿"
        elif brightness < 64:
            return "⠿"
        elif brightness < 128:
            return "⠞"
        elif brightness < 224:
            return "⠓"
        else:
            return "⠂"

    def resize_image(self, image: cv2.typing.MatLike, level: int) -> Optional[cv2.typing.MatLike]:
        """レベル設定に応じて出力画像をリサイズする

        Args:
            image (cv2.typing.MatLike): source
            level (int): level

        Returns:
            cv2.typing.MatLike: resized image
        """
        # 色々試行錯誤した結果サイズ調整は必要なくなったが、一応残しておく
        image_rescaled = cv2.resize(image, None, None, 1.0, 1.0)
        if level == 5:
            image_resized = cv2.resize(image_rescaled, None, None, 0.15, 0.15)
        elif level == 4:
            image_resized = cv2.resize(image_rescaled, None, None, 0.25, 0.25)
        elif level == 3:
            image_resized = cv2.resize(image_rescaled, None, None, 0.5, 0.5)
        elif level == 2:
            image_resized = cv2.resize(image_rescaled, None, None, 0.75, 0.75)
        elif level == 1:
            image_resized = image_rescaled
        else:
            print("Invalid level.")
            return None
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


parser = argparse.ArgumentParser(description="generate dots image from image")
parser.add_argument("-s", "--source_image")
parser.add_argument("-l", "--level")
args = parser.parse_args()
generator = DotsImageGenerator()
source = os.path.join(os.path.dirname(__file__), "../data/", args.source_image)
if os.path.exists(source):
    generator.generate(source, int(args.level))
else:
    print("Source image file not found. ({})".format(args.source_image))