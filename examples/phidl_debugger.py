''' Debugging with non-Klayout layout programs

    First start a klayout application instance. Run the lyIPC.

    Then run this from command line with "python debug_phidl.py"

    Note that klayout can also run this file just fine.
'''
try:
    import lyipc
except ImportError:
    print('Warning: lyipc is not installed on your PYTHONPATH.')
    print('Continuing with relative path for now...\n' + '-' * 50)
    import sys
    from os.path import join, dirname
    sys.path.append(join(dirname(__file__), '..', 'python'))

import phidl
import lyipc.client as ipc
import os
import time

# Define layouts, layers, cell
TOP = phidl.Device('TOP')
somelayer = phidl.Layer(1)




### Basic lyipc usage ###

gdsname = os.path.realpath('box.gds')

# Create and place a rectangle
box = phidl.geometry.rectangle(size=(20, 20), layer=somelayer)
box_ref = TOP.add_ref(box)

# Write and tell Klayout GUI to open the file
TOP.write_gds(gdsname)
ipc.load(gdsname)


### Using python debugger and quick plot function ###

from lyipc import kqp

origin = (0, 0)
turn = 0
for i in range(19):
    if i == 5:
        import pdb; pdb.set_trace()
        # Path 1: let the debugger continue
        # Path 2: execute "turn = 20" in debugger, then continue

    width = 40 - 2 * i
    box2 = phidl.geometry.rectangle(size=(width, width), layer=somelayer)
    box2.xmin, box2.ymin = origin
    TOP.add_ref(box2)
    origin = (box2.xmax - turn, box2.ymax)

    kqp(TOP, fresh=True)
