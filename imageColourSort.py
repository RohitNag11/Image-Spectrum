import emoji as emj
import cv2
import numpy as np
from skimage import io
import math
import colorsys
import asyncio
from urllib.request import urlopen
from urllib.error import HTTPError


def lum(rgb):
    r, g, b = rgb
    return math.sqrt(.241 * r + .691 * g + .068 * b)


def step(rgb, steps=3):
    r, g, b = rgb
    lum = math.sqrt(.241 * r + .691 * g + .068 * b)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h2 = int(h * steps)
    lum2 = int(lum * steps)
    v2 = int(v * steps)
    if h2 % 2 == 1:
        v2 = steps - v2
        lum = steps - lum
    return (h2, lum, v2)


def get_average_colour(img):
    return img.mean(axis=0).mean(axis=0).astype(int)


def get_emoji_code(emojis_char):
    if emj.is_emoji(emojis_char):
        return emj.demojize(emojis_char)
    return None


def get_emoji_img_url(emojis_char, size=32):
    if (size == 32 or 512):
        emoji_code = get_emoji_code(emojis_char)
        if emoji_code:
            return f'https://emojiapi.dev/api/v1/{emoji_code}/{size}.png'
    return None


def is_valid_img_url(url):
    try:
        image_formats = ("image/png", "image/jpeg", "image/gif")
        site = urlopen(url)
        meta = site.info()
        return (meta["content-type"] in image_formats)
    except HTTPError as err:
        print(err.code)
        return False


def fetch_img(url):
    if is_valid_img_url(url):
        return io.imread(url)[:, :, :-1]
    return np.zeros(0)


async def create_emoji_colour_dict_async(emoji_chars, emoji_colour_dict={}, invalid_emojis=[]):
    i = 0
    while i < len(emoji_chars):
        emoji_img_url = get_emoji_img_url(emoji_chars[i], 32)
        emoji_img = fetch_img(emoji_img_url)
        if (emoji_img_url and emoji_img.any()):
            emoji_colour_dict[emoji_chars[i]] = get_average_colour(emoji_img)
            i += 1
        else:
            invalid_emojis.append(emoji_chars.pop(i))


if (__name__ == '__main__'):
    emojis_chars = ['📬', '☁️', '👾', '🏛', '🏢', '💷',
                    '📞', '😌', '🍿', '✈️', '🛍', '🗂']
    emoji_colour_dict = {}
    invalid_emojis = []

    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_emoji_colour_dict_async(
        emojis_chars, emoji_colour_dict, invalid_emojis))
    loop.close()

    hue_sorted_emojis = sorted(emojis_chars,
                               key=lambda emoji_char:
                               colorsys.rgb_to_hls(*emoji_colour_dict[emoji_char]))

    lum_sorted_emojis = sorted(emojis_chars,
                               key=lambda emoji_char:
                               lum(emoji_colour_dict[emoji_char]))

    step_sorted_emojis = sorted(emojis_chars,
                                key=lambda emoji_char:
                                step(emoji_colour_dict[emoji_char], 8))

    print(f'invalid emojis: {invalid_emojis}')
    print(f'valid emojis:   {emojis_chars}')
    print('******')
    print(f'hue sort:       {hue_sorted_emojis}')
    print(f'lum sort:       {lum_sorted_emojis}')
    print(f'step sort:      {step_sorted_emojis}')
