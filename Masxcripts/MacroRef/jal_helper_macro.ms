macroscript jal_create_parentHelper category:"jalTools" tooltip:"create Parent Helper" autoUndoEnabled:true (
    jal.helper.create_parent_helper()
)

macroscript jal_create_helper category:"jalTools" tooltip:"create Helper" autoUndoEnabled:true (
    rollout helperTypeRollout "Set Helper Type" (
        dropdownList helperTypeDrp items:#("Dum", "Root", "Pos", "Rot", "Tg", "IK", "P")
        button okBtn "OK"

        on helperTypeRollout open do (
            helperTypeDrp.items = jal.name.__typeStrArray
        )

        on okBtn pressed do (
            local genHelpers = jal.helper.create_helper()
            for item in genHelpers do (
                item.name = jal.name.replace_type item.name helperTypeDrp.items[helperTypeDrp.selection]
            )
            DestroyDialog helperTypeRollout
        )
    )
    createDialog helperTypeRollout modal:true
)

macroscript jal_create_average_helper category:"jalTools" tooltip:"create Average Helper" autoUndoEnabled:true (
    local selArray = getCurrentSelection()

    if selArray.count > 0 then (
        local tempTransform = matrix3 1
        tempTransform.rotation = (jal.anim.create_average_rot_transform selArray).rotation
        tempTransform.position = (jal.anim.create_average_pos_transform selArray).position

        local dumName = jal.helper.gen_helper_name_from_obj selArray[1]
        local dumShape = jal.helper.gen_helper_shape_from_obj selArray[1]
        local averageDum = jal.helper.create_point dumName[1] size:dumShape[1] boxToggle:dumShape[3] crossToggle:dumShape[2]
        averageDum.transform = tempTransform
    )
)

macroscript jal_create_pos_average_helper category:"jalTools" tooltip:"create Pos avrg. Helper" autoUndoEnabled:true (
    local selArray = getCurrentSelection()

    if selArray.count > 0 then (
        local tempTransform = matrix3 1
        tempTransform.position = (jal.anim.create_average_pos_transform selArray).position

        local dumName = jal.helper.gen_helper_name_from_obj selArray[1]
        local dumShape = jal.helper.gen_helper_shape_from_obj selArray[1]
        local averageDum = jal.helper.create_point dumName[1] size:dumShape[1] boxToggle:dumShape[3] crossToggle:dumShape[2]
        averageDum.transform = tempTransform
        averageDum.name = jal.name.replace_type averageDum.name "Pos"
    )
)

macroscript jal_create_rot_average_helper category:"jalTools" tooltip:"create Rot avrg. Helper" autoUndoEnabled:true (
    local selArray = getCurrentSelection()

    if selArray.count > 0 then (
        local tempTransform = matrix3 1
        tempTransform.rotation = (jal.anim.create_average_rot_transform selArray).rotation

        local dumName = jal.helper.gen_helper_name_from_obj selArray[1]
        local dumShape = jal.helper.gen_helper_shape_from_obj selArray[1]
        local averageDum = jal.helper.create_point dumName[1] size:dumShape[1] boxToggle:dumShape[3] crossToggle:dumShape[2]
        averageDum.transform = tempTransform
        averageDum.name = jal.name.replace_type averageDum.name "Rot"
    )
)

macroscript jal_create_expHelper category:"jalTools" tooltip:"create Exp Helper" autoUndoEnabled:true (
    jal.helper.create_expTm()
)

macroscript jal_create_two_helper category:"jalTools" tooltip:"create Two Helper" autoUndoEnabled:true (
    rollout helperTypeRollout "Set Helper Type" (
        radioButtons helperTypeRdo labels:#("Dum", "Root", "Pos", "Rot", "Tg", "IK", "P") columns:2
        button okBtn "OK"

        on helperTypeRollout open do (
            hleperTypeRdo.labels = jal.name.__typeStrArray
        )

        on okBtn pressed do (
            local genHelpers = jal.helper.create_helper makeTwo:true
            for item in genHelpers do (
                item.name = jal.name.replace_type item.name jal.name.__typeStrArray[helperTypeRdo.state]
            )
            DestroyDialog helperTypeRollout
        )
    )
    createDialog helperTypeRollout modal:true
)

macroscript jal_modify_helperShape category:"jalTools" tooltip:"modify Helper shape" autoUndoEnabled:true (
    rollout helperShapeModRollout "Modify Helper Shape" (
        spinner helperSizeSpn "Size:" range:[0, 100, 1.0] across:2
        spinner helperSizeAddSpn "Add:" range:[-100, 100, 0.0]
        radioButtons helperTypeRdo labels:#("Box", "Cross", "Axis", "Center") across:2 columns:2

        on helperShapeModRollout open do (
            local selArray = getCurrentSelection()
            for item in selArray do (
                if superClassOf item == helper then (
                    helperSizeSpn.value = item.size
                    exit
                )
            )
        )

        on helperSizeSpn changed val do (
            undo on (
                if selection.count > 0 then for item in selection do jal.helper.set_size item val
            )
        )

        on helperSizeAddSpn changed val do (
            undo on (
                if selection.count > 0 then for item in selection do jal.helper.add_size item val
            )
        )
        on helperSizeAddSpn buttonup do helperSizeAddSpn.value = 0.0

        on helperTypeRdo changed state do (
            undo on (
                if selection.count > 0 then (
                    case state of (
                        1: for item in selection do jal.helper.set_shape_to_box item
                        2: for item in selection do jal.helper.set_shape_to_cross item
                        3: for item in selection do jal.helper.set_shape_to_axis item
                        4: for item in selection do jal.helper.set_shape_to_center item
                    )
                )
            )
        )
    )
    createDialog helperShapeModRollout width:250
)
