from PIL import Image


def rotate_img(image, option):

    if option == 1:
        return image.transpose(Image.ROTATE_90)
    elif option == 2:
        return image.transpose(Image.ROTATE_180)
    elif option == 3:
        return image.transpose(Image.ROTATE_270)
    

def flip_img(image, option):

    # Inverte na horizontal
    if option == 1:
        return image.transpose(Image.FLIP_LEFT_RIGHT)
    # Inverte na vertical
    elif option == 2:
        return image.transpose(Image.FLIP_TOP_BOTTOM)


def merge_images(image1, image2, **kwargs):
    img2 = Image.open(image2)
    if kwargs['position_x'] == None or kwargs['position_y'] == None:
        kwargs['position_x'] = 0
        kwargs['position_y'] = 0
    
    image1.paste(img2, (kwargs['position_x'],kwargs['position_y']), kwargs['mask'])
    return image1
