# shoveltest
Create grids to facilitate shovel tests for archaeology site work.

This repository contains an ESRI ArcGIS Python Toolbox that 
I wrote in response to a request for help on ESRI's geonet site.

The posting is here: 
https://geonet.esri.com/message/707096-re-creating-a-shovel-test-grid-for-cultural-resource-management?commentID=707096&et=watches.email.thread#comment-707096

If you want more information contact me, Brian Wilson <brian@wildsong.biz>

## Suggested work flow

Working in a map with local coordinate system in FEET, 
1 Create a line to define the origin (1,1) and direction of the Y-axis.
2 Select a template polygon feature class to define extent.
3 Run tool to generate grid.
4 If you need to tweak the grid, do that now using ArcGIS edit tools.
5 Run tool to convert grid to points; the tool will also label
  points (X,Y) starting at (1,1) by default.
6 If you need to tweak any POINTS you can do that now; move, add or delete
  points and edit the labels in attribute data. The labels will be exported
  to the GPX file so you can see them on the GPS screen.
7 Use tool to reproject to WGS84 and export to GPX file for field use.

(When I say "tool" here I mean some operation that might be a piece of python or a model or a generic ESRI tool
for the purposes of discussion assume it exists.)

In step 1 I assume you draw a line starting at point (1,1) and going up in the direction of "Y" 
and that direction is not "North" Then the tool in step 3 works "up" and to the right generating 50' squares
until it hits the edge of the template. It will generate complete squares only, corners OUTSIDE the template
will not generate points.

My assumptions so far: 
* The template polygon feature class will have just one polygon in it
* Each intersection is the location of shovel test. Using centroids is
  a great way to use Fishnet but will create confusion when visualizing 
  the fishnet grid. The grid-to-point tool (step 5) will deal with corners.
* Your GPS unit can accept a GPX file.




