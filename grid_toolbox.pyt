# Python Tool box for archaeology
# Copyright (c)2017 Brian Wilson <brian@wildsong.biz>
#
import arcpy
from shoveltesttool import ShovelTest_Tool

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of this .pyt file)."""
        self.label = "Archy Toolbox"
        self.alias = ""
        self.description = """Toolbox containing a grid tool for archaeology"""

        # List of tool classes associated with this toolbox
        self.tools = [ShovelTest_Tool]

if __name__ == "__main__":
    # Running this as a standalone script tells what I know about the toolbox.

    toolbox = Toolbox()
    print "toolbox:",toolbox.label
    print "description:",toolbox.description
    print "tools:"
    for t in toolbox.tools:
        tool = t()
        print '  ',tool.label
        print '   description:', tool.description
        for param in tool.getParameterInfo():
            print '    ',param.name,':',param.displayName

    exit(0)
    
# That's all!
