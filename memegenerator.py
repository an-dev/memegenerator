# -*- coding: utf-8 -*-
import sys
import os
import textwrap
import configparser

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

config = configparser.ConfigParser()
config.read('config.ini')
config = config['DEFAULT']

TEMP_FILE   = os.path.join(config['ASSET_PATH'], config['TEMP_FILENAME'])
OUT_FILE    = os.path.join(config['ASSET_PATH'], config['OUT_FILENAME'])
SWOOSH_FILE = os.path.join(config['ASSET_PATH'], config['SWOOSH_ASSET'])

FONT_SIZE = config.getint('FONT_SIZE')
NIKE_OFFSET_X = config.getint('NIKE_OFFSET_X')
NIKE_OFFSET_Y = config.getint('NIKE_OFFSET_Y')


def make_meme(quote):

    swoosh  = Image.open(SWOOSH_FILE)
    img     = Image.open(TEMP_FILE)
    white_color = (255, 255, 255)

    # find biggest font size that works
    font = ImageFont.truetype(
        config['FONT_PATH'],
        FONT_SIZE)

    text_size = font.getsize(quote)

    # wrap quote
    para = textwrap.wrap(quote, width=FONT_SIZE)

    # draw canvas
    draw = ImageDraw.Draw(img)

    bottom_text_position_y = (img.size[1] / 2) - text_size[1]

    # center text, break lines and set padding
    current_h, pad = bottom_text_position_y, 7
    for line in para:
        w, h = font.getsize(line)
        bottom_text_position_x = (img.size[0] / 2) - (w / 2)
        draw.text((bottom_text_position_x, current_h), line, white_color, font=font)
        current_h += h + pad

    nike_text_size = font.getsize(config['NIKE_QUOTE'])
    nike_quote_position_x = (img.size[0] / 2) - ((nike_text_size[0] / 2) - NIKE_OFFSET_X)
    nike_quote_position_y = ((img.size[1]) - nike_text_size[1]) - NIKE_OFFSET_X
    draw.text(
        (nike_quote_position_x, nike_quote_position_y),
        config['NIKE_QUOTE'], white_color, font=font)

    img   = img.convert('L')
    final = Image.new('L', img.size)
    final.paste(img)
    final.paste(
        swoosh,
        (int(nike_quote_position_x - NIKE_OFFSET_Y), int(nike_quote_position_y - NIKE_OFFSET_X)),
        swoosh)
    final.save(OUT_FILE)


if __name__ == '__main__':
    try:
        _quote = str(sys.argv[1])
    except IndexError:
        _quote = config['DEFAULT_QUOTE']

    if len(_quote) > 70:
        raise EOFError('Use a shorter quote!')

    make_meme(_quote)
