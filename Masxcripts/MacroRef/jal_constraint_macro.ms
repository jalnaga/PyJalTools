macroscript jal_collapse_const category:"jalTools" tooltip:"Collapes Constraints" autoUndoEnabled:true (
    if selection.count > 0 then (
        local selArray = getCurrentSelection() as Array
        for selObj in selArray do jal.const.collapse selObj
    )
)

macroscript jal_pos_const category:"jalTools" tooltip:"Constraints Position" autoUndoEnabled:true (
    if selection.count >1 then (
        local selArray = getCurrentSelection()
        local oriObj = selArray[1]
        local targetObjArray = #()
    
        for i = 2 to selArray.count do (
            append targetObjArray selArray[i]
        )
    
        jal.const.assign_pos_const_multi oriObj targetObjArray
    )
)

macroscript jal_ori_const category:"jalTools" tooltip:"Constraints Orientation" autoUndoEnabled:true (
    if selection.count >1 then (
        local selArray = getCurrentSelection()
        local oriObj = selArray[1]
        local targetObjArray = #()
    
        for i = 2 to selArray.count do (
            append targetObjArray selArray[i]
        )
    
        jal.const.assign_rot_const_multi oriObj targetObjArray
    )
)

macroscript jal_rot_script_const category:"jalTools" tooltip:"Constraint Rotation Script" autoUndoEnabled:true (
    if selection.count == 2 then (
        local selArray = getCurrentSelection()
        local oriObj = selArray[1]
        local targetObj = selArray[2]
    
        jal.const.assign_rot_const_scripted oriObj targetObj
    )
)

macroscript jal_lookat_const category:"jalTools" tooltip:"Constraint LookAt" autoUndoEnabled:true (
    if selection.count >1 then (
        local selArray = getCurrentSelection()
        local oriObj = selArray[1]
        local targetObjArray = #()
    
        for i = 2 to selArray.count do (
            append targetObjArray selArray[i]
        )
    
        jal.const.assign_lookat_multi oriObj targetObjArray
    )
)

macroscript jal_lookat_flipless_const category:"jalTools" tooltip:"Constraint LookAt Flipless" autoUndoEnabled:true (
    if selection.count == 2 then (
        local selArray = getCurrentSelection()
        local oriObj = selArray[1]
        local targetObj = selArray[2]
    
        jal.const.assign_lookat_flipless oriObj targetObj
    )
)

macroscript jal_lookat_script_const category:"jalTools" tooltip:"Constraint LookAt Script" autoUndoEnabled:true (
    if selection.count > 1 then (
        local selArray = getCurrentSelection()
        local oriObj = selArray[1]
        local targetObjArray = #()
    
        for i = 2 to selArray.count do (
            append targetObjArray selArray[i]
        )
    
        jal.const.assign_scripted_lookat oriObj targetObjArray
    )
)
