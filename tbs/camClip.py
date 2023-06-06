import hou

def cameraClip():
    obj = hou.node('obj/')
    camFrustum = obj.createNode("geo", "camFrustum")

    # Hiding Interface
    camFrustumTG = camFrustum.parmTemplateGroup()
    camFrustumTG.hideFolder("Transform",True)
    camFrustumTG.hideFolder("Render",True)
    camFrustumTG.hideFolder("Misc",True)
    camFrustumTG.hideFolder("Arnold",True)

    customParams = [hou.FloatParmTemplate("zDist", "Far Clipping Distance", 1, min = 0.0, min_is_strict = True),
    hou.StringParmTemplate("scnCam", "Selected Camera", 1, string_type=hou.stringParmType.NodeReference),
    hou.StringParmTemplate("clipGeo", "Objects For Clipping", 1, string_type=hou.stringParmType.NodeReference)]
    for i in customParams:
        camFrustumTG.append(i)
    # Declaring Some Channel Referece Which Will Be Used Later On
    expCam = '`chsop("../../scnCam")`'
    expObj ='`chsop("../clipGeo")`'

    # Setting Template
    camFrustum.setParmTemplateGroup(camFrustumTG)

    # Creating All The Nodes & Set Parameters
    boxNode = camFrustum.createNode("box", "frustomBox")
    boxNode.setParms({"tx":0.5, "ty":0.5, "tz":-0.5})
    transfNode = camFrustum.createNode("xform", "frustomScale")
    atrbVpNode = camFrustum.createNode("attribvop", "NDC_To_Camera")

    # Create Nodes Inside VOP & Connect Them
    VOPGlobalInput = atrbVpNode.node('geometryvopglobal1')
    VOPGlobalOutput = atrbVpNode.node('geometryvopoutput1')
    frmNDC = atrbVpNode.createNode("fromndcgeo")
    frmNDC.setParms({"camera":expCam})
    frmNDC.setInput(0,VOPGlobalInput,0)
    VOPGlobalOutput.setInput(0,frmNDC,0)
    atrbVpNode.layoutChildren()

    # Continue Creating More Nodes & Set Parameters
    grpNode = camFrustum.createNode("groupcreate", "insideCameraFrustom_GRP")
    grpNode.setParms({"groupname":"frustomGRP", "grouptype":1,"groupbase":0,"groupbounding":1,"boundtype":2})
    objMerNode = camFrustum.createNode("object_merge", "objectForCameraClipping")
    objMerNode.setParms({"xformtype":1,"objpath1":expObj})
    cnvrtNode = camFrustum.createNode("convert", "convertToPolygon")
    nullNode = camFrustum.createNode("null", "OUT")
    nullNode.setDisplayFlag(True)
    nullNode.setRenderFlag(True)

    # Connect All Nodes
    cnvrtNode.setInput(0,objMerNode,0)
    transfNode.setInput(0,boxNode,0)
    atrbVpNode.setInput(0,transfNode,0)
    grpNode.setInput(0,cnvrtNode,0)
    grpNode.setInput(1,atrbVpNode,0)
    nullNode.setInput(0,grpNode,0)
    camFrustum.layoutChildren()
