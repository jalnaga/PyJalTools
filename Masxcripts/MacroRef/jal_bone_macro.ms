macroscript jal_boneOn category:"jalTools" tooltip:"Bone On Selection" autoUndoEnabled:true (
    jal.bone.set_bone_on_selection()
)

macroscript jal_boneOff category:"jalTools" tooltip:"Bone Off Selection" autoUndoEnabled:true (
    jal.bone.set_bone_off_selection()
)

macroscript jal_boneLengthFreezeOn category:"jalTools" tooltip:"Bone Length Freeze On Selection" autoUndoEnabled:true (
    jal.bone.set_freeze_length_on_selection()
)

macroscript jal_boneLengthFreezeOff category:"jalTools" tooltip:"Bone Length Freeze Off Selection" autoUndoEnabled:true (
    jal.bone.set_freeze_length_off_selection()
)

macroscript jal_boneFinOn category:"jalTools" tooltip:"Bone Fin On" autoUndoEnabled:true (
    local selArray = getCurrentSelection() as Array
    if selArray.count > 0 then for item in selArray do jal.bone.set_fin_on item
)

macroscript jal_boneFinOff category:"jalTools" tooltip:"Bone Fin Off" autoUndoEnabled:true (
    local selArray = getCurrentSelection() as Array
    if selArray.count > 0 then for item in selArray do jal.bone.set_fin_off item
)

macroscript jal_boneResetScale category:"jalTools" tooltip:"Bone Reset Scale" autoUndoEnabled:true (
    local selArray = getCurrentSelection() as Array
    for item in selArray do (
        if (classOf item == BoneGeometry) then (
            if item.children.count == 1 then (
                item.realignBoneToChild()
                jal.bone.correct_negative_stretch item true
                item.ResetBoneStretch()
            )
        )
    )
    jal.bone.reset_scale_of_selected_bones true
)

macroscript jal_boneCreate category:"jalTools" tooltip:"Bone Create" autoUndoEnabled:true (
    local boneName = "Bip001 TempBone 0"
    local boneNameSetted = false
    local selArray = getCurrentSelection() as Array
    local simpleBoneLength = 5

    rollout boneNameRollout "Bone Name" (
        editText boneBaseNameTxt "Base Name:" text:"Bip001"
        dropdownList baseNameDrp "" items:#("")
        editText boneNameTxt "Name:" text:"TempBone"
        radiobuttons sideRdo "Side:" align:#left labels:#("(None)", "L", "R") offsets:#([30, -16], [30, -16], [30, -16])
        radiobuttons frontBackRdo "Front:" align:#left labels:#("(None)", "F", "B") offsets:#([30, -16], [30, -16], [30, -16])
        radiobuttons filteringCharRdo "Filtering:" align:#left labels:#("(Blank)", "_") offsets:#([45, -16], [45, -16])
        editText resultTxt "Result:" readOnly:true text:"Bip001 TempBone 0" labelOnTop:true offset:[0, 10]
        button okBtn "OK" across:2 width:50
        button cancelBtn "Cancel" width:50

        local boneBaseName = ""
        local sideCharArray = #()
        local frontBackCharArray = #()
        local boneNameFilteringChar = " "

        fn update_boneNameResult = (
            if boneBaseNameTxt.text != "" then boneBaseName = boneBaseNameTxt.text
            if boneBaseNameTxt.text == "" and baseNameDrp.selection > 1 then boneBaseName = baseNameDrp.items[baseNameDrp.selection]

            boneName = jal.name.combine inBase:boneBaseName inFrontBack:frontBackCharArray[frontBackRdo.state] inSide:sideCharArray[sideRdo.state] inRealName:boneNameTxt.text inIndex:"0" inFilChar:boneNameFilteringChar
            resultTxt.text = boneName
            boneName = jal.name.replace_index boneName ""
        )

        on boneNameRollout open do (
            boneNameSetted = false
            baseNameDrp.items = #("") + jal.name.__baseStrArray
            sideCharArray = #("", jal.name.get_leftStr(), jal.name.get_rightStr())
            frontBackCharArray = #("", jal.name.get_frontStr(), jal.name.get_backStr())
        )

        on boneBaseNameTxt changed inText do update_boneNameResult()
        on baseNameDrp selected inSel do (
            boneBaseNameTxt.text = ""
            update_boneNameResult()
        )
        on boneNameTxt changed inText do update_boneNameResult()

        on sideRdo changed state do update_boneNameResult()
        on frontBackRdo changed state do update_boneNameResult()

        on filteringCharRdo changed state do (
            case state of (
                1: boneNameFilteringChar = " "
                2: boneNameFilteringChar = "_"
            )
            update_boneNameResult()
        )

        on okBtn pressed do (
            update_boneNameResult()

            local isBoneExist = 0
            local nameCheckBonesArray = for item in objects where (classOf item) == BoneGeometry collect item
            for item in nameCheckBonesArray do (
                if (matchPattern item.name pattern:(boneName + (jal.name.get_filteringChar boneName) + "*")) then isBoneExist += 1
            )
            if isBoneExist > 0 then (
                messageBox "Same Name Bones already exist!"
                boneNameSetted = false
            )
            else (
                boneNameSetted = true
                destroydialog boneNameRollout
            )
        )

        on cancelBtn pressed do (
            boneNameSetted = false
            boneName = "Bip001 TempBone 0"
            destroydialog boneNameRollout
        )
    )
    createDialog boneNameRollout style:#(#style_titlebar, #style_border) escapeEnable:false modal:true

    if boneNameSetted then (
        if selArray.count == 0 or selArray.count == 1 then (
            local genBones = jal.bone.create_simple_bone simpleBoneLength boneName
            if selArray.count == 1 then genBones[1].transform = selArray[1].transform
        )
        if selArray.count > 1 then (
            jal.bone.create_bone selArray boneName delPoint:true
        )
    )
)

macroscript jal_boneNubCreate category:"jalTools" tooltip:"Bone Nub Create" autoUndoEnabled:true (
    local selArray = getCurrentSelection() as Array
    if selArray.count > 0 then (
        local lastBoneArray = #()
        local nonBoneArray = #()

        for item in selArray do (
            if (classOf item == BoneGeometry) then append lastBoneArray item
            else append nonBoneArray item
        )

        for item in lastBoneArray do (
            if item.children.count == 0 then jal.bone.create_end_bone item
        )
        for item in nonBoneArray do jal.bone.create_nub_bone_on_obj item
    )
    else jal.bone.create_nub_bone "Temp Nub" 2
)
