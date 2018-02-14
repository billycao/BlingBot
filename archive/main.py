import numpy
from PIL import Image
import PIL.ImageOps
import pyautogui
import tesserocr
from tesserocr import PyTessBaseAPI, RIL

def main():

    while(True):
        # im = pyautogui.screenshot('screenshot.png', region=(2580,460, 70,35))
        image = Image.open('screenshot.png')

        # Invert the image.
        image_inverted = PIL.ImageOps.invert(image)
        image_inverted.save('screenshot_inverted.png')

        # Greyscale the image.
        image_inverted = image_inverted.convert('L')

        # Black/White the image.
        image_array = numpy.asarray(image_inverted).copy()
        image_array[image_array < 128] = 0
        image_array[image_array >= 128] = 255

        final_image = Image.fromarray(image_array)
        final_image.save('screenshot_processed.png')

        with PyTessBaseAPI() as api:
            api.SetImageFile('screenshot_processed_2.png')
            boxes = api.GetComponentImages(RIL.TEXTLINE, True)
            print('Found {} textline image components.'.format(len(boxes)))
            for i, (im, box, _, _) in enumerate(boxes):
                # im is a PIL image object
                # box is a dict with x, y, w and h keys
                api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
                ocrResult = api.GetUTF8Text()
                conf = api.MeanTextConf()
                print((u"Box[{0}]: x={x}, y={y}, w={w}, h={h}, "
                       "confidence: {1}, text: {2}").format(i, conf, ocrResult, **box))
            print(api.GetUTF8Text())
            print(api.AllWordConfidences())
        print(tesserocr.image_to_text(final_image))
        return



if __name__ == '__main__':
    main()
