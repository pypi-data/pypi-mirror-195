from PIL import ImageFilter, ImageOps


def add_blur(image):
    new_image = image.filter(filter=ImageFilter.BLUR)
    return new_image


def add_boder(image, color):
    border_color = color
    if border_color == None:
        border_color = 'white'
    border_image = ImageOps.expand(
        image,
        border=30,
        fill=border_color
    )
    return border_image
