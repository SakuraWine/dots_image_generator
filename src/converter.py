import cv2
import cv2.typing


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
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        source = self.resize_image(image=image_gray, level=level)
        for column in source:
            for row in column:
                print(self.get_dots(row), end="")
            print()

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
        # resize
        image_resized = cv2.resize(image, None, None, 1.0, 0.5)
        # to grayscale
        self.to_dots(image=image_resized, level=level)


generator = DotsImageGenerator()
generator.generate("/home/sakura/workspace/dots_image_generator/data/sample_miyako.png", 5)
