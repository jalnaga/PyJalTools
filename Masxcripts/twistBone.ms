struct _TwistBone (
    name, anim, helper, bone, const, bip,

    baseName = "",
    filteringChar = " ",
    bipObj = undefined,
    upperArmNum = 0,
    foreArmNum = 0,
    thighNum = 0,
    calfNum = 0,
    boneSize = 2.0,
    lUpperArmBoneArray = #(),
    rUpperArmBoneArray = #(),
    lForeArmBoneArray = #(),
    rForeArmBoneArray = #(),
    lThighBoneArray = #(),
    rThighBoneArray = #(),
    lCalfBoneArray = #(),
    rCalfBoneArray = #(),

    thighExpression = "",
    thighExtraExpression = "",
    calfExpression = "",
    calfExtraExpression = "",

    upperArmExpression = "",
    upperArmExtraExpression = "",
    lForeArmExpression = "",
    rForeArmExpression = "",
    foreArmExtraExpression = "",

    fn create_bones inObj inChild inTwistNum inExpression inExtraExpression inControllerLimb inWeightVar = (
        local Limb = inObj
        local distanceVar = (distance Limb inChild)

        local TBExpression=""
        local ControllerLimb = inControllerLimb
        local weightVar = inWeightVar

        TBExpression = inExpression

        local boneChainArray = #()
        
        local TwistBone = BoneSys.createBone Limb.transform.position inChild.transform.position [0,0,1]
        local boneName = (name.get_string inObj.name) + "Twist"
        TwistBone.name = name.replace_index boneName "0"
        TwistBone.transform = Limb.transform
        TwistBone.parent = Limb
        TwistBone.Length = distanceVar/inTwistNum
        TwistBone.Width = distanceVar/8
        TwistBone.Height = TwistBone.Width
        TwistBone.taper = 0
        TwistBone.sidefins = off
        TwistBone.frontfin = off
        TwistBone.backfin = off
        TwistBone.rotation.controller = Rotation_List()
        TwistBone.rotation.controller[1].controller = rotation_script()
        TwistBone.rotation.controller[1].AddNode "Limb" ControllerLimb
        TwistBone.rotation.controller[1].SetExpression TBExpression
        TwistBone.rotation.controller.weight[1] = weightVar
        
        append boneChainArray TwistBone
        
        local TBExtraController = rotation_script()
        if (matchPattern inExtraExpression pattern:"*\nTB.*") then (
            TBExtraController.AddNode "TB" TwistBone
        )
        else (
            TBExtraController.AddNode "Limb" Limb
            TBExtraController.AddNode "LimbParent" TwistBone 
        )
        TBExtraController.setExpression inExtraExpression
        
        local PrevTBE = TwistBone
        
        if inTwistNum > 1 then (
            for j = 2 to (inTwistNum - 1) do
            (
                local TwistBoneExtra = BoneSys.createBone [0,0,0] [1,0,0] [0,0,1]
                local matAux = matrix3 1
                matAux.position = [(distanceVar/inTwistNum), 0, 0]
                TwistBoneExtra.transform = matAux*PrevTBE.transform
                TwistBoneExtra.name = name.replace_index boneName ((j-1) as string)
                TwistBoneExtra.parent = PrevTBE
                TwistBoneExtra.Length = distanceVar/inTwistNum
                TwistBoneExtra.Width = PrevTBE.Width
                TwistBoneExtra.Height = PrevTBE.Height
                TwistBoneExtra.taper = 0
                TwistBoneExtra.sidefins = off
                TwistBoneExtra.frontfin = off
                TwistBoneExtra.backfin = off
                TwistBoneExtra.rotation.controller = Rotation_List()
                TwistBoneExtra.rotation.controller[1].controller = TBExtraController
                TwistBoneExtra.rotation.controller.weight[1] = 100/(inTwistNum - 1)
                PrevTBE = TwistBoneExtra
                
                append boneChainArray TwistBoneExtra
            )
            
            local TwistBoneEnd = BoneSys.createBone [0,0,0] [1,0,0] [0,0,1] 
            local matAux = matrix3 1
            
            matAux.position = [(distanceVar/inTwistNum), 0, 0]
            TwistBoneEnd.transform = matAux*PrevTBE.transform
            TwistBoneEnd.name = name.replace_index boneName ((inTwistNum-1) as string)
            TwistBoneEnd.parent = inObj
            TwistBoneEnd.Length = distanceVar/inTwistNum
            TwistBoneEnd.Width = PrevTBE.Width
            TwistBoneEnd.Height = PrevTBE.Height
            TwistBoneEnd.taper = 0
            TwistBoneEnd.sidefins = off
            TwistBoneEnd.frontfin = off
            TwistBoneEnd.backfin = off
            
            append boneChainArray TwistBoneEnd
        )

        boneChainArray
    ),

    fn reorder_bones inBoneChainArray = (
        local boneChainArray = deepCopy inBoneChainArray
        local returnBoneArray = #()

        local firstBone = boneChainArray[1]
        local lastBone = boneChainArray[boneChainArray.count]
        append returnBoneArray lastBone

        if boneChainArray.count > 1 then (
            anim.move_local firstBone firstBone.length 0 0
            anim.move_local lastBone -(firstBone.length * (boneChainArray.count-1)) 0 0
        )

        for i = 1 to boneChainArray.count-1 do append returnBoneArray boneChainArray[i]
        for i = 1 to returnBoneArray.count do returnBoneArray[i].name = name.replace_index boneChainArray[i].name ((i-1) as string)

        returnBoneArray
    ),

    fn create_upperArm_type inObj inTwistNum = (
        if inObj.parent == undefined or inObj.children.count == 0 then return false

        local controllerLimb = undefined
        local weightVal = 100

        create_bones inObj inObj.children[1] inTwistNum upperArmExpression upperArmExtraExpression inObj weightVal
    ),

    fn create_foreArm_type inObj inTwistNum side:#left = (
        if inObj.parent == undefined or inObj.children.count == 0 then return false

        local controllerLimb = undefined
        local weightVal = 100

        local TBExpression = ""

        if side == #left then TBExpression = lForeArmExpression else TBExpression = rForeArmExpression

        if side == #left then controllerLimb = biped.getNode inObj.controller.rootNode #larm link:4 else controllerLimb = biped.getNode inObj.controller.rootNode #rarm link:4

        if inTwistNum > 1 then weightVal = 100/inTwistNum

        reorder_bones (create_bones inObj controllerLimb inTwistNum TBExpression foreArmExtraExpression controllerLimb weightVal)
    ),

    fn create_thigh_type inObj inTwistNum = (
        if inObj.parent == undefined or inObj.children.count == 0 then return false

        local controllerLimb = undefined
        local weightVal = 100

        create_bones inObj inObj.children[1] inTwistNum thighExpression thighExtraExpression inObj weightVal
    ),

    fn create_calf_type inObj inTwistNum side:#left = (
        if inObj.parent == undefined or inObj.children.count == 0 then return false

        local controllerLimb = undefined
        local weightVal = 100

        if side == #left then controllerLimb = biped.getNode inObj.controller.rootNode #lleg link:3 else controllerLimb = biped.getNode inObj.controller.rootNode #rleg link:3

        if inTwistNum > 1 then weightVal = 100/inTwistNum

        reorder_bones (create_bones inObj controllerLimb inTwistNum calfExpression calfExtraExpression controllerLimb weightVal)
    ),

    fn create_bend_type = (
    ),

    on create do (
        thighExpression = ""
        thighExpression += "try(\n"
        thighExpression += "TM=Limb.transform*inverse Limb.parent.transform\n"
        thighExpression += "vector=normalize (cross -TM.row1 [1,0,0])\n"
        thighExpression +=  "angle=acos -(normalize TM.row1).x\n"
        thighExpression += "(quat 0 1 0 0)*(quat angle vector)*inverse TM.rotation)\n"
        thighExpression += "catch((quat 0 0 0 1))"

        thighExtraExpression = ""
        thighExtraExpression += "try(\n"
        thighExtraExpression += "(Limb.transform*inverse LimbParent.transform).rotation\n"
        thighExtraExpression += ")catch((quat 0 0 0 1))"

        calfExpression = ""
        calfExpression += "try(\n"
        calfExpression += "TM=Limb.transform*inverse Limb.parent.transform\n"
        calfExpression += "vector=normalize (cross TM.row1 [1,0,0])\n"
        calfExpression += "angle=acos (normalize TM.row1).x\n"
        calfExpression += "TM.rotation*(quat -angle vector))\n"
        calfExpression += "catch((quat 0 0 0 1))"

        calfExtraExpression = "try(dependson TB\nTB.rotation.controller[1].value\n)catch((quat 0 0 0 1))"

        upperArmExpression = ""
        upperArmExpression += "try(\n"
        upperArmExpression += "TM=Limb.transform*inverse Limb.parent.transform\n"
        upperArmExpression += "vector=normalize (cross TM.row1 [1,0,0])\n"
        upperArmExpression += "angle=acos (normalize TM.row1).x\n"
        upperArmExpression += "(quat angle vector)*inverse TM.rotation)\n"
        upperArmExpression += "catch((quat 0 0 0 1))"

        upperArmExtraExpression = ""
        upperArmExtraExpression += "try(\n"
        upperArmExtraExpression += "(Limb.transform*inverse LimbParent.transform).rotation\n"
        upperArmExtraExpression += ")catch((quat 0 0 0 1))"

        rForeArmExpression = ""
        rForeArmExpression += "try(\n"
        rForeArmExpression += "TM=(matrix3 [1,0,0] [0,0,-1] [0,1,0] [0,0,0])*Limb.transform*inverse Limb.parent.transform\n"
        rForeArmExpression += "vector=normalize (cross TM.row1 [1,0,0])\n"
        rForeArmExpression += "angle=acos (normalize TM.row1).x\n"
        rForeArmExpression += "TM.rotation*(quat -angle vector))\n"
        rForeArmExpression += "catch((quat 0 0 0 1))"

        lForeArmExpression = ""
        lForeArmExpression += "try(\n"
        lForeArmExpression += "TM=(matrix3 [1,0,0] [0,0,1] [0,-1,0] [0,0,0])*Limb.transform*inverse Limb.parent.transform\n"
        lForeArmExpression += "vector=normalize (cross TM.row1 [1,0,0])\n"
        lForeArmExpression += "angle=acos (normalize TM.row1).x\n"
        lForeArmExpression += "TM.rotation*(quat -angle vector))\n"
        lForeArmExpression += "catch((quat 0 0 0 1))"

        foreArmExtraExpression = "try(dependson TB\nTB.rotation.controller[1].value\n)catch((quat 0 0 0 1))"
    )
)
