from PIL import Image


def read_image(path):
    return Image.open(path)

def save_img(image, path, *args):
    image.save(path, format=args[0])
