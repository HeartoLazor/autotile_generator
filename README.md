# AutoTile Generator

Assemble 3x3 bitmask tileset using a smaller template.

From this:  
![template](https://i.imgur.com/QiyhVhm.png)  
To this:  
![result](https://i.imgur.com/PbmxC9j.png)

Or from this:  
![template](https://i.imgur.com/bgRyd6l.png)  
To this:  
![result](https://i.imgur.com/3mxv01p.png)

The generator is fully customizable and automatically detects template rows as variations and generate another set of tiles in the same result.

## Requirements

* [Python 3.x](https://www.python.org/downloads/)
* [Python Pillow library](https://pillow.readthedocs.io/en/5.1.x/installation.html) (pip install pillow)
* [Python jstyleson library](https://github.com/linjackson78/jstyleson) (pip install jstyleson)

## Installation

Simply run `pip install .` from the root directory to install this package, don't forget administrator privileges. Then you can invoke it anywhere like this `python -m autotile_generator -s <image>`

## Uninstall

Run with administrator privileges `pip uninstall autotile_generator`

## Usage

Before you do anything you need to setup your art, the template is actually 20 tiles, but it's essentially the same amount of effort as making 5 tiles variants as long as you keep in mind that the tiles need to be cut into quarters easily. The structure of the default template sprite is seamless-fill, corners/single, vertical, horizontal and inner-corners. You can typically create the seamless fill tile and modify it for the other variants.

Open a console and write a command like this: 
`python -m autotile_generator -s "input_image.png" -i "input_map.json" -d "output_image.png"`.

Example:

`python -m autotile_generator -s "jungle.png"`

`python -m autotile_generator -s "cave.png" -d "cave_autotile.png"`

`python -m autotile_generator -s "../input images/ice.png' -i "../input maps/seven tile map.json" -d "../autotiles/ice_autotile.png"`

Don't forget to use Quotation marks around your paths for space filename support.

### Usage in Godot

Add the generated autotile tileset sprite to your tileset scene, export it, and enable autotiling in the resource. Now open the template tileset in the inspector, look for the autotile tab and create the bitmask. Also you need to set the tile size in the autotile panel, the spacing to 0, and the bitmask mode to 3x3. 
Here is an Reference for the bitmask:
![bitmask reference](https://i.imgur.com/8Ogwgnf.png)
More Info about autotileset creation in this video form HeartBeast: https://www.youtube.com/watch?v=uV5WKocIycY

## Command list:

`-s, --source or --source_image`: The input image, if not found looks for template.png in the same directory.

Example:

`python -m autotile_generator -s "jungle.png"`

`-i --input_map`: The input mapping, if not found uses default installed map (default_input_map.json).

Example:

`python -m autotile_generator -s "../input images/ice.png' -i "../input maps/seven tile map.json" -d "../autotiles/ice_autotile.png"`

Maps input tilesets to the generated autotile result image. 

Each tile in the result map is represented by 4 values: (number_1, number_2, number_3, number_4)

Where 0 represents an empty tile and a number bigger than 0 represents the tile in input tile, for example 1is the first tile in input tile.

Tiles in result are constructed using each of the four values:
```
number_1 , number_2
number_3 , number_4
```
For example a tile represented by those values (0,1,0,1) result in:
```
top_left_corner_from_0_input_tile, top_right_corner_from_1_input_tile
bot_left_corner_from_1_input_tile, bot_right_corner_from_0_input_tile
```
The map json is composed by many tiles, for example:
```
[2,3,0,1],[3,3,1,0],[4,3,2,0]
[4,4,1,1],[2,2,4,0],[4,4,4,4]
```
Result in an autotile image with 6 tiles.

Another important value from json map is the Input Size, which is how many tiles conform the first row from input image, if last example used a input image with 4 tiles, this value should be 4. The template image uses 5 tiles.

`-d --destination`: The output image destination, if not set the output is <inputfile>_autotile.png in the same directory as the input.

Example:

`python -m autotile_generator -s "cave.png" -d "cave_autotile.png"`

`-h --help`: show help.

Example:

`python -m autotile_generator -h`

### License

MIT License

Based in https://github.com/lunarfyre7/GodotAutotileAssembler/ from https://github.com/lunarfyre7

Main Differences:
* Fully customizable (see input_map command in Command_List).
* Variation Support.
* Doesn't require Gimp.
* Instant tile generation.
