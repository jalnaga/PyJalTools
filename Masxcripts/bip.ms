struct _Bip (
    anim, name, bone,

    fn get_bips = 
    (
        local returnArray = for i in objects where isKindOf i Biped_Object collect i
        returnArray
    ),

    fn get_coms_name = 
    (
        local bips = get_bips()
        local bipComsName = #()
        for obj in bips do appendIfUnique bipComsName obj.controller.rootName

        bipComsName
    ),

    fn get_coms = 
    (
        local bips = get_bips()
        local bipComs = #()
        for obj in bips do appendIfUnique bipComs obj.controller.rootNode

        bipComs
    ),

    fn is_biped_object inObj = ((classOf inObj.controller == BipSlave_control) or (classOf inObj.controller == Footsteps) or (classOf inObj.controller == Vertical_Horizontal_Turn)),

    fn get_com inBip = 
    (
        local returnVal = undefined
        if (is_biped_object inBip) then 
        (
            returnVal = inBip.controller.rootNode
        )
        returnVal
    ),

    fn get_all inBip = 
    (
        local returnVal = #()
        if (is_biped_object inBip) then 
        (
            local root = get_com inBip
            local all = #(root)
            returnVal = #(root)

            for obj in all do (
                for child in obj.children do 
                (
                    appendIfUnique all child
                    if (is_biped_object child) then appendIfUnique returnVal child
                )
                if obj.parent != undefined then 
                (
                    appendIfUnique all obj.parent
                    if (is_biped_object obj.parent) then appendIfUnique returnVal obj.parent
                )
            )
        )

        returnval
    ),

    fn get_nodes inBip = 
    (
        local returnVal = #()
        if (is_biped_object inBip) then 
        (
            local root = get_com inBip
            local all = #(root)
            returnVal = #(root)

            for obj in all do 
            (
                for child in obj.children do 
                (
                    if (classof child != Dummy and classOf child.controller != Footsteps) then 
                    (
                        appendIfUnique all child
                        if (is_biped_object child) then appendIfUnique returnVal child
                    )
                )
                if obj.parent != undefined then 
                (
                    if (classof obj.parent != Dummy and classOf obj.parent.controller != Footsteps) then 
                    (
                        appendIfUnique all obj.parent
                        if (is_biped_object obj.parent) then appendIfUnique returnVal obj.parent
                    )
                )
            )
        )

        returnval
    ),

    fn get_dummy_and_footstep inBip = 
    (
        local returnVal = #()
        if (is_biped_object inBip) then 
        (
            local bipArray = get_all inBip
            returnVal = for item in bipArray where (classof item == Dummy or classOf item.controller == Footsteps) collect item
        )

        returnVal
    ),

    fn get_nodes_by_skeleton_order inBip = 
    (
        if (classOf inBip) != Biped_Object then return #()
        local com = inBip.controller.rootNode

        local head = biped.getNode com #head
        local hips = biped.getNode com #pelvis
        local lArm = biped.getNode com #larm link:2
        local lClavicle = biped.getNode com #larm link:1
        local lFoot = biped.getNode com #lleg link:3
        local lToe = biped.getNode com #ltoes link:1
        local lForeArm = biped.getNode com #larm link:3
        local lHand = biped.getNode com #larm link:4
        local lHandIndex = biped.getNode com #lfingers link:5
        local lHandIndex1 = biped.getNode com #lfingers link:6
        local lHandIndex2 = biped.getNode com #lfingers link:7
        local lHandIndex3 = biped.getNode com #lfingers link:8
        local lHandMiddle = biped.getNode com #lfingers link:9
        local lHandMiddle1 = biped.getNode com #lfingers link:10
        local lHandMiddle2 = biped.getNode com #lfingers link:11
        local lHandMiddle3 = biped.getNode com #lfingers link:12
        local lHandPinky = biped.getNode com #lfingers link:17
        local lHandPinky1 = biped.getNode com #lfingers link:18
        local lHandPinky2 = biped.getNode com #lfingers link:19
        local lHandPinky3 = biped.getNode com #lfingers link:20
        local lHandRing = biped.getNode com #lfingers link:13
        local lHandRing1 = biped.getNode com #lfingers link:14
        local lHandRing2 = biped.getNode com #lfingers link:15
        local lHandRing3 = biped.getNode com #lfingers link:16
        local lHandThumb1 = biped.getNode com #lfingers link:1
        local lHandThumb2 = biped.getNode com #lfingers link:2
        local lHandThumb3 = biped.getNode com #lfingers link:3
        local lLeg = biped.getNode com #lleg link:2
        local lUpLeg = biped.getNode com #lleg link:1
        local neck = biped.getNode com #neck link:1
        local neck1 = biped.getNode com #neck link:2
        local rArm = biped.getNode com #rarm link:2
        local rClavicle = biped.getNode com #rarm link:1
        local rFoot = biped.getNode com #rleg link:3
        local rToe = biped.getNode com #rtoes link:1
        local rForeArm = biped.getNode com #rarm link:3
        local rHand = biped.getNode com #rarm link:4
        local rHandIndex = biped.getNode com #rfingers link:5
        local rHandIndex1 = biped.getNode com #rfingers link:6
        local rHandIndex2 = biped.getNode com #rfingers link:7
        local rHandIndex3 = biped.getNode com #rfingers link:8
        local rHandMiddle = biped.getNode com #rfingers link:9
        local rHandMiddle1 = biped.getNode com #rfingers link:10
        local rHandMiddle2 = biped.getNode com #rfingers link:11
        local rHandMiddle3 = biped.getNode com #rfingers link:12
        local rHandPinky = biped.getNode com #rfingers link:17
        local rHandPinky1 = biped.getNode com #rfingers link:18
        local rHandPinky2 = biped.getNode com #rfingers link:19
        local rHandPinky3 = biped.getNode com #rfingers link:20
        local rHandRing = biped.getNode com #rfingers link:13
        local rHandRing1 = biped.getNode com #rfingers link:14
        local rHandRing2 = biped.getNode com #rfingers link:15
        local rHandRing3 = biped.getNode com #rfingers link:16
        local rHandThumb1 = biped.getNode com #rfingers link:1
        local rHandThumb2 = biped.getNode com #rfingers link:2
        local rHandThumb3 = biped.getNode com #rfingers link:3
        local rLeg = biped.getNode com #rleg link:2
        local rUpLeg = biped.getNode com #rleg link:1
        local spine = biped.getNode com #spine link:1
        local spine1 = biped.getNode com #spine link:2
        local spine2 = biped.getNode com #spine link:3

        local bipNodeArray = #(head, hips, lArm, lClavicle, lFoot, lToe, lForeArm, lHand, lHandIndex, lHandIndex1, lHandIndex2, lHandIndex3, lHandMiddle, lHandMiddle1, lHandMiddle2, lHandMiddle3, lHandPinky, lHandPinky1, lHandPinky2, lHandPinky3, lHandRing, lHandRing1, lHandRing2, lHandRing3, lHandThumb1, lHandThumb2, lHandThumb3, lLeg, lUpLeg, neck, neck1, rArm, rClavicle, rFoot, rToe, rForeArm, rHand, rHandIndex, rHandIndex1, rHandIndex2, rHandIndex3, rHandMiddle, rHandMiddle1, rHandMiddle2, rHandMiddle3, rHandPinky, rHandPinky1, rHandPinky2, rHandPinky3, rHandRing, rHandRing1, rHandRing2, rHandRing3, rHandThumb1, rHandThumb2, rHandThumb3, rLeg, rUpLeg, spine, spine1, spine2)

        bipNodeArray
    ),

    fn load_bip_file inBipRoot inFile = 
    (
        local bipNodeArray = get_all inBipRoot

        inBipRoot.controller.figureMode = False
        biped.loadBipFile inBipRoot.controller inFile
        inBipRoot.controller.figureMode = True
        inBipRoot.controller.figureMode = False

        keyRange = #()
        for i=2 to bipNodeArray.count where (bipNodeArray[i].controller.keys.count != 0) and (bipNodeArray[i].controller.keys.count != -1) do
            appendIfUnique keyRange bipNodeArray[i].controller.keys[bipNodeArray[i].controller.keys.count].time
        if (aMax keyRange) !=0 then animationRange = interval 0 (aMax keyRange)
        sliderTime = 0
    ),

    fn load_fig_file inBipRoot inFile = 
    (
        inBipRoot.controller.figureMode = False
        inBipRoot.controller.figureMode = True
        biped.LoadFigFile inBipRoot.controller inFile
        inBipRoot.controller.figureMode = False
    ),
    
    fn save_fig_file inBipRoot file_name = 
    (
        inBipRoot.controller.figureMode = False
        inBipRoot.controller.figureMode = True
        biped.saveFigFile inBipRoot.controller file_name
    ),

    fn turn_on_figureMode inBip = 
    (
        inBip.controller.figureMode = true
    ),

    fn turn_off_figureMode inBip = 
    (
        inBip.controller.figureMode = false
    ),

    fn delete_copyCollection inBip inName = 
    (
        if ( this.is_biped_object inBip ) then 
        (
            local colNum = biped.numCopyCollections inBip.controller
            if colNum > 0 then 
            (
                for i = 1 to colNum do 
                (
                    if (biped.getCopyCollection inBip.controller i).name == inName then 
                    (
                        biped.deleteCopyCollection inBip.controller i
                        exit
                    )
                )
            )
        )
    ),

    fn link_base_skeleton = (
        setWaitCursor()
        local skinBoneBaseName = "b"

        local bip_skel = get_bips()
        local base_skel = #()
        for i = 1 to bip_skel.count do (
            local baseSkeletonName = name.replace_base bip_skel[i].name skinBoneBaseName
            baseSkeletonName = name.replace_filteringChar baseSkeletonName "_"
            local baseSkel = getNodeByName baseSkeletonName
            if (isValidObj baseSkel) then (
                base_skel[i] = baseSkel
            )
        )

        anim.save_xform bip_skel
        anim.set_xform bip_skel

        anim.save_xform base_skel
        anim.set_xform base_skel

        for i = 1 to base_skel.count do (
            if base_skel[i] != undefined then (
                base_skel[i].scale.controller = (scaleXYZ())
                base_skel[i].controller = (link_constraint())

                anim.set_xform #(base_skel[i]) space:#world
                base_skel[i].transform.controller.AddTarget (bip_skel[i]) 0
            )
        )
        for i = 1 to base_skel.count do if base_skel[i] != undefined then base_skel[i].boneEnable = true
        setArrowCursor()
    ),

    fn unlink_base_skeleton = (
        setWaitCursor()
        local skinBoneBaseName = "b"

        local bip_skel = get_bips()
        local base_skel = #()
        for i = 1 to bip_skel.count do (
            local baseSkeletonName = name.replace_base bip_skel[i].name skinBoneBaseName
            baseSkeletonName = name.replace_filteringChar baseSkeletonName "_"
            local baseSkel = getNodeByName baseSkeletonName
            if (isValidObj baseSkel) then (
                base_skel[i] = baseSkel
            )
        )

        anim.save_xform bip_skel
        anim.set_xform bip_skel

        anim.save_xform base_skel
        anim.set_xform base_skel

        for i = 1 to base_skel.count do
        (
            if base_skel[i] != undefined then (
                base_skel[i].controller = (prs())
                anim.set_xform #(base_skel[i]) space:#world
            )
        )
        for i = 1 to base_skel.count do if base_skel[i] != undefined then base_skel[i].boneEnable = true
        setArrowCursor()
    )
)
