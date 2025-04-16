struct _Constraint (
    str, name, helper,

    fn collapse inObj = (
        if classof inObj != Biped_Object then (
            local tempTransform = inObj.transform
            inObj.position.controller = Position_XYZ()
            inObj.rotation.controller = Euler_XYZ()
            inObj.scale.controller = Bezier_Scale()
            inObj.transform = tempTransform
        )
    ),

    fn set_active_last inObj = (
        if classOf inObj.position.controller == position_list then (
            inObj.position.controller.setActive inObj.position.controller.count
        )
        if classOf inObj.rotation.controller == rotation_list then (
            inObj.rotation.controller.setActive inObj.rotation.controller.count
        )
    ),

    fn get_pos_list_controller inObj = (
        local returnPosListCtr = undefined

        if classOf inObj.position.controller == position_list then returnPosListCtr = inObj.position.controller

        returnPosListCtr
    ),

    fn assign_pos_list inObj = (
        local returnPosListCtr = undefined

        if classOf inObj.position.controller != position_list then (
            returnPosListCtr = position_list()
            inObj.position.controller = returnPosListCtr
            return returnPosListCtr
        )
        if classOf inObj.position.controller == position_list then returnPosListCtr = inObj.position.controller

        returnPosListCtr
    ),

    fn get_pos_const inObj = (
        local returnConst = undefined
        if classOf inObj.position.controller == position_list then (
            local lst = inObj.position.controller
            local constNum = lst.getCount()
            local activeNum = lst.getActive()
            for i = 1 to constNum do (
                if (classOf lst[i].controller == Position_Constraint) then (
                    returnConst = lst[i].controller
                    if activeNum == i then return returnConst
                )
            )
        )

        if classOf inObj.position.controller == Position_Constraint then returnConst = inObj.position.controller

        return returnConst
    ),

    fn assign_pos_const inObj inTarget keepInit:false = (
        if classOf inObj.position.controller != position_list then inObj.position.controller = position_list()
        local targetPosConstraint = get_pos_const inObj
        if targetPosConstraint == undefined then (
            targetPosConstraint = Position_Constraint()
            inObj.position.controller.Available.controller = targetPosConstraint
            inObj.position.controller.setActive inObj.position.controller.count
        )

        local targetNum = targetPosConstraint.getNumTargets()
        local targetWeight = 100.0 / (targetNum + 1)
        targetPosConstraint.appendTarget inTarget targetWeight
        if targetNum > 0 then (
            local newWeightScale = 100.0 - targetWeight
            for i = 1 to targetNum do (
                local newWeight = (targetPosConstraint.GetWeight i) * 0.01 * newWeightScale
                targetPosConstraint.SetWeight i newWeight
            )
        )
        targetPosConstraint.relative = keepInit

        targetPosConstraint
    ),

    fn assign_pos_const_multi inObj inTargetArray keepInit:false = (
        for item in inTargetArray do assign_pos_const inObj item keepInit:keepInit
    ),

    fn add_target_to_pos_const inObj inTarget inWeight = (
        local targetPosConst = assign_pos_const inObj inTarget
        local targetNum = targetPosConst.getNumTargets()
        targetPosConstraint.SetWeight targetNum inWeight
    ),

    fn assign_pos_xyz inObj = (
        if classOf inObj.position.controller != position_list then inObj.position.controller = position_list()
        local posList = assign_pos_list inObj
        posList.Available.controller = Position_XYZ()
        posList.setActive posList.count
    ),

    fn get_rot_list_controller inObj = (
        local returnRotListCtr = undefined

        if classOf inObj.rotation.controller == rotation_list then returnRotListCtr = inObj.rotation.controller

        returnRotListCtr
    ),

    fn assign_rot_list inObj = (
        local returnRotListCtr = undefined

        if classOf inObj.rotation.controller != rotation_list then (
            returnRotListCtr = rotation_list()
            inObj.rotation.controller = returnRotListCtr
            return returnRotListCtr
        )
        if classOf inObj.rotation.controller == rotation_list then returnRotListCtr = inObj.rotation.controller

        returnRotListCtr
    ),

    fn get_rot_const inObj = (
        local returnConst = undefined
        if classOf inObj.rotation.controller == rotation_list then (
            local lst = inObj.rotation.controller
            local constNum = lst.getCount()
            local activeNum = lst.getActive()
            for i = 1 to constNum do (
                if (classOf lst[i].controller == Orientation_Constraint) then (
                    returnConst = lst[i].controller
                    if activeNum == i then return returnConst
                )
            )
        )

        if classOf inObj.rotation.controller == Orientation_Constraint then returnConst = inObj.rotation.controller

        return returnConst
    ),

    fn assign_rot_const inObj inTarget keepInit:false = (
        if classOf inObj.rotation.controller != rotation_list then inObj.rotation.controller = rotation_list()
        local targetRotConstraint = get_rot_const inObj
        if targetRotConstraint == undefined then (
            targetRotConstraint = Orientation_Constraint()
            inObj.rotation.controller.Available.controller = targetRotConstraint
            inObj.rotation.controller.setActive inObj.rotation.controller.count
        )

        local targetNum = targetRotConstraint.getNumTargets()
        local targetWeight = 100.0 / (targetNum + 1)
        targetRotConstraint.appendTarget inTarget targetWeight
        if targetNum > 0 then (
            local newWeightScale = 100.0 - targetWeight
            for i = 1 to targetNum do (
                local newWeight = (targetRotConstraint.GetWeight i) * 0.01 * newWeightScale
                targetRotConstraint.SetWeight i newWeight
            )
        )
        targetRotConstraint.relative = keepInit

        targetRotConstraint
    ),

    fn assign_rot_const_multi inObj inTargetArray keepInit:false = (
        for item in inTargetArray do assign_rot_const inObj item keepInit:keepInit
    ),

    fn add_target_to_rot_const inObj inTarget inWeight = (
        local targetRotConstraint = assign_rot_const inObj inTarget
        local targetNum = targetRotConstraint.getNumTargets()
        targetRotConstraint.SetWeight targetNum inWeight
    ),

    fn assign_euler_xyz inObj = (
        if classOf inObj.rotation.controller != rotation_list then inObj.rotation.controller = rotation_list()
        local rotList = assign_rot_list inObj
        rotList.Available.controller = Euler_XYZ()
        rotList.setActive rotList.count
    ),

    fn get_lookat inObj = (
        local returnConst = undefined
        if classOf inObj.rotation.controller == rotation_list then (
            local lst = inObj.rotation.controller
            local constNum = lst.getCount()
            local activeNum = lst.getActive()
            for i = 1 to constNum do (
                if (classOf lst[i].controller == LookAt_Constraint) then (
                    returnConst = lst[i].controller
                    if activeNum == i then return returnConst
                )
            )
        )

        if classOf inObj.rotation.controller == LookAt_Constraint then returnConst = inObj.rotation.controller

        return returnConst
    ),

    fn assign_lookat inObj inTarget keepInit:false = (
        if classOf inObj.rotation.controller != rotation_list then inObj.rotation.controller = rotation_list()
        local targetRotConstraint = get_lookat inObj
        if targetRotConstraint == undefined then (
            targetRotConstraint = LookAt_Constraint()
            inObj.rotation.controller.Available.controller = targetRotConstraint
            inObj.rotation.controller.setActive inObj.rotation.controller.count
        )

        local targetNum = targetRotConstraint.getNumTargets()
        local targetWeight = 100.0 / (targetNum + 1)
        targetRotConstraint.appendTarget inTarget targetWeight
        if targetNum > 0 then (
            local newWeightScale = 100.0 - targetWeight
            for i = 1 to targetNum do (
                local newWeight = (targetRotConstraint.GetWeight i) * 0.01 * newWeightScale
                targetRotConstraint.SetWeight i newWeight
            )
        )
        targetRotConstraint.relative = keepInit

        targetRotConstraint
    ),

    fn assign_lookat_multi inObj inTargetArray keepInit:false = (
        for item in inTargetArray do assign_lookat inObj item keepInit:keepInit
    ),

    fn assign_lookat_flipless inObj inTarget = (
        if (inObj.parent != undefined) then
        (
            local targetRotConstraint = rotation_script()
            targetRotConstraint.AddNode "Target" inTarget
            targetRotConstraint.AddNode "Parent" inObj.parent
            targetRotConstraint.AddObject "NodePos" inObj.pos.controller
            targetRotConstraint.script = "theTargetVector=(Target.transform.position * Inverse Parent.transform)-NodePos.value\ntheAxis=Normalize (cross theTargetVector [1,0,0])\ntheAngle=acos (dot (Normalize theTargetVector) [1,0,0])\nQuat theAngle theAxis"

            if classOf inObj.rotation.controller != rotation_list then inObj.rotation.controller = rotation_list()
            inObj.rotation.controller.Available.controller = targetRotConstraint
            inObj.rotation.controller.setActive inObj.rotation.controller.count
        )
    ),

    fn assign_rot_const_scripted inObj inTarget = (
        local targetRotConstraint = rotation_script()
        if classOf inObj.rotation.controller != rotation_list then inObj.rotation.controller = rotation_list()
        inObj.rotation.controller.Available.controller = targetRotConstraint
        inObj.rotation.controller.setActive inObj.rotation.controller.count

        local rotPointName = name.replace_type inObj.name (name.get_dummyStr())
        local rotMeasurePointNmae = name.increase_index rotPointName 1
        local rotExpName = name.replace_type inObj.name (name.get_exposeTMStr())
        rotExpName = name.replace_index rotExpName "0"

        local rotPoint = helper.create_point rotPointName size:2 boxToggle:on crossToggle:off
        local rotMeasuerPoint = helper.create_point rotMeasurePointNmae size:3 boxToggle:on crossToggle:off
        local rotExpPoint = ExposeTm name:rotExpName size:3 boxToggle:off crossToggle:on wirecolor:(color 14 255 2)

        rotPoint.transform = inObj.transform
        rotMeasuerPoint.transform = inObj.transform
        rotExpPoint.transform = inObj.transform

        rotPoint.transform.position = inTarget.transform.position
        rotMeasuerPoint.transform.position = inTarget.transform.position
        rotExpPoint.transform.position = inTarget.transform.position

        rotPoint.parent = inTarget
        rotMeasuerPoint.parent = inTarget.parent
        rotExpPoint.parent = inTarget

        rotExpPoint.exposeNode = rotPoint
        rotExpPoint.useParent = false
        rotExpPoint.localReferenceNode = rotMeasuerPoint

        local rotScript = ""
        rotScript += "local targetRot = rot.localEuler\n"
        rotScript += "local rotX = (radToDeg targetRot.x)\n"
        rotScript += "local rotY = (radToDeg targetRot.y)\n"
        rotScript += "local rotZ = (radToDeg targetRot.z)\n"
        rotScript += "local result = eulerAngles rotX rotY rotZ\n"
        rotScript += "eulerToQuat result\n"

        targetRotConstraint.AddNode "rot" rotExpPoint
        targetRotConstraint.SetExpression rotScript

        targetRotConstraint
    ),

    fn assign_scripted_lookat inOri inTarget = (
        local oriObj = inOri
        local oriParentObj = inOri.parent
        local targetObjArray = inTarget

        local objName = name.get_string oriObj.name
        local indexNum = name.get_index_as_digit oriObj.name
        local fChar = str.get_filteringChar objName
        local dummyName = name.add_prefix_to_realName objName (name.get_dummyStr()) filteringChar:fChar

        local lookAtPoint = helper.create_point (dummyName + fChar + (indexNum as String)) size:2 boxToggle:on crossToggle:off
        local lookAtMasuerPoint = helper.create_point (dummyName + fChar + ((indexNum + 1) as String)) size:3 boxToggle:on crossToggle:off
        local lookAtExpPoint = ExposeTm name:(dummyName + (name.get_exposeTMStr()) + fChar + "0") size:3 boxToggle:off crossToggle:on wirecolor:(color 14 255 2)

        lookAtPoint.transform = oriObj.transform
        lookAtMasuerPoint.transform = oriObj.transform
        lookAtExpPoint.transform = oriObj.transform

        lookAtPoint.parent = oriParentObj
        lookAtMasuerPoint.parent = oriParentObj
        lookAtExpPoint.parent = oriParentObj

        lookAtExpPoint.exposeNode = lookAtPoint
        lookAtExpPoint.useParent = false
        lookAtExpPoint.localReferenceNode = lookAtMasuerPoint

        lookAtPoint.rotation.controller = LookAt_Constraint()
        for item in targetObjArray do (
            lookAtPoint.rotation.controller.appendTarget item (1.0 / targetObjArray.count * 100.0)
        )

        local rotControll = Euler_XYZ()
        if classOf oriObj.rotation.controller != rotation_list then oriObj.rotation.controller = rotation_list()
        oriObj.rotation.controller.Available.controller = rotControll

        local rotControllerNum = oriObj.rotation.controller.count
        oriObj.rotation.controller.setname rotControllerNum "Script Rotation"

        rotControll.X_Rotation.controller = Float_Expression()
        rotControll.Y_Rotation.controller = Float_Expression()
        rotControll.Z_Rotation.controller = Float_Expression()

        rotControll.X_Rotation.controller.AddScalarTarget "rotX" lookAtExpPoint.localEulerX.controller
        rotControll.Y_Rotation.controller.AddScalarTarget "rotY" lookAtExpPoint.localEulerY.controller
        rotControll.Z_Rotation.controller.AddScalarTarget "rotZ" lookAtExpPoint.localEulerZ.controller

        rotControll.X_Rotation.controller.SetExpression "rotX"
        rotControll.Y_Rotation.controller.SetExpression "rotY"
        rotControll.Z_Rotation.controller.SetExpression "rotZ"

        rotControll.X_Rotation.controller.Update()
        rotControll.Y_Rotation.controller.Update()
        rotControll.Z_Rotation.controller.Update()
    ),

    fn assign_attachment inPlacedObj inSurfObj bAlign:false shiftAxis:[0,0,1] shiftAmount:3.0 = (
        local placedObjTm = inPlacedObj.transform
        PreTranslate placedObjTm (shiftAxis * (-shiftAmount))
        local dirStartPos = placedObjTm.pos
        dirStartPos = placedObjTm.pos

        placedObjTm = inPlacedObj.transform
        PreTranslate placedObjTm (shiftAxis * shiftAmount)
        local dirEndPos = placedObjTm.pos
        dirEndPos = placedObjTm.pos

        local dirVec = dirEndPos - dirStartPos
        local dirRay = ray dirEndPos -dirVec
        local intersectArr = (intersectRayEx inSurfObj dirRay)

        if intersectArr != undefined then (
            local posListConst = assign_pos_list inPlacedObj
            local attConst = attachment()

            posListConst.Available.controller = attConst
            attConst.node = inSurfObj
            attConst.align = bAlign

            attachKey = attachCtrl.addNewKey attConst 0
            attachKey.face = intersectArr[2] - 1
            attachKey.coord = intersectArr[3]

            return attConst
        )
        else return undefined
    ),

    fn get_pos_controllers_name_from_list inObj = (
        local returnNameArray = #()

        if classOf inObj.position.controller == position_list then (
            local posList = inObj.position.controller
            for i = 1 to posList.count do append returnNameArray posList.getName i
        )

        returnNameArray
    ),

    fn get_pos_controllers_weight_from_list inObj = (
        local returnWeightArray = #()

        if classOf inObj.position.controller == position_list then (
            local posList = inObj.position.controller
            returnWeightArray = posList.weight
        )

        returnWeightArray
    ),

    fn set_pos_controllers_name_in_list inObj inLayerNum inNewName = (
        local listCtr = get_pos_list_controller inObj
        if listCtr != undefined then listCtr.setName inLayerNum inNewName
    ),

    fn set_pos_controllers_weight_in_list inObj inLayerNum inNewWeight = (
        local listCtr = get_pos_list_controller inObj
        if listCtr != undefined then listCtr.weight[inLayerNum] = inNewWeight
    ),

    fn get_rot_controllers_name_from_list inObj = (
        local returnNameArray = #()

        if classOf inObj.rotation.controller == position_list then (
            local rotList = inObj.rotation.controller
            for i = 1 to rotList.count do append returnNameArray rotList.getName i
        )

        returnNameArray
    ),

    fn get_rot_controllers_weight_from_list inObj = (
        local returnWeightArray = #()

        if classOf inObj.rotation.controller == position_list then (
            local rotList = inObj.rotation.controller
            returnWeightArray = rotList.weight
        )

        returnWeightArray
    ),

    fn set_rot_controllers_name_in_list inObj inLayerNum inNewName = (
        local listCtr = get_rot_list_controller inObj
        if listCtr != undefined then listCtr.setName inLayerNum inNewName
    ),

    fn set_rot_controllers_weight_in_list inObj inLayerNum inNewWeight = (
        local listCtr = get_rot_list_controller inObj
        if listCtr != undefined then listCtr.weight[inLayerNum] = inNewWeight
    )
)
