This is a project using OpenCV to scan and analyize a crossword puzzle.
The current goal is to simply take a downloaded image, find the squares of the puzzle and output the grid needed to represent it.
Run a second CV process to parse the text and clues and correctly assess if they are down or across

Future goals:
Modify ImageScanner to not just be code from an article and connect to a phone to scan a crossword on a piece of paper
Take the information parsed from the image and export it to a seperate GUI type thing to play it
    -> basically take the scan of a paper crossword and create a digital game version on your phone

Stretch Crazy goal:
Have the digital version get solved with ML to have a crossword solver as well (since it would be funny to spoil a crossword puzzle with an app)

python package import list:
pip install -U scikit-image
pip install --upgrade imutils
pip install opencv-python
pip install numpy

Dart stuff (WIP):
flutter install guide -> https://docs.flutter.dev/get-started/install
These are from cursory search, there may be better packages to do this with
OCR tool ->  https://pub.dev/packages/google_ml_kit
OpenCV -> https://pub.dev/packages/opencv_dart
Numpy -> https://github.com/jsonfm/numpy-dart