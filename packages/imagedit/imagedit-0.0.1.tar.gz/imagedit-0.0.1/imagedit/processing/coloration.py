from PIL import ImageEnhance


def add_contrast(image, value):
    new_image = ImageEnhance.Contrast(image)
    return new_image.enhance(1+value)


def remove_contrast(image, value):
    new_image = ImageEnhance.Contrast(image)
    return new_image.enhance(1-value)


def add_brightness(image, value):
    new_image = ImageEnhance.Brightness(image)
    return new_image.enhance(1+value)


def remove_brightness(image, value):
    new_image = ImageEnhance.Brightness(image)
    return new_image.enhance(1-value)


def add_color(image, value):
    new_image = ImageEnhance.Color(image)
    return new_image.enhance(1+value)


def remove_color(image, value):
    new_image = ImageEnhance.Color(image)
    return new_image.enhance(1-value)
