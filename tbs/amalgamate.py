import hou

def callMerge():
    selNodes = hou.selectedNodes()
    if len(selNodes) >= 1:
        currentPath = selNodes[0].parent()
        mergeNode = currentPath.createNode("merge")
        mergeNode.setName("MERGING_IN_" + str(len(selNodes)) + "_NODE", unique_name=True)
        mergeNode.setDisplayFlag(True)
        mergeNode.setRenderFlag(True)
        
        for i, node in enumerate(selNodes):
            mergeNode.setInput(i,node)
        
        mergeNode.setColor(hou.Color((0.23922, 0.35294, 0.50196)))      # Metallic Blue Color
        mergeNode.moveToGoodPosition()
        mergeNode.setUserData("nodeshape", "chevron_up")
        mergeNode.setSelected(True, clear_all_selected=True)

    else:
        hou.ui.displayMessage("Select At Least 1 Node")   