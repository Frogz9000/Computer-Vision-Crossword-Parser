#references: https://learnopencv.com/contour-detection-using-opencv-python-c/
#            https://stackoverflow.com/questions/55169645/square-detection-in-image

from typing import List, Tuple, Union, Sequence
import cv2
import cv2.typing
import numpy as np
from pathlib import Path
import pdf2image
from math import floor

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
    cv2.drawContours(image, contours, contourIdx=-1, color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA)


def output_image(path: Path, image: Image):
    cv2.imwrite(str(path.absolute()), image)


def read_image(path: Path) -> Union[Image, None]:
    if path.suffix == '.pdf':
        return np.asarray(pdf2image.convert_from_path(str(path.absolute()), dpi=300)[0])
    else:
        return cv2.imread(str(path.absolute()))


def main():
    assets_root = Path('assets/')
    generated_root = Path('generated/')
    project_assets_root = Path('AndroidAppDev/app/src/main/assets/')

    generated_root.mkdir(exist_ok=True)

    for path in assets_root.iterdir():
        image = read_image(path.absolute())

        if image is None:
            print(f"Error: File {path.absolute()} was not able to be read")
            return None

        contours = parse_contours(image)

        contours_image = np.zeros_like(image)
        draw_contours(contours_image, contours)

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
            lambda x, w=median_width: abs(w / (cv2.arcLength(x, True) / 4) - 1) < 0.10,
            list.copy(square_contours)
        ))

        max_width = max([cv2.arcLength(square, True) / 4 for square in square_contours])

        # Create a new image to store the average square
        # It's more like a sum of all squares cause I don't ever divide them

        kernel_width_half = int(max_width * 0.5 + 3)
        kernel: Image = np.zeros((2 * kernel_width_half, 2 * kernel_width_half, 3), dtype=np.float64)

        for square in square_contours:
            x, y, w, h = cv2.boundingRect(square)
            center_x, center_y = x + w // 2, y + h // 2
            square_image = np.zeros_like(image)
            draw_contours(square_image, [square])
            x1, y1 = center_x - kernel_width_half, center_y - kernel_width_half
            x2, y2 = center_x + kernel_width_half, center_y + kernel_width_half
            cropped = contours_image[y1:y2,x1:x2]
            try:
                kernel += cropped
            except ValueError:
                print(f"There's a square too close to the edge of the {path.absolute()} image. That's fine though, we'll just ignore it.")
                continue

        # Normalize the average square image
        kernel = 2 * kernel / len(square_contours)
        kernel = np.clip(kernel, 0, 255)
        kernel = (kernel - kernel.min()) / (kernel.max() - kernel.min()) * 255
        kernel[kernel == 0] = - 1024
        
        convolved_image = cv2.filter2D(contours_image, -1, kernel / 255 / 255)

        _, points_image = cv2.threshold(convolved_image, thresh=np.percentile(convolved_image, 99.7), maxval=255, type=cv2.THRESH_BINARY)

        # Create a new kernel that has a dot in the middle
        kernel2 = np.zeros((2 * kernel_width_half, 2 * kernel_width_half, 3), dtype=np.float64)
        kernel2[kernel_width_half-2:kernel_width_half+2, kernel_width_half-2:kernel_width_half+2] = 255
        kernel2 = cv2.blur(kernel2, (5, 5))
        kernel2 = (kernel2 - kernel2.min()) / (kernel2.max() - kernel2.min()) * 255
        kernel2[kernel2 == 0] = -255

        convolved_image2 = cv2.filter2D(convolved_image, -1, kernel2 / 255 / 255)
        convolved_image2: Image = (convolved_image2 - convolved_image2.min()) / (convolved_image2.max() - convolved_image2.min()) * 255

        # Find all the black dots in the image
        # and create a mask for them

        _, black_dots = cv2.threshold(image, thresh=10, maxval=255, type=cv2.THRESH_BINARY)

        # Multiply the results for the best of both worlds
        product = convolved_image2 * points_image / 255
        product = cv2.threshold(product, thresh=0, maxval=255, type=cv2.THRESH_BINARY)[1]
        product *= black_dots / 255

        product = product.astype(np.uint8)

        dots = parse_contours(product)

        leftmost = min([cv2.boundingRect(dot)[0] for dot in dots])
        rightmost = max([cv2.boundingRect(dot)[0] for dot in dots])
        topmost = min([cv2.boundingRect(dot)[1] for dot in dots])
        bottommost = max([cv2.boundingRect(dot)[1] for dot in dots])

        product[topmost:bottommost, leftmost:rightmost] = 255

        width = round(1 + (rightmost - leftmost) / (median_width + 2))
        height = round(1 + (bottommost - topmost) / (median_width + 2))

        grid = np.zeros((height, width), dtype=np.uint8)

        for dot in dots:
            x, y, _, _ = cv2.boundingRect(dot)
            offset_x = x - leftmost
            offset_y = y - topmost
            grid[round((height - 1) * offset_y / (bottommost - topmost))][round((width - 1) * offset_x / (rightmost - leftmost))] = 255
        
        output_image(generated_root.joinpath(f"{path.stem}-grid.jpg"), grid)

        with open(project_assets_root.joinpath(f"{path.stem}-grid.txt"), 'w') as f:
            f.truncate(0)
            f.write(f"{width} {height}\n")
            grid_str = ','.join([('O' if cell == 255 else 'X') for cell in grid.flatten()])
            f.write(f'{grid_str}\n')
            f.write("ACROSS\n")
            f.write("END_ACROSS\n")
            f.write("DOWN\n")
            f.write("END_DOWN\n")


if __name__ == "__main__":
    main()