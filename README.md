# shoveltest
Create grids to facilitate shovel tests for archaeology site work.

This repository contains an ESRI ArcGIS Python Toolbox that 
I wrote in response to a request for help on ESRI's geonet site.

The posting is here: 
https://geonet.esri.com/message/707096-re-creating-a-shovel-test-grid-for-cultural-resource-management?commentID=707096&et=watches.email.thread#comment-707096

If you want more information contact me, Brian Wilson <brian@wildsong.biz>

## Suggested work flow

1 Open a map in ArcMap with local coordinate system in feet, (not degrees).
2 Create a line to define the origin (1,1) and direction of the Y-axis.
3 Select a template polygon feature class to define extent.
4 Run the tool to generate the grid in both point and polygon format.
The tool will create an attribute file with labels (X,Y) starting at (1,1).
5 Add the feature classes to the map.
6 If you need to tweak locations you can do that now; move, add or delete
  points and edit the labels in attribute data. The labels will be exported
  to the GPX file so you can see them on the GPS screen.
7 Use the "Project" tool to reproject the points to WGS84
8 Export the reprojected WGS84 points to a GPX file for field use.


In step 2, I assume you draw a line starting at point (1,1) and going
up in the direction of "Y". That direction does not have to be
"North".  The grid tool (step 4) works "up" and to the right
generating 50' squares until it hits the edges of the template. It
will generate complete grid squares only, and the corners that are
OUTSIDE your polygon template will not generate points.

Notes
* The template polygon feature class will have just one polygon. (The grid tool only reads the first one if there is more than one.)
* This assumes your GPS unit accepts a GPX file in WGS84 format.

## Working with Github

You have the option of using ZIP to simply download a complete archive
of this project. The ZIP will be a snapshot of the latest code.

### Zip download

To use a zip download, you'd click the "Clone or download" tab and
then click "Download ZIP". Then you would unzip the downloaded file.

If later on you want a newer version, you'd repeat the same
download/unpack steps.

### Git clone

Instead of downloading zip files, you can take advantage of the power
of git version control by installing a git client on your computer.  Then
when updates are available you can just issue a 'git pull' from your
computer and only the changes will be downloaded.

I normally use the generic command line git
tools. https://git-for-windows.github.io/ A GUI tool that seems good
is "git kraken" https://www.gitkraken.com/ but I have not used it much
yet.

As an end user of github you only need two commands: "git clone" and
"git update". The first time you want to download code, you use "git
clone" followed by the URL copied from the Github web site. This
creates a new folder with everything in it; nothing to unpack. Later
on you can "chdir" into the same folder and issue "git pull" to get
any changes.

## Python code overview

This project is designed so that you can either run the grid generator
"shoveltest.py" directly from the command line or you can use it in
ArcMap as a tool.

**grid_toolbox.pyt** is the Python toolbox. This code that glues my
code to ArcGIS. Currently this toolbox contains just one tool,
shoveltesttool.py.

Running "python grid_toolbox.pyt" from the command line lists out what
it knows about its tools.

**shoveltesttool.py** is a class that is included from the PYT
file. It defines the parameters you see in the tool from ArcGIS and
passes data back and forth between ArcGIS and my code.

Running "python shoveltesttool.py" from the command line will help if
you are making changes and want to check for errors in your python.

**shoveltest.py** is the code that actual generates the grid feature
classes.

Running "python shoveltest.py" from the command line with no
additional arguments will give you information on how to use it in
standalone mode.

The current version takes the baseline and template polygon feature
classes and generates output polygon and point feature classes. It can
optionally take grid dimensions (width and height). These default to
50 x 50 map units, which means the map should be in some reasonable
projection either meters or feet.  A grid square of 50 degrees lon and
50 degrees lat will not be useful!

## Other files

Included in this repo are some test files used in development.

***test.sh*** is an example of how to run shoveltest.py from a bash script.
If you install "git for windows" it comes along with a bash shell.

***testspace.gdb*** is a geodatabase with sample baseline, polygon, and
generated grid poly and point feature classes.

***testmap.mxd*** is a sample 10.5.1 MXD based on testspace.gdb.

### Python development note

During development, I run shoveltest.py from the command line because
it eliminates interactions with ArcMap or ArcCatalog. I can make a
change in the code and run the tool again immediately; I am only
testing my code in isolation and not all the toolbox code.

When I am testing from ArcMap, when I make changes in the .py files I
have to remove the *.pyc files, do "refresh" etc to get my changes to
show up in ArcMap. If you make edits to the py files, be aware of this
issue.

