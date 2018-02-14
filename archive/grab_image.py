import numpy
from PIL import Image
import PIL.ImageOps
import pyautogui
from tesserocr import PyTessBaseAPI

def main():
    num = 14
    image = pyautogui.screenshot('%d.png' % num, region=(2580,460, 70,70))

    # Invert the image.
    image_inverted = PIL.ImageOps.invert(image)
    image_inverted.save('%d_inverted.png' % num)

    # Greyscale the image.
    image_inverted = image_inverted.convert('L')

    # Black/White the image.
    image_array = numpy.asarray(image_inverted).copy()
    image_array[image_array < 128] = 0
    image_array[image_array >= 128] = 255

    final_image = Image.fromarray(image_array)
    final_image.save('%d_final.png' % num)




if __name__ == '__main__':
    main()
