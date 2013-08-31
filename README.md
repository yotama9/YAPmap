YAPmap
======

Yet Another Python mapping program. The goal is to create an easy to use tiling map program that will have some random features. 

Description
===========

This is an attempt to make a mapping application which is easy to use for on the fly mapping. I develop this program
with role playing game mastering in mind but this mainly come to fill a gap which I believe is lacking. An important feature
of this program is the randomness of the map. The user select what kind of tiles he would like to place (river, mountains, etc.) 
and the program will place a tile which is randomly selected from its repository. The user can easily design new tiles for the program

Usage
=====
Download the files and extracted them to a folder. 

Making Maps
-----------
Launch the YAPmap.py python file. When editing a map, select a bunch of tiles, select from the first combo box the 
tile family you want to use (mountains, rivers, etc), select the tile kind (easy mounains, small rivers etc) from the second 
combo box. Click the DoIt button and the tiles will be placed on the screen 
Making Tiles
------------
Launch the tileMaker.py python file. Draw the tiles on the main drawing area (at the bottom right there is a preview for the tiles).
You can:
1. select a color to draw (including alpha channel) using the color dialog
2. Draw over tiles
3. Erase tiles
4. Draw while not overwriting over tiles

Before you close the button, choose the tile family (top combo box) and name (bottom combo box) to store the tile at. Should
you choose a new family or new tile at the combobox, a dialog will pop upp asking for a name to use. The program will let you know
if the name already exist. 
