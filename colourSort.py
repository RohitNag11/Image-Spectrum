import random
import colorsys
import math


def rgb_block(rgb):
    r, g, b = rgb
    return f"\033[48:2::{int(255*r)}:{int(255*g)}:{int(255*b)}m \033[49m"


def print_rgb_colours(rgb_colours):
    for rgb_colour in rgb_colours:
        print(rgb_block(rgb_colour), end='')
    print()


def lum(r, g, b):
    return math.sqrt(.241 * r + .691 * g + .068 * b)


def step(r, g, b, repetitions=1):
    lum = math.sqrt(.241 * r + .691 * g + .068 * b)

    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    h2 = int(h * repetitions)
    lum2 = int(lum * repetitions)
    v2 = int(v * repetitions)

    if h2 % 2 == 1:
        v2 = repetitions - v2
        lum = repetitions - lum

    return (h2, lum, v2)


length = 100
rgb_colours = [(random.random(), random.random(), random.random())
               for i in range(length)]
sorted_rgb_colours_by_hue = sorted(
    rgb_colours, key=lambda rgb: colorsys.rgb_to_hls(*rgb)[0])
sorted_rgb_colours_by_lum = sorted(
    rgb_colours, key=lambda rgb: lum(*rgb))
sorted_rgb_colours_by_steps = sorted(
    rgb_colours, key=lambda rgb: step(*rgb, length//20))

# print_rgb_colours(rgb_colours)
# print(hsv_colours)
# print(sorted_rgb_colours)
print_rgb_colours(rgb_colours)
print_rgb_colours(sorted_rgb_colours_by_hue)
print_rgb_colours(sorted_rgb_colours_by_lum[::-1])
print_rgb_colours(sorted_rgb_colours_by_steps)
