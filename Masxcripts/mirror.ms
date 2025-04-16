struct _Mirror (
    name, bone,

    fn mirror_matrix mAxis:"x" mFlip:"x" tm:(matrix3 1) pivotTm:(matrix3 1) = (
       fn fetch_reflection a = (
          case a of (
          "x": [-1,1,1]  -- reflect in YZ plane
          "y": [1,-1,1]  --     in ZX plane
          "z": [1,1,-1]  --     in XY plane
          default: [1,1,1]
          )
       )

       aReflection = scalematrix (fetch_reflection mAxis)
       fReflection = scalematrix (fetch_reflection mFlip)

       --calculate the mirroredTM
       --fReflection * (tm * (inverse pivotTm)) * aReflection * pivotTm
       fReflection * tm * aReflection * pivotTm
    ),

    fn apply_mirror inObj axis:1 flip:2 pivotObj:undefined cloneStatus:2 negative:false = (
        local axisArray = #("x", "y", "z", "none")
        local copyObj = copy inObj
        local objTm = inObj.transform
        local pivotTm = (matrix3 1)
        local mirrorAxisIndex = axis
        local flipAxisIndex = flip
        local copyObjName = name.gen_mirroring_name inObj.name axis:axis

        if pivotObj != undefined then pivotTm = pivotObj.transform
        if negative == true then flipAxisIndex = 4
        
        copyObj.name = copyObjName
        copyObj.parent = undefined
        copyObj.wirecolor = inObj.wirecolor
        
        case cloneStatus of (
            1: (
                delete copyObj
                copyObj = undefined
                inObj.transform = mirror_matrix mAxis:axisArray[mirrorAxisIndex] mFlip:axisArray[flipAxisIndex] tm:objTm pivotTm:pivotTm
                copyObj = inObj
            )
            2: (
                copyObj.transform = mirror_matrix mAxis:axisArray[mirrorAxisIndex] mFlip:axisArray[flipAxisIndex] tm:objTm pivotTm:pivotTm
            )
            3: (
                delete copyObj
                copyObj = undefined
                copyObj = (snapShot inObj)
                copyObj.transform = mirror_matrix mAxis:axisArray[mirrorAxisIndex] mFlip:axisArray[flipAxisIndex] tm:objTm pivotTm:pivotTm
            )
        )

        return copyObj
    ),

    fn mirror_object inObjArray mAxis:1 pivotObj:undefined cloneStatus:2 = (
        local returnArray = for i = 1 to inObjArray.count collect (apply_mirror inObjArray[i] axis:mAxis pivotObj:pivotObj cloneStatus:cloneStatus negative:true)

        returnArray
    ),

    fn mirror_without_negative inMirrorObjArray mAxis:1 pivotObj:undefined cloneStatus:2 = (
        --mirrorAxis labels:#("XY", "XZ", "YX", "YZ", "ZX", "ZY")
        local axisIndex = 1
        local flipIndex = 1

        case mAxis of (
            1: (
                axisIndex = 1
                flipIndex = 2
            )
            2: (
                axisIndex = 1
                flipIndex = 3
            )
            3: (
                axisIndex = 2
                flipIndex = 1
            )
            4: (
                axisIndex = 2
                flipIndex = 3
            )
            5: (
                axisIndex = 3
                flipIndex = 1
            )
            6: (
                axisIndex = 3
                flipIndex = 2
            )
            default: (
                axisIndex = 1
                flipIndex = 1
            )
        )
        local returnArray = for i = 1 to inMirrorObjArray.count collect (apply_mirror inMirrorObjArray[i] axis:axisIndex flip:flipIndex pivotObj:pivotObj cloneStatus:cloneStatus negative:false)

        returnArray
    ),

    fn mirror_bone inBoneArray mAxis:1 flipZ:false offset:0.0 = (
        local bones = bone.sort_bones_as_hierarchy inBoneArray
        local axisFactor = [1,1,1]
        case mAxis of (
            1: axisFactor = [-1,1,1]
            2: axisFactor = [1,-1,1]
            3: axisFactor = [1,1,-1]
        )
        -- prepare the storage for the new bones and their parents
        local parents = #()
        local created = #()
        local root    = bones[1].transform.translation
        created.count = 0
        
        -- loop through the sorted selection so that the hierarchy is browsed from top to bottom
        for i = 1 to bones.count do (
            local original = bones[i]
            if (classof original != BoneGeometry) do -- not a real bone
            (
                append parents undefined --no parent will be assigned. undefined is added only to keep the numbering
                continue
            )

            -- take the start point, end point and the Z axis from the original bone                
            local boneStart  = original.pos
            local boneEnd    = bone.get_bone_end_position original
            local boneZ      = original.dir
            
            -- apply mirroring to the start and end points
            for k = 1 to 3 do (
                if ( axisFactor[k] < 0 ) do
                (
                  boneStart [k] = 2.0*root[k] - boneStart[k] + offset
                  boneEnd   [k] = 2.0*root[k] - boneEnd  [k] + offset
                  boneZ     [k] = -boneZ[k]
                )
            )

            -- flip the bone's Z axis if the flipZ argument says so
            if ( flipZ ) do boneZ = -boneZ

            -- create the reflection of the original bone               
            local reflection              = bonesys.createbone boneStart boneEnd boneZ
            
            -- copy all applicable parameters from the original bone to the reflection
            reflection.backfin            = original.backfin
            reflection.backfinendtaper    = original.backfinendtaper
            reflection.backfinsize        = original.backfinsize 
            reflection.backfinstarttaper  = original.backfinstarttaper
            reflection.frontfin           = original.frontfin
            reflection.frontfinendtaper   = original.frontfinendtaper
            reflection.frontfinsize       = original.frontfinsize
            reflection.frontfinstarttaper = original.frontfinstarttaper
            reflection.height             = original.height
            if ((name.has_side original.name) or (name.has_front_back original.name)) then reflection.name = (name.gen_mirroring_name original.name axis:mAxis)
            else reflection.name = name.add_sufix_to_realName original.name "Mirrored"
            reflection.sidefins           = original.sidefins 
            reflection.sidefinsendtaper   = original.sidefinsendtaper
            reflection.sidefinssize       = original.sidefinssize
            reflection.sidefinsstarttaper = original.sidefinsstarttaper
            reflection.taper              = original.taper
            reflection.width              = original.width
            reflection.wirecolor          = original.wirecolor

            append created reflection
            append parents reflection
        )

        for i = created.count to 2 by -1 do (
            local pIndex = findItem bones bones[i].parent
            if pIndex != 0 then created[i].parent = parents[pIndex]
        )
        created[1].parent = bones[1].parent
        for i = 1 to created.count do (
            if created[i].parent == undefined then created[i].position = bones[i].position * axisFactor
        )

        return created
    ),

    fn mirror_geo inMirrorObjArray mAxis:1 pivotObj:undefined cloneStatus:2 = (
        local mirroredArray = mirror_object inMirrorObjArray mAxis:mAxis pivotObj:pivotObj cloneStatus:cloneStatus
        local resetXformArray = #()
        local nonResetXformArray = #()
        local returnArray = #()

        for item in mirroredArray do (
            local caseIndex = 0
            if classOf item == Editable_Poly then caseIndex += 1
            if classOf item == Editable_mesh then caseIndex += 1
            if item.modifiers.count > 0 then caseIndex += 1

            case caseIndex of (
                1: append resetXformArray item
                default: append nonResetXformArray item
            )
        )

        for item in resetXformArray do (
            ResetXForm item
            local tempNormalMod = normalModifier()
            tempNormalMod.flip = true
            addModifier item tempNormalMod
            collapseStack item
        )
        
        join returnArray resetXformArray
        join returnArray nonResetXformArray

        returnArray
    )
)
