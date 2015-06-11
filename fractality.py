#!/usr/bin/python

try:
    import tkinter
except ImportError:
    import Tkinter
    
import re
import sys

_x1, _y1, _x2, _y2, _name = range(5)


def rectangle(x1, y1, x2, y2, name, father_name):
    return (x1, y1, x2, y2, father_name + name)


def create_quadrants(canvas_startx, canvas_starty, canvas_width, canvas_height,
                     depth, father=''):
    # 2 | 1
    # -----
    # 3 | 4

    x0, y0, x, y = canvas_startx, canvas_starty, canvas_width, canvas_height
    delta_x, delta_y = x - x0 >> 1, y - y0 >> 1

    rects = (
        rectangle(x0 + delta_x, y0, x, y0 + delta_y, '1', father),
        rectangle(x0, y0, x0 + delta_x, y0 + delta_y, '2', father),
        rectangle(x0, y0 + delta_y, x0 + delta_x, y, '3', father),
        rectangle(x0 + delta_x, y0 + delta_y, x, y, '4', father),
    )

    if depth <= 1:
        return rects

    final_rects = []
    for rect in rects:
        final_rects.extend(
            create_quadrants(rect[_x1], rect[_y1], rect[_x2], rect[_y2],
                             depth - 1, rect[_name]))

    return final_rects


def crazy(hex_color, rect_number):
    if hex_color[0] == '#':
        hex_color = '0x' + hex_color[1::]
    number = int(hex_color, 16)
    final_hex = hex(number * int(rect_number))[2::]
    if len(final_hex) > 6:
        final_hex = final_hex[len(final_hex) - 6::]
    if len(final_hex) < 6:
        aux = ''
        for i in range(len(final_hex) - 6):
            aux += '0'
        final_hex = aux + final_hex

    return "#" + final_hex


def generate_fractal(regex, main_color, secondary_color, depth,
                     coloring_function=None):
    def noop(x, y):
        return x

    if coloring_function is None:
        coloring_function = noop
    else:
        coloring_function = globals()[coloring_function]
        
    try:
        master = tkinter.Tk()
        canvas = tkinter.Canvas(width=600, height=600)
    except NameError:
        master = Tkinter.Tk()
        canvas = Tkinter.Canvas(width=600, height=600)
 
    canvas.pack()

    rects = create_quadrants(0, 0, 600, 600, depth)

    for rect in rects:
        if regex.search(rect[_name]) is not None:
            color = coloring_function(main_color, rect[_name])
        else:
            color = secondary_color

        canvas.create_rectangle(rect[_x1], rect[_y1], rect[_x2], rect[_y2],
                                fill=color, outline=color)

    master.mainloop()


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--regex', '-r', type=re.compile,
                        help='The regular expression used to generate the fractal')
    parser.add_argument('--colors', '-c', nargs=2,
                        help='The colors used on the coloring function')
    parser.add_argument('--function', '-f', nargs='?',
                        help='Defines the fractal coloring function (optional)')
    parser.add_argument('--depth', '-d', type=int, nargs='?', default=8,
                        help='The detail depth of the fractal (optional)')

    args = parser.parse_args()
    generate_fractal(regex=args.regex, main_color=args.colors[0],
                     secondary_color=args.colors[1], depth=args.depth,
                     coloring_function=args.function)


if __name__ == '__main__':
    main()
