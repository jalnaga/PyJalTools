macroscript jal_align_to_last category:"jalTools" tooltip:"Aling to last" autoUndoEnabled:true (
    jal.align.align_to_last_sel()
)

macroscript jal_align_to_last_center category:"jalTools" tooltip:"Aling to last center" autoUndoEnabled:true (
    jal.align.align_to_last_sel_center()
)

macroscript jal_align_pos_only category:"jalTools" tooltip:"Aling Position only" autoUndoEnabled:true (
    jal.align.align_to_last_sel_pos()
)

macroscript jal_align_rot_only category:"jalTools" tooltip:"Aling Rotation only" autoUndoEnabled:true (
    jal.align.align_to_last_sel_rot()
)

macroscript jal_align_mirror_x category:"jalTools" tooltip:"Mirror X" autoUndoEnabled:true (
    if selection.count > 0 then (
        local pObj = undefined
        local defMirrorAxis = 0
        local nonNegativeAxis = 0
        local oriObjArray = getCurrentSelection() as Array
        local inOriObjArray = deepCopy oriObjArray
        local boneArray = #()
        local helperArray = #()
        local nonBoneArray = #()

        local mirroredBoneArray = #()
        local mirroredHelperArray = #()
        local mirroredNonBoneArray = #()
        local mirroredObjArray = #()

        defMirrorAxis = 1
        nonNegativeAxis = 1

        for item in inOriObjArray do (
            local caseIndex = 0
            if classOf item == BoneGeometry then caseIndex = 1
            if superClassOf item == helper then caseIndex = 2
            case caseIndex of (
                1: append boneArray item
                2: append helperArray item
                default: append nonBoneArray item
            )
        )
        if boneArray.count != 0 then mirroredBoneArray = jal.mirror.mirror_bone boneArray mAxis:defMirrorAxis
        if helperArray.count != 0 then (
            mirroredHelperArray = jal.mirror.mirror_geo helperArray mAxis:defMirrorAxis pivotObj:pObj cloneStatus:2
        )
        if nonBoneArray.count != 0 then (
            mirroredNonBoneArray = jal.mirror.mirror_geo nonBoneArray mAxis:defMirrorAxis pivotObj:pObj cloneStatus:2
        )

        join mirroredObjArray mirroredBoneArray
        join mirroredObjArray mirroredHelperArray
        join mirroredObjArray mirroredNonBoneArray

        clearSelection()
        select mirroredObjArray
    )
)

macroscript jal_align_mirror_y category:"jalTools" tooltip:"Mirror Y" autoUndoEnabled:true (
    if selection.count > 0 then (
        local pObj = undefined
        local defMirrorAxis = 0
        local nonNegativeAxis = 0
        local oriObjArray = getCurrentSelection() as Array
        local inOriObjArray = deepCopy oriObjArray
        local boneArray = #()
        local helperArray = #()
        local nonBoneArray = #()

        local mirroredBoneArray = #()
        local mirroredHelperArray = #()
        local mirroredNonBoneArray = #()
        local mirroredObjArray = #()

        defMirrorAxis = 2
        nonNegativeAxis = 3

        for item in inOriObjArray do (
            local caseIndex = 0
            if classOf item == BoneGeometry then caseIndex = 1
            if superClassOf item == helper then caseIndex = 2
            case caseIndex of (
                1: append boneArray item
                2: append helperArray item
                default: append nonBoneArray item
            )
        )
        if boneArray.count != 0 then mirroredBoneArray = jal.mirror.mirror_bone boneArray mAxis:defMirrorAxis
        if helperArray.count != 0 then (
            mirroredHelperArray = jal.mirror.mirror_geo helperArray mAxis:defMirrorAxis pivotObj:pObj cloneStatus:2
        )
        if nonBoneArray.count != 0 then (
            mirroredNonBoneArray = jal.mirror.mirror_geo nonBoneArray mAxis:defMirrorAxis pivotObj:pObj cloneStatus:2
        )

        join mirroredObjArray mirroredBoneArray
        join mirroredObjArray mirroredHelperArray
        join mirroredObjArray mirroredNonBoneArray

        clearSelection()
        select mirroredObjArray
    )
)
