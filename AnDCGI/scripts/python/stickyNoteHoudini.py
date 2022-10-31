# © 2021 AnD CGI This work is licensed under a Creative Commons
# Attribution-ShareAlike 4.0 International License.
import hou  # Importing The Main Maya Python Module

obj = hou.node("/obj")  # Getting In To Object Context
# Creating The Sticky Note

# The Text That Will be Inside The Sticky Note
theText = '''Please Read This The ABC Shot Builder Tool Import All Latest
 Caches From Proper Directory & Creates The Files Also Assinging A Null Node
 To Each File. Since The Update Tool Isn\'t Ready Yet, Its A Suggestion To Use
 Object Merge Everywhere. So If There Is Any Cache Update You Can Manually
 Replace The Caches & The File Will Work Just Fine'''
# This Creates The Sticky Note
note = obj.createStickyNote()

# Customizing Some Aspects Of The Sticky note
note.setName('note_name')
note.setSize([2, 3])
note.setPosition([-5, -2])
note.setText(theText)
note.setTextSize(0.15)
note.setColor(hou.Color(0.635, 0.8, 0.215))
note.setTextColor(hou.Color(0, 0, 0))
