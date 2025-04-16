/*******************************/
/* Bone Creation Library
/* dependency:
/*     name.ms
/*     anim.ms
/*     helper.ms
/*     constraint.ms
/*******************************/
struct _Bone (
    str, name, anim, helper, const,

    fn remove_ik inBone = (
        if (not IsProperty inBone "pos") or (not IsProperty inBone "rotation") then HDIKSys.RemoveChain inBone
    ),

    fn get_bone_assemblyHead inBone = (
        tempBone = inBone
        while (tempBone != undefined) do (
            if tempBone.assemblyHead then return tempBone
            if not tempBone.assemblyMember then exit
            tempBone = tempBone.parent
        )
        undefined
    ),

    fn put_child_into_bone_assembly inBone = (
        if (inBone.parent != undefined) and (inBone.parent.assemblyMember) then (
            inBone.assemblyMember = true
            inBone.assemblyMemberOpen = true
        )
    ),

    fn sort_bones_as_hierarchy inBoneArray = (
        struct BoneLevel (index, level)
        local bones     = #()

        -- fill the array of bone structures. intialize the hierarchy level with 0
        for i = 1 to inBoneArray.count do
        (
            bones[i] = BoneLevel i 0
        )

        -- calculate the hierarchy level for each bone in bones array. the hierarchy level
        -- is the number of ancestors between the current bone and the root node
        for i = 1 to bones.count do
        (
            local node = inBoneArray[bones[i].index]
            local n    = 0
            do
            (
                n    = n + 1
                node = node.parent
            ) while (node != undefined)
            bones[i].level = n
        )

        -- sort the bones array by the hierarchy level
        qsort bones (fn myLevel v1 v2 = (v1.level - v2.level))

        -- prepare the storage for the new bones and their parents
        local returnBonesArray = #()
        for i = 1 to inBoneArray.count do append returnBonesArray inBoneArray[bones[i].index]

        return returnBonesArray
    ),

    fn correct_negative_stretch bone ask = (
        local axisIndex, ooscale
        case bone.boneAxis of
        (
            #X: axisIndex = 1
            #Y: axisIndex = 2
            #Z: axisIndex = 3
        )

        ooscale = bone.objectOffsetScale
        if (ooscale[axisIndex] < 0) and ((not ask) or (queryBox "Correct negative scale?" title:bone.Name)) do
        (
            ooscale[axisIndex] = -ooscale[axisIndex]
            axisIndex = axisIndex+2
            if axisIndex > 3 do axisIndex = axisIndex-3
            ooscale[axisIndex] = -ooscale[axisIndex]
            bone.objectOffsetScale = ooscale
        )
    ),

    fn reset_scale_of_selected_bones ask = (
        local bones = for item in selection where classof item == BoneGeometry collect item
        bones = sort_bones_as_hierarchy selection

        -- reset scale for all bones in the bones array
        --print "***resetting***"
        for i = 1 to bones.count do
        (
            ResetScale bones[i]
            if ask do correct_negative_stretch bones[i] false
        )
    ),

    fn is_nub_bone inputBone = (
        if (classOf inputBone) == BoneGeometry then (
            if inputBone.parent == undefined and inputBone.children.count == 0 then return true
            else return false
        )
        return false
    ),

    fn is_end_bone inputBone = (
        if (classOf inputBone) == BoneGeometry then (
            if inputBone.parent != undefined and inputBone.children.count == 0 then return true
            else return false
        )
        return false
    ),

    fn create_nub_bone inName inSize = (
        local nubBone = undefined
        with redraw off (
            nubBone = BoneSys.createBone [0,0,0] [1,0,0] [0,0,1]

            nubBone.width = inSize
            nubBone.height = inSize
            nubBone.taper = 90
            nubBone.length = inSize
            nubBone.frontfin = off
            nubBone.backfin = off
            nubBone.sidefins = off
            nubBone.name = name.set_index_as_nub inName
        )
        redrawViews()

        return nubBone
    ),

    fn create_nub_bone_on_obj inObj inSize:1 = (
        local boneName = name.get_string inObj.name
        local newBone = create_nub_bone boneName inSize
        newBone.transform = inObj.transform

        return newBone
    ),

    fn create_end_bone inBone = (
        local parentBone  = inBone
        local parentTrans = parentBone.transform
        local parentPos = parentTrans.translation
        local boneName = name.get_string parentBone.name
        local newbone = create_nub_bone boneName parentBone.width

        newBone.transform = parentTrans
        in coordSys Local move newBone [parentBone.length, 0, 0]

        newBone.parent = parentBone
        put_child_into_bone_assembly newBone

        newBone.width = parentBone.width
        newBone.height = parentBone.height
        newBone.frontfin = off
        newBone.backfin = off
        newBone.sidefins = off
        newBone.taper = 90
        newBone.length = (parentBone.width + parentBone.height) / 2
        newBone.wirecolor = parentBone.wirecolor

        return newBone
    ),

    fn create_bone inPointArray inName end:true delPoint:false parent:false size:2 normals:#() = (
        local filteringChar = str.get_filteringChar inName
        local tempBone = undefined
        local newBone = undefined

        local returnBoneArray = #()

        if inPointArray.count != 1 then (
            for i = 1 to (inPointArray.count - 1) do (
                local boneNum = i - 1

                if normals.count == inPointArray.count then (
                    local xDir = normalize(inPointArray[i+1].transform.position - inPointArray[i].transform.position)
                    local zDir = normalize(cross xDir normals[i])
                    newBone = BoneSys.createBone inPointArray[i].transform.position inPointArray[i+1].transform.position zDir
                )
                else (
                    newBone = BoneSys.createBone inPointArray[i].transform.position inPointArray[i+1].transform.position [0,-1,0]
                )

                newBone.boneFreezeLength=true
                newBone.name = inName + filteringChar + (boneNum as String)
                newBone.height = size
                newBone.width = size
                newBone.frontfin = off
                newBone.backfin = off
                newBone.sidefins = off

                append returnBoneArray newBone

                if tempBone != undefined then (
                    local tempTm = copy (newBone.transform * Inverse tempBone.transform)
                    local localRot = (tempTm.rotation as EulerAngles).x

                    anim.rotate_local newBone -localRot 0 0
                )

                newBone.parent = tempBone
                tempBone = newBone
            )

            if delPoint then (
                for i = 1 to inPointArray.count do (
                    if ((classOf inPointArray[i] == Dummy) or (classOf inPointArray[i] == ExposeTm) or (classOf inPointArray[i] == Point)) then delete inPointArray[i]
                )
            )

            if parent then (
                local parentNubPoint = helper.create_point (inName + filteringChar + "PNub") size:size boxToggle:on crossToggle:on
                parentNubPoint.transform = returnBoneArray[1].transform
                returnBoneArray[1].parent = parentNubPoint
            )

            select newBone

            if end then (
                local endBone = create_end_bone newBone
                append returnBoneArray endBone

                clearSelection()

                return returnBoneArray
            )
            else return returnBoneArray
        )
        else return false
    ),

    fn create_simple_bone inLength inName end:true size:1 = (
        local startPoint = helper.create_point "tempStart"
        local endPoint = helper.create_point "tempEnd" pos:[inLength, 0, 0]
        local returnBoneArray = create_bone #(startPoint, endPoint) inName end:end delPoint:true size:size

        return returnBoneArray
    ),

    fn create_stretch_bone inPointArray inName size:2 = (
        local tempBone = #()
        local returnArray = #()
        tempBone = create_bone inPointArray inName size:size

        for i = 1 to (tempBone.count - 1) do
        (
            tempBone[i].position.controller = Position_Constraint()
            tempBone[i].position.controller.AppendTarget inPointArray[i] 100

            tempBone[i].rotation.controller =  LookAt_Constraint()
            tempBone[i].rotation.controller.appendTarget inPointArray[i+1] 100
            tempBone[i].rotation.controller.lookat_vector_length = 0
        )

        tempBone[tempBone.count].position.controller = Position_Constraint()
        tempBone[tempBone.count].position.controller.AppendTarget inPointArray[inPointArray.count] 100

        return tempBone
    ),

    fn create_simple_stretch_bone inStart inEnd inName squash:false size:1 = (
        local returnArray = #()
        returnArray = create_stretch_bone #(inStart, inEnd) inName size:size
        if squash then returnArray[1].boneScaleType = #squash

        return returnArray
    ),

    fn get_bone_shape inBone = (
        local returnArray = #()
        if (classOf inBone) == BoneGeometry then (
            returnArray[1] = inBone.width
            returnArray[2] = inBone.height
            returnArray[3] = inBone.taper
            returnArray[4] = inBone.length
            returnArray[5] = inBone.sidefins
            returnArray[6] = inBone.sidefinssize
            returnArray[7] = inBone.sidefinsstarttaper
            returnArray[8] = inBone.sidefinsendtaper
            returnArray[9] = inBone.frontfin
            returnArray[10] = inBone.frontfinsize
            returnArray[11] = inBone.frontfinstarttaper
            returnArray[12] = inBone.frontfinendtaper
            returnArray[13] = inBone.backfin
            returnArray[14] = inBone.backfinsize
            returnArray[15] = inBone.backfinstarttaper
            returnArray[16] = inBone.backfinendtaper
        )

        return returnArray
    ),

    fn pasete_bone_shape targetBone shapeArray = (
        if (classOf targetBone) == BoneGeometry then (
            targetBone.width = shapeArray[1]
            targetBone.height = shapeArray[2]
            targetBone.taper = shapeArray[3]
            --targetBone.length = shapeArray[4]
            targetBone.sidefins = shapeArray[5]
            targetBone.sidefinssize = shapeArray[6]
            targetBone.sidefinsstarttaper = shapeArray[7]
            targetBone.sidefinsendtaper = shapeArray[8]
            targetBone.frontfin = shapeArray[9]
            targetBone.frontfinsize = shapeArray[10]
            targetBone.frontfinstarttaper = shapeArray[11]
            targetBone.frontfinendtaper = shapeArray[12]
            targetBone.backfin = shapeArray[13]
            targetBone.backfinsize = shapeArray[14]
            targetBone.backfinstarttaper = shapeArray[15]
            targetBone.backfinendtaper = shapeArray[16]

            if (is_end_bone targetBone) then (
                targetBone.taper = 90
                targetBone.length = (targetBone.width + targetBone.height) / 2
                targetBone.frontfin = off
                targetBone.backfin = off
                targetBone.sidefins = off
            )

            return true
        )
        return false
    ),

    fn set_fin_on inBone side:true front:true back:false inSize:2.0 inTaper:0.0 = (
        if (classOf inBone) == BoneGeometry then (
            if not (is_end_bone inBone) then (
                inBone.frontfin = front
                inBone.frontfinsize = inSize
                inBone.frontfinstarttaper = inTaper
                inBone.frontfinendtaper = inTaper

                inBone.sidefins = side
                inBone.sidefinssize = inSize
                inBone.sidefinsstarttaper = inTaper
                inBone.sidefinsendtaper = inTaper

                inBone.backfin = back
                inBone.backfinsize = inSize
                inBone.backfinstarttaper = inTaper
                inBone.backfinendtaper = inTaper
            )
        )
    ),

    fn set_fin_off inBone = (
        if (classOf inBone) == BoneGeometry then (
            inBone.frontfin = false
            inBone.sidefins = false
            inBone.backfin = false
        )
    ),

    fn set_bone_size inBone inSize = (
        if (classOf inBone == BoneGeometry) then (
            inBone.width = inSize
            inBone.height = inSize

            if (is_end_bone inBone) or (is_nub_bone inBone) then (
                inBone.taper = 90
                inBone.length = inSize
            )
        )
    ),

    fn set_bone_taper inBone inTaper = (
        if (classOf inBone == BoneGeometry) then (
            if not (is_end_bone inBone) then inBone.taper = inTaper
        )
    ),

    fn delete_bones_safely inBoneArray = (
        if inBoneArray.count > 0 then (
            for targetBone in inBoneArray do (
                const.collapse targetBone
                targetBone.parent = undefined
                delete targetBone
            )
            inBoneArray = deepCopy #()
        )
    ),

    fn select_first_children inObj = (
        selectmore inObj

        if inObj.children[1] == undefined then return false
        else (
            for i = 1 to inObj.children.count do (
                select_first_children inObj.children[i]
            )
            return true
        )
    ),

    fn select_every_children inObj includeSelf:false = (
        local children = #()
        if includeSelf then (
            children = (execute ("$'" + inObj.name + "'/*/.../*")) as array
            insertItem inObj children 1
        )
        else children = (execute ("$'" + inObj.name + "'/*/.../*")) as array

        children
    ),

    fn get_bone_end_position inBone = (
        if (classOf inBone == BoneGeometry) then [inBone.length, 0, 0] * inBone.objectTransform
        else (inBone.transform).translation
    ),

    fn link_skin_bone inSkinBone inOriBone = (
        anim.save_xform inSkinBone
        anim.set_xform inSkinBone

        anim.save_xform inOriBone
        anim.set_xform inOriBone

        inSkinBone.scale.controller = (scaleXYZ())
        inSkinBone.controller = (link_constraint())

        anim.set_xform #(inSkinBone) space:#world
        inSkinBone.transform.controller.AddTarget (inOriBone) 0
    ),

    fn link_skin_bones inSkinBoneArray inOriBoneArray = (
        if inSkinBoneArray.count != inOriBoneArray.count then return false

        for i = 1 to inSkinBoneArray.count do (
            link_skin_bone inSkinBoneArray[i] inOriBoneArray[i]
        )

        return true
    ),

    fn create_skin_bone inBoneArray skipNub:true mesh:true link:true skinBoneBaseName:"b" = (
        local bones = #()
        local oriBoneNames = for item in inBoneArray collect item.name
        local skinBoneFilteringChar = "_"
        local skinBonePushAmount = -0.02
        local returnBones = #()

        for i = 1 to inBoneArray.count do (
            --local skinBone = BoneSys.createBone inBoneArray[i].transform.translation (inBoneArray[i].transform.translation+6) inBoneArray[i].dir
            local skinBoneName = name.replace_base inBoneArray[i].name skinBoneBaseName
            skinBoneName = name.replace_filteringChar skinBoneName skinBoneFilteringChar

            local skinBone = (create_nub_bone "b_TempSkin" 2)
            skinBone.name = skinBoneName
            skinBone.wireColor = color 255 88 199
            skinBone.transform = inBoneArray[i].transform

            if mesh == true then (
                local snapShotObj = snapshot inBoneArray[i]
                addModifier snapShotObj (Push())
                snapShotObj.modifiers[#Push].Push_Value = skinBonePushAmount
                collapseStack snapShotObj

                addModifier skinBone (Edit_Poly())
                max modify mode
                modPanel.setCurrentObject skinBone.modifiers[#Edit_Poly]
                skinBone.modifiers[#Edit_Poly].Attach snapShotObj editPolyNode:skinBone
            )

            skinBone.boneEnable = true
            skinBone.renderable = false
            skinBone.boneScaleType=#none

            append bones skinBone
        )

        for i = 1 to inBoneArray.count do (
            local oriParentObj = inBoneArray[i].parent
            if oriParentObj != undefined then (
                local skinBoneParentObjName = name.replace_base oriParentObj.name skinBoneBaseName
                skinBoneParentObjName = name.replace_filteringChar skinBoneParentObjName skinBoneFilteringChar
                bones[i].parent = getNodeByName skinBoneParentObjName
            )
            else bones[i].parent = undefined
        )
        if link == true then (
            link_skin_bones bones inBoneArray
        )

        if skipNub then (
            for item in bones do (
                if not (matchPattern item.name pattern:"*Nub") then append returnBones item
                else delete item
            )
        )
        else returnBones = deepCopy bones

        bones = #()

        return returnBones
    ),

    fn create_skin_bone_from_bip inBoneArray skipNub:true mesh:false link:true skinBoneBaseName:"b" = (
        local targetBones = for item in inBoneArray where ((classOf item) == Biped_Object) and (not(matchPattern item.name pattern:"*Twist*")) and (item != item.controller.rootNode) collect item
        local returnSkinBones = create_skin_bone targetBones skipNub:skipNub mesh:mesh link:link skinBoneBaseName:skinBoneBaseName

        returnSkinBones
    ),

    fn create_skin_bone_from_bip_for_unreal inBoneArray skipNub:true mesh:false link:true skinBoneBaseName:"b" = (
        local genBones = create_skin_bone_from_bip inBoneArray skipNub:skipNub mesh:mesh link:link skinBoneBaseName:skinBoneBaseName
        if genBones.count == 0 then return false
        
        for item in genBones do (
            if matchPattern item.name pattern:"*Pelvis*" then anim.rotate_local item 180 0 0
            if matchPattern item.name pattern:"*Spine*" then anim.rotate_local item 180 0 0
            if matchPattern item.name pattern:"*Neck*" then anim.rotate_local item 180 0 0
            if matchPattern item.name pattern:"*Head*" then anim.rotate_local item 180 0 0
        )

        return genBones
    ),

    fn set_bone_on inBone = (
        if (classOf inBone == BoneGeometry) then (
            inBone.boneEnable = true
        )
    ),

    fn set_bone_off inBone = (
        if (classOf inBone == BoneGeometry) then (
            inBone.boneEnable = false
        )
    ),

    fn set_bone_on_selection = (
        local selArray = getCurrentSelection() as array
        for item in selArray do set_bone_on item
    ),

    fn set_bone_off_selection = (
        local selArray = getCurrentSelection() as array
        for item in selArray do set_bone_off item
    ),

    fn set_freeze_length_on inBone = (
        if (classOf inBone == BoneGeometry) then (
            inBone.boneFreezeLength = true
        )
    ),

    fn set_freeze_length_off inBone = (
        if (classOf inBone == BoneGeometry) then (
            inBone.boneFreezeLength = false
        )
    ),

    fn set_freeze_length_on_selection = (
        local selArray = getCurrentSelection() as array
        for item in selArray do set_freeze_length_on item
    ),

    fn set_freeze_length_off_selection = (
        local selArray = getCurrentSelection() as array
        for item in selArray do set_freeze_length_off item
    )
)
