#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymxs import runtime as rt
from PySide2 import QtWidgets, QtCore, QtGui
import gc  # Import garbage collector

from JalLib.max.header import Header

jal = Header()

class HelperTypeSelDialog(QtWidgets.QDialog):
    def __init__(self, parent=QtWidgets.QWidget.find(rt.windows.getMAXHWND())):
        super(HelperTypeSelDialog, self).__init__(parent)
        
        self.selectedHelperType = ""
        self.changeHelperType = False
        
        self.setWindowTitle("Helper Type")
        self.setMinimumWidth(100)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.helper_type_combo = QtWidgets.QComboBox(self)
        typeNamePart = jal.name.get_name_part("Type")
        typeNameDescriptions = typeNamePart.get_descriptions()
        self.helper_type_combo.addItems(typeNameDescriptions)
        self.layout.addWidget(self.helper_type_combo)

        self.ok_button = QtWidgets.QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)
        
        self.ok_button.clicked.connect(self.ok_pressed)
    
    def ok_pressed(self):
        selHelperDescription = self.helper_type_combo.currentText()
        typeNamePart = jal.name.get_name_part("Type")
        self.selectedHelperType = typeNamePart.get_value_by_description(selHelperDescription)
        self.changeHelperType = True
        self.accept()

def jal_create_parentHelper():
    jal.helper.create_parent_helper()

def jal_create_helper():
    dialog = HelperTypeSelDialog()
    result = dialog.exec_()
    changeHelperType = dialog.changeHelperType
    if changeHelperType:
        helperType = dialog.selectedHelperType
        genHelpers = jal.helper.create_helper()
        for item in genHelpers:
            item.name = jal.name.replace_name_part(item.name, "Type", helperType)
        
    dialog.deleteLater()
    dialog = None  # Clear the reference to the dialog object
    gc.collect()  # Force garbage collection to free up memory
    

def jal_create_average_helper():
    sel_array = rt.getCurrentSelection()
    
    if len(sel_array) > 0:
        temp_transform = rt.matrix3(1)
        temp_transform.rotation = jal.anim.create_average_rot_transform(sel_array).rotation
        temp_transform.position = jal.anim.create_average_pos_transform(sel_array).position
        
        dum_name = jal.helper.gen_helper_name_from_obj(sel_array[0])
        dum_shape = jal.helper.gen_helper_shape_from_obj(sel_array[0])
        average_dum = jal.helper.create_point(
            dum_name[0], 
            size=dum_shape[0],
            boxToggle=dum_shape[2],
            crossToggle=dum_shape[1]
        )
        average_dum.transform = temp_transform

def jal_create_pos_average_helper():
    sel_array = rt.getCurrentSelection()
    
    if len(sel_array) > 0:
        temp_transform = rt.matrix3(1)
        temp_transform.position = jal.anim.create_average_pos_transform(sel_array).position
        
        dum_name = jal.helper.gen_helper_name_from_obj(sel_array[0])
        dum_shape = jal.helper.gen_helper_shape_from_obj(sel_array[0])
        average_dum = jal.helper.create_point(
            dum_name[0], 
            size=dum_shape[0],
            boxToggle=dum_shape[2],
            crossToggle=dum_shape[1]
        )
        average_dum.transform = temp_transform
        average_dum.name = jal.name.replace_name_part(average_dum.name, "Type", "Pos")

def jal_create_rot_average_helper():
    sel_array = rt.getCurrentSelection()
    
    if len(sel_array) > 0:
        temp_transform = rt.matrix3(1)
        temp_transform.rotation = jal.anim.create_average_rot_transform(sel_array).rotation
        
        dum_name = jal.helper.gen_helper_name_from_obj(sel_array[0])
        dum_shape = jal.helper.gen_helper_shape_from_obj(sel_array[0])
        average_dum = jal.helper.create_point(
            dum_name[0], 
            size=dum_shape[0],
            boxToggle=dum_shape[2],
            crossToggle=dum_shape[1]
        )
        average_dum.transform = temp_transform
        average_dum.name = jal.name.replace_name_part(average_dum.name, "Type", "Rot")

def jal_create_expHelper():
    jal.helper.create_exp_tm()

def jal_create_two_helper():
    dialog = HelperTypeSelDialog()
    result = dialog.exec_()
    helperType = dialog.selectedHelperType
    genHelpers = jal.helper.create_helper(make_two=True)
    for item in genHelpers:
        item.name = jal.name.replace_name_part(item.name, "Type", helperType)
        
    dialog.deleteLater()
    dialog = None  # Clear the reference to the dialog object
    gc.collect()  # Force garbage collection to free up memory

def jal_modify_helperShape():
    pass

# Register macroscripts
macroScript_Category = "jalTools"

'''
rt.jal_create_parentHelper = jal_create_parentHelper
rt.macros.new(
    macroScript_Category,
    "jal_create_parentHelper",
    "create Parent Helper",
    "jal_create_parentHelper",
    "jal_create_parentHelper()"
)

rt.jal_create_helper = jal_create_helper
rt.macros.new(
    macroScript_Category,
    "jal_create_helper",
    "create Helper",
    "jal_create_helper",
    "jal_create_helper()"
)

rt.jal_create_average_helper = jal_create_average_helper
rt.macros.new(
    macroScript_Category,
    "jal_create_average_helper",
    "create Average Helper",
    "jal_create_average_helper",
    "jal_create_average_helper()"
)

rt.jal_create_pos_average_helper = jal_create_pos_average_helper
rt.macros.new(
    macroScript_Category,
    "jal_create_pos_average_helper",
    "create Pos avrg. Helper",
    "jal_create_pos_average_helper",
    "jal_create_pos_average_helper()"
)

rt.jal_create_rot_average_helper = jal_create_rot_average_helper
rt.macros.new(
    macroScript_Category,
    "jal_create_rot_average_helper",
    "create Rot avrg. Helper",
    "jal_create_rot_average_helper",
    "jal_create_rot_average_helper()"
)

rt.jal_create_expHelper = jal_create_expHelper
rt.macros.new(
    macroScript_Category,
    "jal_create_expHelper",
    "create Exp Helper",
    "jal_create_expHelper",
    "jal_create_expHelper()"
)

rt.jal_create_two_helper = jal_create_two_helper
rt.macros.new(
    macroScript_Category,
    "jal_create_two_helper",
    "create Two Helper",
    "jal_create_two_helper",
    "jal_create_two_helper()"
)

rt.jal_modify_helperShape = jal_modify_helperShape
rt.macros.new(
    macroScript_Category,
    "jal_modify_helperShape",
    "modify Helper shape",
    "jal_modify_helperShape",
    "jal_modify_helperShape()"
)
'''
# jal_create_two_helper()
jal_create_helper()
