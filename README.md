Simple (and crude) map visualizer for [TinTin++](https://tintin.mudhalla.net/) map files.

This script will iterate through the map file, and map the connections between the rooms. If any rooms are not found to be connected by any path to room 1, their vnums will be printed on the console.

Currently supports up/down/north/south/west/east directions.

The map created is 2D, and room 1 is set as coordinate 0,0,0. Maps on different levels on the Z-axis are superimposed one on top of the other, but slightly offset diagonally, and differently colored.

```
usage: map_parser_2d.py [-h] [--map_file MAP_FILE] [--output_file OUTPUT_FILE]
                        [--no_nums | --no-no_nums | -n]

options:
  --map_file MAP_FILE, -m MAP_FILE
  --output_file OUTPUT_FILE, -o OUTPUT_FILE
    # if none is provided, the map will be saved as 'map.png'
  --no_nums, --no-no_nums, -n
    # Only add room names to the map, not vnums
```
Example:
```
$ python3 ./map_parser_2d.py -m arctic_map  -n -o arctic.png
Unconnected rooms:
[]
Plotting connections
Plotting rooms
Adding room names
```

![output example](https://github.com/mantzoun/tt_map_visualizer/blob/master/example.png?raw=true)
