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


def get_average_color(img):
    return img.mean(axis=0).mean(axis=0).astype(int)


def get_emoji_code(emoji):
    if emj.is_emoji(emoji):
        return emj.demojize(emoji)
    return None


def get_emoji_img_url(emoji):
    emoji_code = get_emoji_code(emoji)
    if emoji_code:
        return f'https://emojiapi.dev/api/v1/{emoji_code}/32.png'
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


async def create_emoji_color_dict_async(emojis_chars, emoji_color_dict={}, not_emojis=[]):
    for i, emoji_char in enumerate(emojis_chars):
        emoji_img_url = get_emoji_img_url(emoji_char)
        emoji_img = fetch_img(emoji_img_url)
        if (emoji_img_url and emoji_img.any()):
            emoji_color_dict[emoji_char] = get_average_color(emoji_img)
        else:
            not_emoji = emojis_chars.pop(i)
            not_emojis.append(not_emoji)
    return emoji_color_dict, not_emojis

emojis_chars = ['😠', '🌥', '🍎', '🥒', '💙', '💚',
                '🫐', '👑', '🌓', '🌾', '📈', '🗂', '🅰️']
emoji_color_dict = {}
not_emojis = []

loop = asyncio.get_event_loop()
loop.run_until_complete(create_emoji_color_dict_async(
    emojis_chars, emoji_color_dict, not_emojis))
loop.close()


hue_sorted_emojis = sorted(emojis_chars,
                           key=lambda emoji_char:
                           colorsys.rgb_to_hls(*emoji_color_dict[emoji_char]))

lum_sorted_emojis = sorted(emojis_chars,
                           key=lambda emoji_char:
                           lum(emoji_color_dict[emoji_char]))

step_sorted_emojis = sorted(emojis_chars,
                            key=lambda emoji_char:
                            step(emoji_color_dict[emoji_char], 8))


print(f'original: {emojis_chars}')
print(f'hue sort:  {hue_sorted_emojis}')
print(f'lum sort:  {lum_sorted_emojis}')
print(f'step sort: {step_sorted_emojis}')
