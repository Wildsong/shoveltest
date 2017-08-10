# shoveltesttool.py
# Copyright (c)2017 Brian Wilson <brian@wildsong.biz>
#
from __future__ import print_function
import arcpy
from shoveltest import makegrid

class ShovelTest_Tool(object):
    """This class has the methods you need to define
       to use your code as an ArcGIS Python Tool."""
        
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Make Shovel Test Grid"
        self.description = """Makes a shovel test grid."""
        self.canRunInBackground = False
        self.category = "Wildsong" # Use your own category here, or an existing one.
        #self.stylesheet = "" # I don't know how to use this yet.
        
    def getParameterInfo(self):
        """Define parameter definitions
           Refer to http://resources.arcgis.com/en/help/main/10.2/index.html#/Defining_parameters_in_a_Python_toolbox/001500000028000000/
           For datatype see http://resources.arcgis.com/en/help/main/10.2/index.html#/Defining_parameter_data_types_in_a_Python_toolbox/001500000035000000/
        """
        
        params = []
    
        baseline_fc = arcpy.Parameter(name="baseline",
                                      displayName="Baseline Feature Class",
                                      datatype="DEFeatureClass",
                                      parameterType="Required", # Required|Optional|Derived
                                      direction="Input", # Input|Output
                                )
        baseline_fc.filter.list = ["Polyline"]
        baseline_fc.value = "testspace.gdb/baseline" # default
        params.append(baseline_fc)
        
        template_fc = arcpy.Parameter(name="template",
                                      displayName="Template Feature Class",
                                      datatype="DEFeatureClass",
                                      parameterType="Required", # Required|Optional|Derived
                                      direction="Input", # Input|Output
                                )
        template_fc.filter.list = ["Polygon"]
        template_fc.value = "testspace.gdb/template" # default
        params.append(template_fc)

        output_workspace = arcpy.Parameter(name="output_workspace",
                                           displayName="Output workspace",
                                           datatype="DEWorkspace",
                                           parameterType="Required", # Required|Optional|Derived
                                           direction="Input", # Input|Output
                                )
        #output_fc.parameterDependencies = []
        output_workspace.value = "testspace.gdb" # default
        params.append(output_workspace)

        output_poly = arcpy.Parameter(name="output_polygon_features",
                                      displayName="Output polygon feature class",
                                      datatype="GPString",
                                      parameterType="Required", # Required|Optional|Derived
                                      direction="Input", # Input|Output
                                )
        output_poly.value = "grid_poly"
        params.append(output_poly)

        output_point = arcpy.Parameter(name="output_point_features",
                                       displayName="Output point feature class",
                                       datatype="GPString",
                                       parameterType="Required", # Required|Optional|Derived
                                       direction="Input", # Input|Output
                                )
        output_point.value = "grid_point"
        params.append(output_point)

        width = arcpy.Parameter(name="grid_cell_width",
                                displayName="Width of a grid cell",
                                datatype="GPDouble",
                                parameterType="Required", # Required|Optional|Derived
                                direction="Input", # Input|Output
                                )
        width.value = "50"
        params.append(width)

        height = arcpy.Parameter(name="grid_cell_height",
                                 displayName="Height of a grid cell",
                                 datatype="GPDouble",
                                 parameterType="Required", # Required|Optional|Derived
                                 direction="Input", # Input|Output
                                )
        height.value = "50"
        params.append(height)

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of your tool."""
        
        # Let's dump out what we know here.
        for param in parameters:
            messages.AddMessage("Parameter: %s = %s" % (param.name, param.valueAsText) )
        
        baseline_fc  = parameters[0].valueAsText
        template_fc  = parameters[1].valueAsText
        workspace    = parameters[2].valueAsText
        output_poly  = parameters[3].valueAsText
        output_point = parameters[4].valueAsText
        width        = parameters[5].valueAsText
        height       = parameters[6].valueAsText
        
        # Okay, finally go ahead and do the work.
        makegrid(baseline_fc, template_fc, workspace, output_poly, output_point, width, height)
        return

if __name__ == "__main__":
    # Run me from the command line to find typos!
    foo = ShovelTest_Tool()
    foo.getParameterInfo()
    foo.execute()
# That's all!
