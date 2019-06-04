#Author: Hearto Lazor
#Assemble 3x3 bitmask tileset using a smaller template.
#Tool page: https://github.com/HeartoLazor/autotile_generator
#Based on GodotAutotileAssembler from lunarfyre7 (https://github.com/lunarfyre7/GodotAutotileAssembler)
#Developed and tested in python 3.x
#Requirements:
#	pillow python library (pip install pillow)
#	jstyleson library (pip install jstyleson)
#Command examples:
#	 python -m autotile_generator -s "jungle.png"
#	 python -m autotile_generator -s "cave.png" -d "cave_autotile.png"
#	 python -m autotile_generator -s "../input images/ice.png' -i "../input maps/seven tile map.json" -d "../autotiles/ice_autotile.png"
#This is a fully configurable 3x3 autotile tilemap generator using only 5 tiles.
#Before you do anything you need to setup your art, the default template is actually 20 tiles, but it's essentially the same amount of effort as making 5 tiles variants as long as you keep in mind that the tiles need to be cut into quarters easily. The structure of the template sprite is seamless-fill, corners/single, vertical, horizontal and inner-corners. You can typically create the seamless fill tile and modify it for the other variants.
#The template and result map could be fully customized with commands.
#Don't forget to use Quotation marks around your paths for space filename support.
#Command list:
#-s, --source or --source_image: The source image, if not found looks for template.png in the same directory.
#-i, --input_map: The input mapping, if not found looks for default_input_map.json in the same directory.
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
import pkg_resources
import re
from PIL import Image, ImageDraw

DEFAULT_INPUT_NAME = "template.png"
DEFAULT_INPUT_MAP_NAME = pkg_resources.resource_filename('autotile_generator', 'default_input_map.json')
DEFAULT_DEST_SUFFIX = "_autotile.png"

COMMAND_SOURCE = ["-s","--source","-source","--source_image","-source_image"]
COMMAND_INPUT_MAP = ["-i","--input_map","-input_map"]
COMMAND_RESULT_PATH = ["-d","--destination","-destination"]
COMMAND_HELP = ["-h","--help","-help"]

def draw_source_map(source_map, tile_size, save_path):
	tile_half_size = { 'x':int(tile_size['x'] * 0.5),'y':int(tile_size['y'] * 0.5) }
	image = Image.new("RGBA", (len(source_map) * tile_size['x'], len(source_map[0]) * tile_size['y']))
	for i in range(0, len(source_map)):
		for j in range(0, len(source_map[i])):
			cell = source_map[i][j]
			p = {'x':i * tile_size['x'],'y':j * tile_size['y']}
			if(cell != None):
				image.paste(cell[0], (p['x'], p['y']))
				image.paste(cell[1], (p['x'] + tile_half_size['x'], p['y']))
				image.paste(cell[2], (p['x'], p['y'] + tile_half_size['y']))
				image.paste(cell[3], (p['x'] + tile_half_size['x'], p['y'] + tile_half_size['y']))
	image.save(save_path)

def is_tile_empty(tile):
	pixels = list(tile.getdata())
	for pixel in pixels:
		if(pixel[3] != 0):
			return False
	return True

def create_cells(pos, tile_half_size, source):
	cell = []
	pos_x = pos['x']
	pos_y = pos['y']
	cell.append(source.crop((pos_x, pos_y, pos_x + tile_half_size['x'], pos_y + tile_half_size['y'])))
	pos_x = pos['x'] + tile_half_size['x']
	pos_y = pos['y']
	cell.append(source.crop((pos_x, pos_y, pos_x + tile_half_size['x'], pos_y + tile_half_size['y'])))
	pos_x = pos['x']
	pos_y = pos['y'] + tile_half_size['y']
	cell.append(source.crop((pos_x, pos_y, pos_x + tile_half_size['x'], pos_y + tile_half_size['y'])))
	pos_x = pos['x'] + tile_half_size['x']
	pos_y = pos['y'] + tile_half_size['y']
	cell.append(source.crop((pos_x, pos_y, pos_x + tile_half_size['x'], pos_y + tile_half_size['y'])))
	return cell

def create_autotile(generator_map, tile_size, source, autocomplete):
	tile_half_size = { 'x':int(tile_size['x'] * 0.5),'y':int(tile_size['y'] * 0.5) }
	source_quantity = { 'x':math.floor(source.width / tile_size['x']),'y':math.floor(source.height / tile_size['y']) } 
	#image sections,  1 cell is composed of 4 portions of each tile, 
	#where 0 = top left, 1 = top right, 2 = bot left and 3 = bot right. Those values are the ones used by generator_map and an empty cell = None
	source_map = []
	for x in range(0, source_quantity['x']):
		variation = []
		for y in range(0, source_quantity['y']):
			p = {'x':x * tile_size['x'],'y':y * tile_size['y']}
			if(is_tile_empty(source.crop((p['x'], p['y'], p['x'] + tile_size['x'], p['y'] + tile_size['y'])))):
				cell = None
				if(autocomplete):
					for sy in range(0, source_quantity['y']):
						sp = {'x':x * tile_size['x'],'y':sy * tile_size['y']}
						empty = is_tile_empty(source.crop((sp['x'], sp['y'], sp['x'] + tile_size['x'], sp['y'] + tile_size['y'])))
						if(sy != y and not empty):
							cell = create_cells(sp, tile_half_size, source)
				variation.append(cell)
			else:
				variation.append(create_cells(p, tile_half_size, source))
		source_map.append(variation)

	#Calculate result image size
	result_size = {'x':0,'y':0}
	for cells in generator_map:
		cell_len = len(cells)
		if(cell_len > result_size['x']):
			result_size['x'] = cell_len
	result_size['x'] *= tile_size['x']
	width = 0
	for v_index in range(0, source_quantity['y']):
		for i in range(0, len(generator_map)):
			for j in range(0, len(generator_map[i])):
				cells = generator_map[i][j]
				skip = False
				for cell in cells:
					cell = cell - 1
					if(source_map[cell][v_index] == None):
						skip = True
						break
				if(not skip):
					width += tile_size['x']
				if(width >= result_size['x']):
					result_size['y'] += tile_size['y']
					width = 0
	if(width > 0):
		result_size['y'] += tile_size['y']
	if(result_size['x'] <= 0 and result_size['y'] <= 0):
		print("Empty image input.")
		return None

	#Render result image
	image_result = Image.new("RGBA", (result_size['x'], result_size['y']))
	width = 0
	height = 0
	for v_index in range(0, source_quantity['y']):
		for i in range(0, len(generator_map)):
			for j in range(0, len(generator_map[i])):
				cells = generator_map[i][j]
				skip = False
				for cell in cells:
					cell = cell - 1
					if(source_map[cell][v_index] == None):
						skip = True
						break
				if(not skip):
					cell = cells[0]
					if(cell > 0):
						image_result.paste(source_map[cell - 1][v_index][0], (width, height))
					cell = cells[1]
					if(cell > 0):
						image_result.paste(source_map[cell - 1][v_index][1], (width + tile_half_size['x'], height))
					cell = cells[2]
					if(cell > 0):
						image_result.paste(source_map[cell - 1][v_index][2], (width, height + tile_half_size['y']))
					cell = cells[3]
					if(cell > 0):
						image_result.paste(source_map[cell - 1][v_index][3], (width + tile_half_size['x'],  height + tile_half_size['y']))
					width += tile_size['x']
				if(width >= result_size['x']):
					height += tile_size['y']
					width = 0
					
	return image_result

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
	source = source.convert("RGBA")
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
	tile_size = None
	generator_map = None
	autocomplete = False
	if(input_map == None):
		return
	else:
		if("input_size" in input_map):
			print("input_size parameter is deprecated. Use instead: ""tile_width"":32,""tile_height"":32")
		if("tile_width" in input_map and "tile_height" in input_map):
			try:
				tile_size = { 'x':abs(int(input_map["tile_width"])), 'y':abs(int(input_map["tile_height"])) }
			except:
				tile_size = None
		if("autocomplete" in input_map):
			autocomplete = bool(input_map["autocomplete"])
		if("input_map" in input_map):
			generator_map = validate_generator_map(input_map["input_map"])
	if(tile_size == None or generator_map == None):
		if(tile_size == None):
			print("tile_width or tile_height parameter invalid or not found in json file.")
		if(generator_map == None):
			print("input_map parameter invalid or not found in json file.")
		return
	#Process files and save
	result = create_autotile(generator_map, tile_size, source, autocomplete)
	if(result != None):
		try:
			result.save(dest_path)
		except (ValueError, IOError, SystemError) as err:
			print("Unable to save file: " + str(dest_path) + "\nCheck tile_size in input map. Tile size: " + str(tile_size) + "\n" + str(err))

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
	print("\t python -m autotile_generator -s \"jungle.png\"")
	print("\t python -m autotile_generator -s \"cave.png\" -d \"cave_autotile.png\"")
	print("\t python -m autotile_generator -s \"../input images/ice.png\" -i \"../input maps/seven tile map.json\" -d \"../autotiles/ice_autotile.png\"")
	print("Don't forget to use Quotation marks around your paths for space filename support.")
	print("Command list:")
	print("-s --input: The input image, if not found looks for template.png in the same directory.")
	print("-i --input_map: The input mapping, if not found looks for default_input_map.json in the same directory.")
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
		result = read_command(COMMAND_SOURCE, sys.argv)
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
		destination_path = re.sub(r'(.jpg|.png|.tiff|.tif|.gif)$', '', input_path, re.IGNORECASE) + DEFAULT_DEST_SUFFIX
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