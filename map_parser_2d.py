import re
import os
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Visualize a tintin++ map file')
parser.add_argument("--map_file", '-m')
parser.add_argument("--output_file", '-o')
parser.add_argument("--no_nums", '-n', action=argparse.BooleanOptionalAction)

args = parser.parse_args()

map_file = args.map_file

if args.output_file is None:
    output_file = "map.png"
else:
    output_file = args.output_file

mpl.use('Agg')

class Map:
    def __init__(self):
        self.x = {}
        self.y = {}
        self.z = {}

        self.x_inv = {}
        self.y_inv = {}
        self.z_inv = {}
        self.invis = []
        self.names = {}
        self.connections = []

mp = Map()
mp.x["1"] = 0
mp.y["1"] = 0
mp.z["1"] = 0

def conv_3d_2d(x, y, z):
    mult = 10
    offs = 2

    return x * mult - z * offs, y * mult + z * offs

def single_pass(map_data, mp):
    skipped = []
    new_data = []

    vnum = ""
    name = ""

    for line in map_data:
        elems = re.split('{|}| ', line)

        if re.search("^R", line):
            vnum = elems[2]
            name = elems[8]

            if name != "":
                mp.names[vnum] = name
            else:
                if not args.no_nums:
                    mp.names[vnum] = vnum

            if elems[4] == "4104" or elems[4] == "8":
                mp.invis.append(vnum)
            new_data.append(line)
        elif re.search("^E", line):
            exit_vnum = elems[2]
            direction = elems[4]

            if vnum not in mp.x:
                skipped.append(vnum)
                new_data.append(line)
            else:
                x_, y_, z_ = 0, 0, 0
                _x, _y, _z = mp.x[vnum], mp.y[vnum], mp.z[vnum]

                if exit_vnum in mp.x:
                    x_ = mp.x[exit_vnum]
                    y_ = mp.y[exit_vnum]
                    z_ = mp.z[exit_vnum]
                else:
                    x_ = _x
                    y_ = _y
                    z_ = _z

                    if direction == "n":
                        y_ += 1
                    elif direction == "s":
                        y_ -= 1
                    elif direction == "w":
                        x_ -= 1
                    elif direction == "e":
                        x_ += 1
                    elif direction == "u":
                        z_ += 1
                    elif direction == "d":
                        z_ -= 1

                    mp.x[exit_vnum] = x_
                    mp.y[exit_vnum] = y_
                    mp.z[exit_vnum] = z_

                con = ((min(x_, _x), max(x_, _x)), (min(y_, _y), max(y_, _y)), (min(z_, _z), max(z_, _z)))

                if con not in mp.connections:
                    mp.connections.append(con)

    return skipped, new_data

with open(map_file,"r") as mapfile:
    data = mapfile.read().splitlines()

last_skip = -1

while True:
    skipped, data = single_pass(data, mp)

    if len(skipped) == 0:
        break;
    elif len(skipped) == last_skip:
        print("Could not map %d rooms\n" % (last_skip))
        break
    else:
        last_skip = len(skipped)
        print("Unconnected rooms: %5d" % (last_skip) , end ="\r")

print("Unconnected rooms:      ")
print(skipped)

fig = plt
fig.figure(0)
fig.figure(figsize=(75, 75))

print("Plotting connections")
for con in mp.connections:
    x_ = con[0][0]
    _x = con[0][1]
    y_ = con[1][0]
    _y = con[1][1]
    z_ = con[2][0]
    _z = con[2][1]

    if min(z_, _z) % 3 == 0:
        color = 'b'
    elif min(z_, _z) % 3 == 1:
        color = 'g'
    else:
        color = 'r'
    x2d, y2d = conv_3d_2d(_x, _y, _z)
    x2d_, y2d_ = conv_3d_2d(x_, y_, z_)
    fig.plot([x2d, x2d_], [y2d, y2d_], color)

print("Plotting rooms")
for room in mp.x.keys():
    if room not in mp.invis:
        x_, y_ = conv_3d_2d(mp.x[room], mp.y[room], mp.z[room])
        fig.scatter(x_, y_, s=15, c='k')

print("Adding room names")
for room in mp.names.keys():
    if room not in mp.invis:
        x_, y_ = conv_3d_2d(mp.x[room], mp.y[room], mp.z[room])
        fig.text(x_, y_, mp.names[room])

fig.savefig(output_file)