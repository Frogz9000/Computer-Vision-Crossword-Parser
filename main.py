#references: https://learnopencv.com/contour-detection-using-opencv-python-c/
#            https://stackoverflow.com/questions/55169645/square-detection-in-image

from typing import List, Tuple, Union, Sequence
import cv2
import cv2.typing
import numpy as np
from pathlib import Path

Image = cv2.typing.MatLike
Contour = cv2.typing.MatLike

def parse_contours(image: Image) -> Sequence[Contour]:
    grayscaled_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, black_and_white_image = cv2.threshold(grayscaled_image, thresh=150, maxval=255, type=cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(image=black_and_white_image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    return contours


def try_square_approximation(contour: Contour) -> Union[Contour, None]:
    _x, _y, w, h = cv2.boundingRect(contour)
    aspect_ratio = w / h
    contour_len = cv2.arcLength(contour, True)
    cnt = cv2.approxPolyDP(contour, epsilon=0.02*contour_len, closed=True)
    if len(cnt) <= 6 and cv2.contourArea(cnt) > 100 and abs(aspect_ratio-1) < 0.05:
        return cnt
    else:
        return None


def draw_contours(image: Image, contours: Sequence[Contour]) -> None:
    cv2.drawContours(image, contours, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)


def output_image(path: Path, image: Image):
    cv2.imwrite(str(path.absolute()), image)


def main():
    assets_root = Path('assets/')
    generated_root = Path('generated/')

    generated_root.mkdir(exist_ok=True)

    for path in assets_root.iterdir():
        image = cv2.imread(str(path.absolute()))

        if image is None:
            print(f"Error: File {path.absolute()} was not able to be read")
            return None

        contours = parse_contours(image)

        contours_image = np.zeros_like(image)
        draw_contours(contours_image, contours)
        output_image(generated_root.joinpath(f"{path.stem}-contours.jpg"), contours_image)

        square_contours = list(filter(
            lambda x: x is not None,
            [try_square_approximation(contour) for contour in contours]
        ))

        widths: List[float] = []
        for square in square_contours:
            widths.append(cv2.arcLength(square, True) / 4)

        median_width = sorted(widths)[len(widths) // 2]

        # Filter out squares of the wrong size
        square_contours: List[Contour] = list(filter(
            lambda x: abs(median_width / (cv2.arcLength(x, True) / 4) - 1) < 0.10,
            list.copy(square_contours)
        ))

        squares_image = np.zeros_like(image)
        draw_contours(squares_image, square_contours)
        output_image(generated_root.joinpath(f"{path.stem}-squares.jpg"), squares_image)

        both_image = np.copy(image)
        draw_contours(both_image, square_contours)
        output_image(generated_root.joinpath(f"{path.stem}-origin+squares.jpg"), both_image)

        # Create a new image to store the average square
        # It's more like a sum of all squares cause I don't ever divide them

        # This formula looks sus, but trust
        average_square_image_width_half = int(median_width * 0.75)
        average_square_image = np.zeros((2 * average_square_image_width_half, 2 * average_square_image_width_half, 3))

        for square in square_contours:
            x, y, w, h = cv2.boundingRect(square)
            center_x, center_y = x + w // 2, y + h // 2
            square_image = np.zeros_like(image)
            draw_contours(square_image, [square])
            x1, y1 = center_x - average_square_image_width_half, center_y - average_square_image_width_half
            x2, y2 = center_x + average_square_image_width_half, center_y + average_square_image_width_half
            cropped = square_image[y1:y2,x1:x2]
            try:
                average_square_image = average_square_image + cropped
            except ValueError:
                print(f"There's a square too close to the edge of the {path.absolute()} image. That's fine though, we'll just ignore it.")
                continue

        output_image(generated_root.joinpath(f"{path.stem}-average-square.jpg"), average_square_image)


if __name__ == "__main__":
    main()