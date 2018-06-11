#Author: Hearto Lazor
#Assemble 3x3 bitmask tileset using a minitileset.
#Run on a sprite using the template format
#Based on GodotAutotileAssembler from lunarfyre7 (https://github.com/lunarfyre7/GodotAutotileAssembler)
#Developed and tested in python 3.x
#requires pillow library
#pip install pillow
#usage: python autotile_generator.py path_to_image

import sys
import math
from PIL import Image, ImageDraw

# BLANK = 0
# FILL = 1
# CENTER = 2
# VERTICAL = 3
# HORIZONTAL = 4
# INSIDE = 5
RESULT_MAP = [
    [(2,2,3,3),(2,4,3,5),(4,4,5,5),(4,2,5,3),(1,5,5,5),(4,4,5,1),(4,4,1,5),(5,1,5,5),(2,4,3,1),(5,5,1,1),(4,4,1,1),(4,2,1,3)],
    [(3,3,3,3),(3,5,3,5),(5,5,5,5),(5,3,5,3),(3,5,3,1),(5,1,1,1),(1,5,1,1),(5,3,1,3),(3,1,3,1),(5,1,1,5),(0,0,0,0),(1,5,1,5)],
    [(3,3,2,2),(3,5,2,4),(5,5,4,4),(5,3,4,2),(3,1,3,5),(1,1,5,1),(1,1,1,5),(1,3,5,3),(5,1,5,1),(1,1,1,1),(1,5,5,1),(1,3,1,3)],
    [(2,2,2,2),(2,4,2,4),(4,4,4,4),(4,2,4,2),(5,5,1,5),(5,1,4,4),(1,5,4,4),(5,5,5,1),(3,1,2,4),(1,1,4,4),(1,1,5,5),(1,3,4,2)]
]

SOURCE_QUANTITY = 5
DEFAULT_DEST_NAME = "result.png"

def process_image(image_path, dest_name = DEFAULT_DEST_NAME):
	try:
		source = Image.open(image_path)
	except:
	    print("Unable to load image: " + str(image_path) + " ", sys.exc_info())
	    return
	source = source.convert("RGBA")
	tile_size = int(source.width / SOURCE_QUANTITY)
	tile_half_size = int(tile_size * 0.5)
	tile_quantity = SOURCE_QUANTITY
	variation_quantity = math.floor(source.height / tile_size)
	max_cell_len = 0
	for cells in RESULT_MAP:
		cell_len = len(cells)
		if(cell_len > max_cell_len):
			max_cell_len = cell_len
	dest_tile_quantity = (max_cell_len, len(RESULT_MAP))
	dest_tile_size = (dest_tile_quantity[0] * tile_size, dest_tile_quantity[1] * tile_size * variation_quantity)
	dest = Image.new("RGBA", dest_tile_size)
	#image sections,  1 cell is composed of 4 portions of each tile, 
	#where 0 = top left, 1 = top right, 2 = bot left and 3 = bot right. Those values are the ones used by RESULT_MAP
	source_map = []
	for v in range(0, variation_quantity):
		variation = []
		for x in range(0, source.width , tile_size):
			cell = []
			pos_x = x
			pos_y = v * tile_size
			cell.append(source.crop((pos_x, pos_y, pos_x + tile_half_size, pos_y + tile_half_size)))
			pos_x = x + tile_half_size
			pos_y = v * tile_size
			cell.append(source.crop((pos_x, pos_y, pos_x + tile_half_size, pos_y + tile_half_size)))
			pos_x = x
			pos_y = v * tile_size + tile_half_size
			cell.append(source.crop((pos_x, pos_y, pos_x + tile_half_size, pos_y + tile_half_size)))
			pos_x = x + tile_half_size
			pos_y = v * tile_size + tile_half_size
			cell.append(source.crop((pos_x, pos_y, pos_x + tile_half_size, pos_y + tile_half_size)))
			variation.append(cell)
		source_map.append(variation)
	result_map_size = len(RESULT_MAP)
	for v in range(0, variation_quantity):
		for x in range(0, result_map_size):
			r_cells = RESULT_MAP[x]
			r_cells_size = len(r_cells)
			for y in range(0, r_cells_size):
				r_cell = r_cells[y]
				cell = r_cell[0]
				if(cell > 0):
					dest.paste(source_map[v][cell - 1][0], (y * tile_size, (x + v * result_map_size) * tile_size))
				cell = r_cell[1]
				if(cell > 0):
					dest.paste(source_map[v][cell - 1][1], (y * tile_size + tile_half_size, (x + v * result_map_size) * tile_size))
				cell = r_cell[2]
				if(cell > 0):
					dest.paste(source_map[v][cell - 1][2], (y * tile_size,  (x + v * result_map_size) * tile_size + tile_half_size))
				cell = r_cell[3]
				if(cell > 0):
					dest.paste(source_map[v][cell - 1][3], (y * tile_size + tile_half_size, (x + v * result_map_size) * tile_size + tile_half_size))
	dest.save(dest_name)

def main():
	print(sys.argv)
	if(len(sys.argv) > 2):
		process_image(sys.argv[1],sys.argv[2])
	elif(len(sys.argv) > 1):
		process_image(sys.argv[1])
	else:
		print("Image Path parameter is required")
 
if __name__ == '__main__':
	main()