import hou

def callPipeIn():
    sel = hou.selectedNodes()
    if len(sel) == 1: 
        currentPath = sel[0].parent()
        objectPath = sel[0].path()
        chainTopName = hou.node(objectPath).inputAncestors()
        if len(chainTopName) == 0:
            chainTopName = sel[0].name()
        else:
            chainTopName = chainTopName[-1]
        if hou.node(objectPath).type() == hou.nodeType(hou.sopNodeTypeCategory(), "null"):
            hou.node(objectPath).setName("OUT_" + str(chainTopName).upper(), unique_name=True)
            sel[0].setColor(hou.Color(0.16078, 0.19608, 0.25490))     # Gunmetal Color 
        else:
            null = currentPath.createNode("null")
            null.setName("OUT_" + str(chainTopName).upper(), unique_name=True)
            null.setColor(hou.Color(0.16078, 0.19608, 0.25490))     # Gunmetal Color
            null.setInput(0, sel[0], 0)
            null.setPosition(sel[0].position() + hou.Vector2(0,-1))
            null.setSelected(True, clear_all_selected=True)
        currentSelection = hou.selectedNodes()
        updatedPath = currentSelection[0].parent()
        newObjectPath = currentSelection[0].path()
        nodePos = currentSelection[0].position() + hou.Vector2(0,-1)
        objMerge = updatedPath.createNode("object_merge")
        csn = currentSelection[0].name()
        csn = csn[4:]
        objMerge.setName("PIPE_IN_" + csn, unique_name=True)
        objMerge.setColor(hou.Color((0.93333, 0.42353, 0.30196)))      # Burnt Sienna Color
        objMerge.setPosition(nodePos)
        objMerge.setUserData("nodeshape", "chevron_down")  
        objMerge.parm("objpath1").set(newObjectPath)
        objMerge.parm("xformtype").set(1)
    else:
        hou.ui.displayMessage("Select A Node, Before Proceeding", buttons=('Cool',))
