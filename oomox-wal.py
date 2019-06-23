#!/usr/bin/env python3.6

"""\
oomox-wal
Generate oomox theme based on pywal colours

Usage:
  oomox-wal [-f] <name>
  oomox-wal -h

Options:
  -f --force       Overwrite theme if it exists.
"""

import sys
import subprocess
import os
from docopt import docopt

from base import base

def get_Xcolours():
    p = subprocess.Popen(["xrdb","-query"],stdout=subprocess.PIPE)
    Xvars,err = p.communicate()
    Xvars = Xvars.decode("ascii")
    Xvars = dict([keypair.strip("*").split("\t") for keypair in Xvars.replace(":","").strip("\n").split("\n") if keypair[0] == "*"])

    COLORS = {"color0":Xvars[".color0"],
              "color1":Xvars[".color1"],
              "color2":Xvars[".color2"],
              "color3":Xvars[".color3"],
              "color4":Xvars[".color4"],
              "color5":Xvars[".color5"],
              "color6":Xvars[".color6"],
              "color7":Xvars[".color7"],
              "color8":Xvars[".color8"],
              "color9":Xvars[".color9"],
              "color10":Xvars[".color10"],
              "color11":Xvars[".color11"],
              "color12":Xvars[".color12"],
              "color13":Xvars[".color13"],
              "color14":Xvars[".color14"],
              "color15":Xvars[".color15"],
              "background":Xvars[".background"],
              "foreground":Xvars[".foreground"]}
    return COLORS

def make_theme(name, oomox_dir="~/.config/oomox/colors", overwrite=False):
    oomox_dir = os.path.expanduser(oomox_dir)
    theme_path = os.path.join(oomox_dir, os.path.basename(name))

    xvals = get_Xcolours()
    
    theme = base
    for key, val in xvals.items():
        val = val.replace("#","")
        if key[:-1] == "color":
            theme = theme.replace("c#"+str(key[5:]), val)
        elif key == "background":
            theme = theme.replace("bg", val)
        elif key == "foreground":
            theme = theme.replace("fg", val)

    if os.path.exists(theme_path) and not overwrite:
        print("Theme already exists. Use -f to force overwrite.")
        return

    with open(theme_path, "w") as f:
        f.write(theme)

    print("Done!")

if __name__ == "__main__":
    args = docopt(__doc__)

    make_theme(args["<name>"], overwrite=args["--force"])
    
