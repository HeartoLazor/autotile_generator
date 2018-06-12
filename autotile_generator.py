#Author: Hearto Lazor
#Assemble 3x3 bitmask tileset using a smaller template.
#Tool page: https://github.com/HeartoLazor/autotile_generator
#Based on GodotAutotileAssembler from lunarfyre7 (https://github.com/lunarfyre7/GodotAutotileAssembler)
#Developed and tested in python 3.x
#Requirements:
#	pillow python library (pip install pillow)
#	jstyleson library (pip install jstyleson)
#Command examples:
#	 python autotile_generator.py -i "jungle.png"
#	 python autotile_generator.py -i "cave.png" -d "cave_autotile.png"
#	 python autotile_generator.py -i "../input images/ice.png' -m "../input maps/seven tile map.json" -d "../autotiles/ice_autotile.png"
#This is a fully configurable 3x3 autotile tilemap generator using only 5 tiles.
#Before you do anything you need to setup your art, the default template is actually 20 tiles, but it's essentially the same amount of effort as making 5 tiles variants as long as you keep in mind that the tiles need to be cut into quarters easily. The structure of the template sprite is seamless-fill, corners/single, vertical, horizontal and inner-corners. You can typically create the seamless fill tile and modify it for the other variants.
#The template and result map could be fully customized with commands.
#Don't forget to use Quotation marks around your paths for space filename support.
#Command list:
#-i --input: The input image, if not found looks for template.png in the same directory.
#-m --input_map: The input mapping, if not found looks for default_input_map.json in the same directory.
#	 Maps input tilesets to the generated autotile result image. 
#	 Each tile in the result map is represented by 4 values: (number_1, number_2, number_3, number_4)
#	 Where 0 represents an empty tile and a number bigger than 0 represents the tile in input tile, for example 1 is the first tile in input tile.
#	 Tiles in result are constructed using each of the four values:
#		 number_1 , number_2
#		 number_3 , number_4
#	 For example a tile represented by those values (0,1,0,1) result in:
#		 top_left_corner_from_0_input_tile,	top_right_corner_from_1_input_tile
#		 bot_left_corner_from_1_input_tile,	bot_right_corner_from_0_input_tile
#	 The map json is composed by many tiles, for example:
#		 [2,3,0,1],[3,3,1,0],[4,3,2,0]
#		 [4,4,1,1],[2,2,4,0],[4,4,4,4]
#	 Result in an autotile image with 6 tiles
#	 Another important value from json map is the Input Size, which is how many tiles conform the first row from input image, 
#if last example used a input image with 4 tiles, this value should be 4. The template image uses 5 tiles.
#-d --destination: The output image destination, if not set, generates result.png in the same directory.
#-h --help: show help.

import sys
import math
import json
import jstyleson
from PIL import Image, ImageDraw

DEFAULT_INPUT_NAME = "template.png"
DEFAULT_INPUT_MAP_NAME = "default_input_map.json"
DEFAULT_DEST_NAME = "result.png"

COMMAND_INPUT = ["-i","--input","-input"]
COMMAND_INPUT_MAP = ["-m","--input_map","-input_map"]
COMMAND_RESULT_PATH = ["-d","--destination","-destination"]
COMMAND_HELP = ["-h","--help","-help"]

def process_image(input_path, input_map_path, dest_path):
	#Load input image
	source = None
	try:
		source = Image.open(input_path)
	except (FileNotFoundError, IOError, UnicodeDecodeError, SystemError) as err:
	    print("Unable to load image: " + str(input_path) + "\n" + str(err))
	    return
	except:
	    print("Unable to load image: " + str(input_path))
	    return
	if(source == None):
		return
	#load input map json
	input_map = None
	try:
		result = open(input_map_path, 'r')
		input_map = jstyleson.dispose(result)
		input_map = jstyleson.loads(input_map)
		result.close()
	except (FileNotFoundError, IOError, UnicodeDecodeError, SystemError, json.JSONDecodeError) as err:
	    print("Unable to load input json map: " + str(input_map_path) + "\n" + str(err))
	    return
	except:
	    print("Unable to load input json map: " + str(input_map_path))
	    return
	#Extract json values
	source_quantity = None
	generator_map = None
	if(input_map == None):
		return
	else:
		if("input_size" in input_map):
			try:
				source_quantity = abs(int(input_map["input_size"]))
			except:
				source_quantity = None
		if("input_map" in input_map):
			generator_map = validate_generator_map(input_map["input_map"])
	if(source_quantity == None or generator_map == None):
		if(source_quantity == None):
			print("input_size parameter invalid or not found in json file.")
		if(generator_map == None):
			print("input_map parameter invalid or not found in json file.")
		return
	#Process files and save
	source = source.convert("RGBA")
	tile_size = int(source.width / source_quantity)
	tile_half_size = int(tile_size * 0.5)
	tile_quantity = source_quantity
	variation_quantity = math.floor(source.height / tile_size)
	max_cell_len = 0
	for cells in generator_map:
		cell_len = len(cells)
		if(cell_len > max_cell_len):
			max_cell_len = cell_len
	dest_tile_quantity = (max_cell_len, len(generator_map))
	dest_tile_size = (dest_tile_quantity[0] * tile_size, dest_tile_quantity[1] * tile_size * variation_quantity)
	dest = Image.new("RGBA", dest_tile_size)
	#image sections,  1 cell is composed of 4 portions of each tile, 
	#where 0 = top left, 1 = top right, 2 = bot left and 3 = bot right. Those values are the ones used by generator_map
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
	#create autotile image
	generator_map_size = len(generator_map)
	for v in range(0, variation_quantity):
		for x in range(0, generator_map_size):
			r_cells = generator_map[x]
			r_cells_size = len(r_cells)
			for y in range(0, r_cells_size):
				r_cell = r_cells[y]
				cell = r_cell[0]
				if(cell > 0):
					dest.paste(source_map[v][cell - 1][0], (y * tile_size, (x + v * generator_map_size) * tile_size))
				cell = r_cell[1]
				if(cell > 0):
					dest.paste(source_map[v][cell - 1][1], (y * tile_size + tile_half_size, (x + v * generator_map_size) * tile_size))
				cell = r_cell[2]
				if(cell > 0):
					dest.paste(source_map[v][cell - 1][2], (y * tile_size,  (x + v * generator_map_size) * tile_size + tile_half_size))
				cell = r_cell[3]
				if(cell > 0):
					dest.paste(source_map[v][cell - 1][3], (y * tile_size + tile_half_size, (x + v * generator_map_size) * tile_size + tile_half_size))
	try:
		dest.save(dest_path)
	except (ValueError, IOError, SystemError) as err:
	    print("Unable to save file: " + str(dest_path) + "\nCheck input_size in input map. Tile calculated size: " + str(tile_size) + "\n" + str(err))

#return a ready to process generator map, return None in case of an invalid input map
def validate_generator_map(json_map):
	generator_map = None
	try:
		g_map = json_map
		if(isinstance(g_map, list) and len(g_map) > 0):
			for row in g_map:
				if(isinstance(row, list) == False):
					return None
				for cells in row:
					if(isinstance(cells, list) == False or len(cells) != 4):
						return None
					cell_size = len(cells)
					for j in range(0,cell_size):
						cells[j] = int(cells[j])
			generator_map = g_map
	except (ValueError) as err:
	    print("Invalid tile map value: " + "\n" + str(err))
	except:
		generator_map = None
	if(generator_map != None):
		max_row_size = 0
		for row in generator_map:
			row_size = len(row)
			if(row_size > max_row_size):
				max_row_size = row_size
		for row in generator_map:
			while(len(row) < max_row_size):
				row.append((0,0,0,0))
	if(len(generator_map) == 1 and len(generator_map[0]) == 0):
		return None
	return generator_map

def dump_help():
	print("This is a fully configurable 3x3 autotile tilemap generator using only 5 tiles.")
	print("Before you do anything you need to setup your art, the default template is actually 20 tiles, but it's essentially the same amount of effort as making 5 tiles variants as long as you keep in mind that the tiles need to be cut into quarters easily. The structure of the template sprite is seamless-fill, corners/single, vertical, horizontal and inner-corners. You can typically create the seamless fill tile and modify it for the other variants.")
	print("The template and result map could be fully customized with commands.")
	print("Author: Hearto Lazor. Based in GodotAutotileAssembler from lunarfyre7")
	print("Tool page: https://github.com/HeartoLazor/autotile_generator")
	print("Command examples:")
	print("\t python autotile_generator.py -i \"jungle.png\"")
	print("\t python autotile_generator.py -i \"cave.png\" -d \"cave_autotile.png\"")
	print("\t python autotile_generator.py -i \"../input images/ice.png\" -m \"../input maps/seven tile map.json\" -d \"../autotiles/ice_autotile.png\"")
	print("Don't forget to use Quotation marks around your paths for space filename support.")
	print("Command list:")
	print("-i --input: The input image, if not found looks for template.png in the same directory.")
	print("-m --input_map: The input mapping, if not found looks for default_input_map.json in the same directory.")
	print("\t Maps input tilesets to the generated autotile result image. ")
	print("\t Each tile in the result map is represented by 4 values: (number_1, number_2, number_3, number_4)")
	print("\t Where 0 represents an empty tile and a number bigger than 0 represents the tile in input tile, for example 1 is the first tile in input tile.")
	print("\t Tiles in result are constructed using each of the four values:")
	print("\t\t number_1 , number_2")
	print("\t\t number_3 , number_4")
	print("\t For example a tile represented by those values (0,1,0,1) result in:")
	print("\t\t top_left_corner_from_0_input_tile,	top_right_corner_from_1_input_tile")
	print("\t\t bot_left_corner_from_1_input_tile,	bot_right_corner_from_0_input_tile")
	print("\t The map json  is composed by many tiles, for example:")
	print("\t\t (2,3,0,1),(3,3,1,0),(4,3,2,0)")
	print("\t\t (4,4,1,1),(2,2,4,0),(4,4,4,4)")
	print("\t Result in an autotile image with 6 tiles")
	print("\t Another important value from json map is the Input Size, which is how many tiles conform the first row from input image, ")
	print("\t if last example used a input image with 4 tiles, this value should be 4. The template image uses 5 tiles.")
	print("-d --destination: The output image destination, if not set, generates result.png in the same directory.")
	print("-h --help: show help.")

def main():
	#search help
	result = read_command(COMMAND_HELP, sys.argv)
	if(result != -1):
		dump_help()
	else:
		#search input
		input_path = DEFAULT_INPUT_NAME
		result = read_command(COMMAND_INPUT, sys.argv)
		if(result != -1):
			result = read_command_value(result, sys.argv)
			if(result != None):
				input_path = result
		#search input map
		input_map_path = DEFAULT_INPUT_MAP_NAME
		result = read_command(COMMAND_INPUT_MAP, sys.argv)
		if(result != -1):
			result = read_command_value(result, sys.argv)
			if(result != None):
				input_map_path = result
		destination_path = DEFAULT_DEST_NAME
		#search destination
		result = read_command(COMMAND_RESULT_PATH, sys.argv)
		if(result != -1):
			result = read_command_value(result, sys.argv)
			if(result != None):
				destination_path = result
		process_image(input_path, input_map_path, destination_path)
 
#look for a command and returns the arg index, if not found return -1
def read_command(commands, args):
	args_size = len(args)
	for i in range(0, args_size):
		clean_arg = args[i].strip().lower()
		for command in commands:
			if(clean_arg == command):
				return i
	return -1

#looks for a command value based in the command index
def read_command_value(index, args):
	args_size = len(args)
	if(args_size > 2 and index < args_size and index + 1 < args_size):
		return args[index + 1]
	return None


if __name__ == '__main__':
	main()