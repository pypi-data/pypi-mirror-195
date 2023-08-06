from PIL import (Image,
                 ImageDraw,
                 ImageFont)


def create_thumbnail(img, path=''):
    MAX_SIZE = (100, 100)
    return img.thumbnail(MAX_SIZE)


def draw_text(img, position_x, position_y, text, **kwargs):
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(kwargs['text_color'])
    text_color = kwargs['text_color']
    font_size = kwargs['font_size']

    if ['text_color'] not in kwargs:
        text_color = (255, 255, 255, 255)
    
    if ['font_type'] not in kwargs:
        font=ImageFont.truetype('Roboto.otf')

    if ['font_size'] not in kwargs:
        font_size = 80
    
    
    draw_image = draw.text((position_x, position_y), text, fill=text_color, font=font, size=font_size)
    
    return draw_image
