# AutoTile Generator

This is a 3x3 autotile tilemap generator using only 5 tiles.

From this:  
![template](https://i.imgur.com/QiyhVhm.png)  
To this:  
![result](https://i.imgur.com/PbmxC9j.png)

Or from this:  
![template](https://i.imgur.com/bgRyd6l.png)  
To this:  
![result](https://i.imgur.com/3mxv01p.png)

The generator automatically detects template rows as variations and generate another set of tiles in the same result

## Requirements
* [Python 3.x](https://www.python.org/downloads/)
* [Python Pillow library](https://pillow.readthedocs.io/en/5.1.x/installation.html) (pip install pillow)

## Usage

Before you do anything you need to setup your art, the template is actually 20 tiles, but it's essentially the same amount of effort as making 5 tiles variants as long as you keep in mind that the tiles need to be cut into quarters easily. The structure of the minitile sprite is seamless-fill, corners/single, vertical, horizontal and inner-corners. You can typically create the seamless fill tile and modify it for the other variants.

Open a console inside the directory and run the `autotile_generator.py` python script with this format `python autotile_generator.py input_image.png output_image.png` where output_image.png is optional.

Example:
`python autotile_generator.py template.png result.png`

**Usage in Godot**

Add the generated autotile tileset sprite to your tileset scene, export it, and enable autotiling in the resource. Now open the template tileset in the inspector, look for the autotile tab and create the bitmask. Also you need to set the tile size in the autotile panel, the spacing to 0, and the bitmask mode to 3x3. 
Here is an Reference for the bitmask:
![bitmask reference](https://i.imgur.com/8Ogwgnf.png)
More Info about autotileset creation in this video form HeartBeast: https://www.youtube.com/watch?v=uV5WKocIycY

### license
CC-0

Based in https://github.com/lunarfyre7/GodotAutotileAssembler/ from https://github.com/lunarfyre7

Main Differences:
* Doesn't require Gimp
* Instant tile generation
* Variation Support
