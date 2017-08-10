# shoveltest.py
# Copyright (c)2017 Brian Wilson <brian@wildsong.biz>
#
from __future__ import print_function
import arcpy
import os, sys
import math

# You can run this script from the command line, if you want.

def usage():
    print("""usage: shoveltest.py baselinefc templatefc outputpoly outputpt [width height]

Generates polygon and point feature classes in a grid, to facilitate archaeology shovel tests.

baselinefc    A polyline feature class containing one line defining the yaxis of the grid
templatefc    A polygon feature class containing one polygon that defines the area the grid will cover
outputpoly    A feature class that will be OVERWRITTEN with the polygons generated
outputpt      A feature class that will be OVERWRITTEN with the points generated
width height  Width and height of grid squares in map units. Optional, defaults to 50,50
""")

# ------------------------------------------------------------------------

def findtheta(p0, p1):
    """ Find the angle in radians of the this line """
    return math.atan2( p1.X - p0.X, p1.Y - p0.Y )

def affine(p, scale, theta, offset):
    """ Scale, rotate and translate point """
    return arcpy.Point((p.X * math.cos(theta) - p.Y * math.sin(theta)) * scale.X + offset.X,
                       (p.X * math.sin(theta) + p.Y * math.cos(theta)) * scale.Y + offset.Y)

def findextent(geom, th, origin):
    # I need to rotate the template to align it with the baseline; 
    # then I can use its extent to figure out how big the grid needs to be.
    for part in geom:
        newpts = []
        for pt in part:
            x = (pt.X - origin.X)
            y = (pt.Y - origin.Y)
            x1 = (x * math.cos(th) - y * math.sin(th)) + origin.X
            y1 = (x * math.sin(th) + y * math.cos(th)) + origin.Y
            newpts.append(arcpy.Point(x1,y1))
    return arcpy.Polygon(arcpy.Array(newpts)).extent

def create_fc(fcpath, shapetype, sref):
    try:
        if arcpy.Exists(fcpath): arcpy.Delete_management(fcpath)
    except Exception as e:
        arcpy.AddError("Delete failed on \"%s\". %s" % (fcpath,e))
        return False
    template = None
    has_m = has_z = "DISABLED"
    (workspace, name) = os.path.split(fcpath)
    try:
        arcpy.CreateFeatureclass_management(workspace, name, shapetype, template, has_m, has_z, sref)
        arcpy.AddField_management(fcpath, "label", "TEXT", 50)
    except Exception as e:
        arcpy.AddError("Create failed for \"%s\". %s" % (fcpath,e))
        return False
    return True

# ------------------------------------------------------------------------

def makegrid(baseline, template, workspace, gridpoly, gridpt, width=50, height=50):

    # Read the baseline geometry, which defines the origin of the grid and its orientation.
    try:
        fieldnames = ["SHAPE@"]
        cursor = arcpy.da.SearchCursor(baseline, fieldnames)
        row = cursor.next()
        del cursor
        geom = row[0][0]
        origin = geom[0]
        end    = geom[1]
    except Exception as e:
        arcpy.AddError("Could not read baseline from \"%s\". %s" % (baseline, e))
        return False

    # Read the template feature class, which defines the output spatial reference,
    # and the extent of the grid that will be generated.
    try:
        # For now I assume there is only one polygon in the template
        # and that it has only one part

        desc = arcpy.Describe(template)
        sref = desc.spatialReference

        stemp = arcpy.da.SearchCursor(template, ["SHAPE@"])
        row = stemp.next()
        template_geometry = row[0] # NB we use this later to clip the output
        del row
        del stemp

    except Exception as e:
        arcpy.AddMessage("Can't read template polygon \"%s\". %s" % (template, e))
        return False

    arcpy.AddMessage("baseline origin: %d,%d end: %d,%d" % (origin.X, origin.Y, end.X, end.Y))

    theta_right = findtheta(origin,end)  # rotate RIGHT
    theta_left  = -theta_right           # rotate LEFT

    # This has to happen outside the edit session!
    pointpath = os.path.join(workspace, gridpt)
    polypath  = os.path.join(workspace, gridpoly)
    create_fc(pointpath, "POINT",   sref)
    create_fc(polypath,  "POLYGON", sref)

    # Start an edit session so we can use two InsertCursors at the same time.
    with arcpy.da.Editor(workspace) as edit:

        fieldnames = ["SHAPE@", "label"]

        scale = arcpy.Point(width, height)
        tile_count = point_count = 0
        allpoints = {} # Keep track of what points we've already written so there are no duplicates

        # Use the baseline origin as the min limit; don't use full extent
        # of template polygon, because it might extend to the left or end to the
        # right of the baseline.  If it's to the left then it gets clipped
        # off, and to the right we might generate some extra points, not a big deal.

        tmpl_ext = findextent(template_geometry, theta_right, origin)
        width  = int((abs(tmpl_ext.XMax - origin.X) + scale.X) / scale.X)
        height = int((abs(tmpl_ext.YMax - origin.Y) + scale.Y) / scale.Y)

        arcpy.AddMessage("Grid size will be (%d x %d)" % (width, height))
        if width > 500 or height > 500:
            arcpy.AddError("I won't generate that many tiles!")
            return False

        cursor_poly = arcpy.da.InsertCursor(polypath,  fieldnames)
        cursor_pt   = arcpy.da.InsertCursor(pointpath, fieldnames)

        for x in range(0, width):
            for y in range(0, height):

                # Corners in untransformed format
                corners = [ arcpy.Point(x+0, y+0), arcpy.Point(x+1, y+0),
                            arcpy.Point(x+1, y+1), arcpy.Point(x+0, y+1) ]
                polycorners = []
                clipped = False # If any corners get clipped, drop the polygon too,
                for p0 in corners:
                    p1 = affine(p0, scale, theta_left, origin)
                    polycorners.append(p1)
                    label = "%d,%d" % (p0.X+1, p0.Y+1)
                    if not label in allpoints:

                        # Check to make sure point is not clipped by template.
                        if p1.within(template_geometry, None):
                            cursor_pt.insertRow([p1, label])
                            allpoints[label] = 1
                            point_count += 1
                        else:
                            clipped = True

                if not clipped:
                    tile_label = "%d,%d" % (x,y)
                    geom = arcpy.Polygon(arcpy.Array(polycorners))
                    cursor_poly.insertRow([geom, tile_label])
                    tile_count += 1
        del cursor_pt, cursor_poly
    # Edit session ends here!
    arcpy.AddMessage("Generated %d tiles and %d shovel sites" % (tile_count, point_count))

# ------------------------------------------------------------------------

if __name__ == "__main__":

    tile_width  = 50
    tile_height = 50

    try:
        baseline  = sys.argv[1]
        template  = sys.argv[2]
        workspace = sys.argv[3]
        gridpoly  = sys.argv[4]
        gridpt    = sys.argv[5]

        if len(sys.argv[7]):
            tile_width = sys.argv[6]
            tile_height = sys.argv[7]
    except:
        usage()
        exit(1)
    
    makegrid(baseline, template, workspace, gridpoly, gridpt, tile_width, tile_height)

# That's all! 
