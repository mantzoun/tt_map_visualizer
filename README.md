Simple (and crude) map visualizer for [TinTin++](https://tintin.mudhalla.net/) map files.

This script will iterate through the map file, and map the connections between the rooms. If any rooms are not found to be connected by any path to room 1, their vnums will be printed on the console.

Currently supports up/down/north/south/west/east directions.

The map created is 2D, and room 1 is set as coordinate 0,0,0. Maps on different levels on the Z-axis are superimposed one on top of the other, but slightly offset diagonally, and differently colored.

usage: map\_parser\_2d.py [-h] [--map_file MAP_FILE] [--output\_file OUTPUT\_FILE]
                        [--no_nums | --no-no_nums | -n]

options:
  --map\_file MAP\_FILE, -m MAP\_FILE
  --output\_file OUTPUT\_FILE, -o OUTPUT\_FILE
    # if none is provided, the map will be saved as 'map.png'
  --no\_nums, --no-no\_nums, -n
    # Only add room names to the map, not vnums

Example:
```
$ python3 ./map\_parser\_2d.py -m arctic\_map  -n -o arctic.png
Unconnected rooms:
[]
Plotting connections
Plotting rooms
Adding room names
```

![output example](https://github.com/mantzoun/tt_map_visualizer/blob/master/example.png?raw=true)
