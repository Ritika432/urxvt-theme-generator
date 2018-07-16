import os
import click

from blendit import blendit
from settings import *

@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--wr", is_flag=True, help="only write to Xresources")
@click.option("--wall", is_flag=True, help="set the file as wallpaper")

def cli(filename,wr,wall):
    """ change color scheme of urxvt terminal according to wallpaper """

    argb, argbi = blendit.calculate(filename)

    print("Average color : ", argb)
    print("Invert of average color : ", argbi)

    if wr:
        if os.path.exists(XRS):
            with open(XRS, "r+") as xr:
                xr.seek(0)
                content = xr.read().split("\n")
                for x in content:
                    if "*.background" in x:
                        content[content.index(x)] = "*.background:  {}".format(argb)
                    if "*.foreground" in x:
                        content[content.index(x)] = "*.foreground:  {}".format(argbi)

                xr.seek(0)
                xr.write("\n".join(content))
            os.system("xrdb {}".format(XRS))
        else:
            click.echo("Invalid path to Xresources file.")
              
    if wall:
        os.system("feh --bg-fill {}".format(filename))
