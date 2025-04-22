#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymxs import runtime as rt

def jal_create_parentHelper():
    jal.helper.create_parent_helper()

def jal_create_helper():
    class HelperTypeRollout:
        def __init__(self):
            self.rollout = rt.dotNetObject("System.Windows.Forms.Form")
            self.rollout.Text = "Set Helper Type"
            self.rollout.Width = 250
            self.rollout.Height = 100
            self.rollout.FormBorderStyle = rt.dotNetObject("System.Windows.Forms.FormBorderStyle").FixedDialog
            self.rollout.StartPosition = rt.dotNetObject("System.Windows.Forms.FormStartPosition").CenterScreen
            
            self.helperTypeDrp = rt.dotNetObject("System.Windows.Forms.ComboBox")
            self.helperTypeDrp.DropDownStyle = rt.dotNetObject("System.Windows.Forms.ComboBoxStyle").DropDownList
            self.helperTypeDrp.Location = rt.dotNetObject("System.Drawing.Point", 10, 10)
            self.helperTypeDrp.Width = 230
            self.rollout.Controls.Add(self.helperTypeDrp)
            
            self.okBtn = rt.dotNetObject("System.Windows.Forms.Button")
            self.okBtn.Text = "OK"
            self.okBtn.Location = rt.dotNetObject("System.Drawing.Point", 85, 40)
            self.okBtn.Width = 80
            self.okBtn.Click += self.on_ok_pressed
            self.rollout.Controls.Add(self.okBtn)
            
            # Fill the dropdown with items
            for item in jal.name.__typeStrArray:
                self.helperTypeDrp.Items.Add(item)
            self.helperTypeDrp.SelectedIndex = 0
            
        def on_ok_pressed(self, sender, args):
            gen_helpers = jal.helper.create_helper()
            for item in gen_helpers:
                item.name = jal.name.replace_type(item.name, self.helperTypeDrp.Items[self.helperTypeDrp.SelectedIndex])
            self.rollout.Close()
        
        def show_dialog(self):
            self.rollout.ShowDialog()
    
    # Create and show the dialog
    dialog = HelperTypeRollout()
    dialog.show_dialog()

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
    class HelperTypeRollout:
        def __init__(self):
            self.rollout = rt.dotNetObject("System.Windows.Forms.Form")
            self.rollout.Text = "Set Helper Type"
            self.rollout.Width = 250
            self.rollout.Height = 180
            self.rollout.FormBorderStyle = rt.dotNetObject("System.Windows.Forms.FormBorderStyle").FixedDialog
            self.rollout.StartPosition = rt.dotNetObject("System.Windows.Forms.FormStartPosition").CenterScreen
            
            # Create radio buttons
            self.radio_buttons = []
            radio_labels = jal.name.__typeStrArray
            
            # Create a panel to hold the radio buttons
            panel = rt.dotNetObject("System.Windows.Forms.Panel")
            panel.Location = rt.dotNetObject("System.Drawing.Point", 10, 10)
            panel.Width = 230
            panel.Height = 120
            
            # Add radio buttons to the panel in a 2-column layout
            col_width = 115
            row_height = 25
            for i, label in enumerate(radio_labels):
                row = i // 2
                col = i % 2
                
                radio = rt.dotNetObject("System.Windows.Forms.RadioButton")
                radio.Text = label
                radio.Location = rt.dotNetObject("System.Drawing.Point", col * col_width, row * row_height)
                radio.Width = col_width
                panel.Controls.Add(radio)
                self.radio_buttons.append(radio)
            
            # Select the first radio button
            if len(self.radio_buttons) > 0:
                self.radio_buttons[0].Checked = True
            
            self.rollout.Controls.Add(panel)
            
            # Add OK button
            self.okBtn = rt.dotNetObject("System.Windows.Forms.Button")
            self.okBtn.Text = "OK"
            self.okBtn.Location = rt.dotNetObject("System.Drawing.Point", 85, 130)
            self.okBtn.Width = 80
            self.okBtn.Click += self.on_ok_pressed
            self.rollout.Controls.Add(self.okBtn)
            
        def on_ok_pressed(self, sender, args):
            selected_index = -1
            for i, radio in enumerate(self.radio_buttons):
                if radio.Checked:
                    selected_index = i
                    break
            
            if selected_index >= 0:
                gen_helpers = jal.helper.create_helper(makeTwo=True)
                type_str = jal.name.__typeStrArray[selected_index]
                for item in gen_helpers:
                    item.name = jal.name.replace_type(item.name, type_str)
            
            self.rollout.Close()
        
        def show_dialog(self):
            self.rollout.ShowDialog()
    
    # Create and show dialog
    dialog = HelperTypeRollout()
    dialog.show_dialog()

def jal_modify_helperShape():
    class HelperShapeModRollout:
        def __init__(self):
            self.rollout = rt.dotNetObject("System.Windows.Forms.Form")
            self.rollout.Text = "Modify Helper Shape"
            self.rollout.Width = 280
            self.rollout.Height = 160
            self.rollout.FormBorderStyle = rt.dotNetObject("System.Windows.Forms.FormBorderStyle").FixedDialog
            self.rollout.StartPosition = rt.dotNetObject("System.Windows.Forms.FormStartPosition").CenterScreen
            
            # Create size spinners
            # Size spinner
            self.size_spinner_label = rt.dotNetObject("System.Windows.Forms.Label")
            self.size_spinner_label.Text = "Size:"
            self.size_spinner_label.Location = rt.dotNetObject("System.Drawing.Point", 10, 15)
            self.size_spinner_label.Width = 40
            self.rollout.Controls.Add(self.size_spinner_label)
            
            self.size_spinner = rt.dotNetObject("System.Windows.Forms.NumericUpDown")
            self.size_spinner.Location = rt.dotNetObject("System.Drawing.Point", 50, 13)
            self.size_spinner.Width = 70
            self.size_spinner.Minimum = rt.dotNetObject("System.Decimal", 0.0)
            self.size_spinner.Maximum = rt.dotNetObject("System.Decimal", 100.0)
            self.size_spinner.Value = rt.dotNetObject("System.Decimal", 1.0)
            self.size_spinner.DecimalPlaces = 2
            self.size_spinner.Increment = rt.dotNetObject("System.Decimal", 0.1)
            self.size_spinner.ValueChanged += self.on_size_changed
            self.rollout.Controls.Add(self.size_spinner)
            
            # Add size spinner
            self.add_spinner_label = rt.dotNetObject("System.Windows.Forms.Label")
            self.add_spinner_label.Text = "Add:"
            self.add_spinner_label.Location = rt.dotNetObject("System.Drawing.Point", 150, 15)
            self.add_spinner_label.Width = 40
            self.rollout.Controls.Add(self.add_spinner_label)
            
            self.add_spinner = rt.dotNetObject("System.Windows.Forms.NumericUpDown")
            self.add_spinner.Location = rt.dotNetObject("System.Drawing.Point", 190, 13)
            self.add_spinner.Width = 70
            self.add_spinner.Minimum = rt.dotNetObject("System.Decimal", -100.0)
            self.add_spinner.Maximum = rt.dotNetObject("System.Decimal", 100.0)
            self.add_spinner.Value = rt.dotNetObject("System.Decimal", 0.0)
            self.add_spinner.DecimalPlaces = 2
            self.add_spinner.Increment = rt.dotNetObject("System.Decimal", 0.1)
            self.add_spinner.ValueChanged += self.on_add_size_changed
            self.add_spinner.MouseUp += self.on_add_size_reset
            self.rollout.Controls.Add(self.add_spinner)
            
            # Radio buttons for shape type
            self.shape_types = ["Box", "Cross", "Axis", "Center"]
            self.radio_buttons = []
            
            # Create a panel to hold the radio buttons
            panel = rt.dotNetObject("System.Windows.Forms.Panel")
            panel.Location = rt.dotNetObject("System.Drawing.Point", 10, 45)
            panel.Width = 260
            panel.Height = 65
            
            # Add radio buttons to the panel in a 2-column layout
            col_width = 120
            row_height = 25
            for i, label in enumerate(self.shape_types):
                row = i // 2
                col = i % 2
                
                radio = rt.dotNetObject("System.Windows.Forms.RadioButton")
                radio.Text = label
                radio.Location = rt.dotNetObject("System.Drawing.Point", col * col_width, row * row_height)
                radio.Width = col_width
                radio.Click += self.on_shape_type_changed
                panel.Controls.Add(radio)
                self.radio_buttons.append(radio)
            
            self.rollout.Controls.Add(panel)
            
            # Initialize with current selection
            sel_array = rt.getCurrentSelection()
            if len(sel_array) > 0:
                for item in sel_array:
                    if rt.superClassOf(item) == rt.helper:
                        self.size_spinner.Value = rt.dotNetObject("System.Decimal", float(item.size))
                        break
        
        def on_size_changed(self, sender, args):
            val = float(self.size_spinner.Value)
            if rt.selection.count > 0:
                rt.undo.beginBlock()
                for item in rt.selection:
                    jal.helper.set_size(item, val)
                rt.undo.endBlock()
        
        def on_add_size_changed(self, sender, args):
            val = float(self.add_spinner.Value)
            if rt.selection.count > 0:
                rt.undo.beginBlock()
                for item in rt.selection:
                    jal.helper.add_size(item, val)
                rt.undo.endBlock()
        
        def on_add_size_reset(self, sender, args):
            self.add_spinner.Value = rt.dotNetObject("System.Decimal", 0.0)
        
        def on_shape_type_changed(self, sender, args):
            if rt.selection.count > 0:
                rt.undo.beginBlock()
                for i, radio in enumerate(self.radio_buttons):
                    if radio.Checked:
                        for item in rt.selection:
                            if i == 0:  # Box
                                jal.helper.set_shape_to_box(item)
                            elif i == 1:  # Cross
                                jal.helper.set_shape_to_cross(item)
                            elif i == 2:  # Axis
                                jal.helper.set_shape_to_axis(item)
                            elif i == 3:  # Center
                                jal.helper.set_shape_to_center(item)
                        break
                rt.undo.endBlock()
        
        def show_dialog(self):
            self.rollout.Show()
    
    # Create and show dialog
    dialog = HelperShapeModRollout()
    dialog.show_dialog()

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
# jal_create_average_helper()
# jal_create_pos_average_helper()
# jal_create_rot_average_helper()
# jal_create_two_helper()
# jal_modify_helperShape()
# jal_create_expHelper()
# jal_create_helper()
jal_create_parentHelper()
