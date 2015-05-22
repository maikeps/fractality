#!/usr/bin/python

import Tkinter
import re
import sys


class Rect:
	def __init__(self, x, y, x2, y2, name, father_name):
		self.x = x
		self.y = y
		self.x2 = x2
		self.y2 = y2
		self.name = father_name + name

	def coordinates(self):
		return [(self.x, self.y), (self.x2, self.y2)]


def create_quadrants(canvas_startx, canvas_starty, canvas_width, canvas_height, depth, father_name=''):
	# 2 | 1
	# -----
	# 3 | 4

	x = canvas_startx
	y = canvas_starty

	r1 = Rect(x+(canvas_width-x)/2, canvas_starty, canvas_width, y+(canvas_height-y)/2, '1', father_name)
	r2 = Rect(canvas_startx, canvas_starty, x+(canvas_width-x)/2, y+(canvas_height-y)/2, '2', father_name)
	r3 = Rect(canvas_startx, y+(canvas_height-y)/2, x+(canvas_width-x)/2, canvas_height, '3', father_name)
	r4 = Rect(x+(canvas_width-x)/2, y+(canvas_height-y)/2, canvas_width, canvas_height, '4', father_name)

	rects = [r1, r2, r3, r4]

	final_rects = []

	if depth-1 > 0:
		for rect in rects:
			sub_rects = create_quadrants(rect.x, rect.y, rect.x2, rect.y2, depth-1, rect.name)
			for sub_rect in sub_rects:
				final_rects.append(sub_rect)

	else:
		return rects

	return final_rects

def crazy(hex_color, rect_number):
	if hex_color[0] == '#':
		hex_color = '0x'+hex_color[1::]
	number = int(hex_color, 16)
	final_hex = hex(number*int(rect_number))[2::]
	if len(final_hex) > 6:
		final_hex = final_hex[len(final_hex)-6::]
	if len(final_hex) < 6:
		aux = ''
		for i in range(len(final_hex) - 6):
			aux += '0'
		final_hex = aux + final_hex

	return "#"+final_hex



def generate_fractal(regex, main_color, secondary_color, coloring_function=None):
	master = Tkinter.Tk()

	canvas = Tkinter.Canvas(width=800, height=800)
	canvas.pack()

	rects = create_quadrants(0, 0, 800, 800, 8)
	final_rects = []

	for rect in rects:
		color = ''
		if re.search(regex, rect.name):
			if coloring_function:
				color = globals()[coloring_function](main_color, rect.name)
			else:
				color = main_color
		else:
			color = secondary_color
		canvas.create_rectangle(rect.x, rect.y, rect.x2, rect.y2, fill=color, outline=color)

	master.mainloop()

def main():
	if len(sys.argv) > 1:
		if sys.argv[1] == '--help' or sys.argv[1] == '-h':
			print_help()
		else:
			if not arguments_correct(sys.argv):
				print("Arguments incorrect")
				return 0
			regex = find_arg('-r', sys.argv)
			if not regex_correct(regex):
				print("Regular Expression malformed")
				return 0
			main_color = find_arg('-p', sys.argv).upper()
			secondary_color = find_arg('-s', sys.argv).upper()
			if len(sys.argv) > 8:
				coloring_function = find_arg('-f', sys.argv).lower()
				if coloring_function not in globals():
					print("Function not found")
					return 0
			else:
				coloring_function = None
			generate_fractal(regex, main_color, secondary_color, coloring_function)

def find_arg(arg, argv):
	return argv[argv.index(arg)+1]

def regex_correct(regex):
	return True

def arguments_correct(argv):
	if len(argv) < 6:
		return False
	return True

def print_help():
	BOLD = '\033[1m'
	END = '\033[0m'

	print("\n")
	print(BOLD+"Fractality - Regex Fractal Generator:"+END)
	print("Fractality is a fractal generator based on regular expression.\n")

	print(BOLD+"Usage:"+END)
	print("-r <arg>\tThe regular expression used to generate the fractal")
	print("-f <arg>\tDefines the fractal coloring function")
	print("-p <arg>\tThe primary color used on the coloring function")
	print("-s <arg>\tThe secondary color used on the coloring function\n")
	print("OBS:\nThe arguments don't need to be in order;\nAll arguments need to be in quotes.\n")

	print(BOLD+"Coloring functions:"+END)
	print("crazy\n")

	print(BOLD+"Regular Expresison examples:"+END)
	print("(23|41|34|12)")
	print("(13|31|24|42)")
	print("(13|31)")
	print("(1)\n\n")

	print("Made by Maike de Paula Santos")
	print("Inspired by ssodelta: http://ssodelta.wordpress.com")

if __name__ == '__main__':
	main()