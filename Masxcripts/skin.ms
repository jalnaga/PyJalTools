/**************************************/
/* Skin Library
/**************************************/

struct _SkinVert (
    index,
    boneArray = #(),
    boneIDArray = #(),
    boneNameArray = #(),
    weightArray = #()
)

struct _Skin (
    name,

    prog,

    skinMod,
    modIndex = 0,
    allBoneNamesArray = #(),
    allBonesArray = #(),
    skinWeightsArray = #(),

    fn has_skin obj:selection[1] = ( if (for m in obj.modifiers where classOf m == Skin collect m).count != 0 then True else false ),

    fn is_valide_bone n = ( superClassOf n == GeometryClass or classOf n == BoneGeometry or superClassOf n == helper),

    fn get_skin_mod obj:selection[1] = (for mod in obj.modifiers where (classOf mod == Skin) collect mod),

    fn find_skin inputObj = (
        local returnVal = 0
        if inputObj.modifiers.count == 0 then return returnVal
        for i = 1 to inputObj.modifiers.count do (
            if (classof inputObj.modifiers[i]) == Skin then (
                skinMod = inputObj.modifiers[i]
                modIndex = i
                returnVal = i
            )
        )

        returnVal
    ),

    fn select_skinObj inputObj = (
        local returnVal = false
        if (find_skin inputObj) == 0 then return returnVal

        max modify mode
        select inputObj
        modPanel.setCurrentObject inputObj.modifiers[modIndex]
        subobjectLevel = 1
        returnVal = true
        returnVal
    ),

    fn remove_unused_bones inputObj weightThresh:0.0001 = (
        local returnVal = false
        if not(select_skinObj inputObj) then return returnVal

        local vertCount = skinOps.GetNumberVertices skinMod
        local bonesCount = skinOps.GetNumberBones skinMod
        local unusedBones = #{1..bonesCount}

        for v = 1 to vertCount do (
            local vertWeightCount = skinOps.GetVertexWeightCount skinMod v

            for i = 1 to vertWeightCount do (
                local weight = skinOps.GetVertexWeight skinMod v i
                if weight >= weightThresh then (
                    local boneID = skinOps.GetVertexWeightBoneID skinMod v i
                    unusedBones[boneID] = false
                )
            )
        )

        for i = bonesCount to 1 by -1 where unusedBones[i] do (
            skinOps.SelectBone skinMod i
            skinOps.RemoveBone skinMod
        )

        returnVal = true
        returnVal
    ),

    fn get_bones_from_skin objs skinModIndex = (
        infList = #()
        -- filter
        fn is_bone n = (superClassOf n == GeometryClass or classOf n == BoneGeometry or superClassOf n == helper)

        for obj in objs where isValidNode obj do (
            for n in (refs.dependsOn obj.modifiers[skinModIndex]) where isValidNode n and is_bone n do appendIfUnique infList n
        )
        return infList
    ),

    fn get_bone_index inputObj targetBone = (
        local returnVal = 0
        if allBonesArray.count > 0 then (
            local boneID = findItem allBonesArray targetBone
            returnVal = boneID
        )

        returnVal
    ),

    fn round_number num precision:3 = (
        local multiplier = 10 ^ precision
        ( floor ( (num * multiplier) + 0.5) ) / multiplier
    ),

    fn get_selected_skinVerts inputObj = (
        local returnVal = #()
        if not(select_skinObj inputObj) then return returnVal
        returnVal = for v = 1 to skinOps.GetNumberVertices skinMod where skinOps.IsVertexSelected skinMod v == 1 collect v

        returnVal
    ),

    fn get_vert_weight inputObj inVertIndex = (
        local returnVal = _SkinVert()
        if allBonesArray.count == 0 then (
            get_all_bones inputObj
            if allBonesArray.count == 0 then return returnVal
        )

        local boneArray = #()
        local boneIDArray = #()
        local boneNameArray = #()
        local weightArray = #()
        local boneNum = skinOps.getVertexWeightCount skinMod inVertIndex

        for i = 1 to boneNum do (
            local boneID = skinOps.getVertexWeightBoneID skinMod inVertIndex i
            local boneName = skinOps.GetBoneName skinMod boneID 0
            local boneSysID = findItem allBoneNamesArray boneName
            local boneWeight = skinOps.getVertexWeight skinMod inVertIndex i
            append boneArray allBonesArray[boneSysID]
            append boneIDArray boneID
            append boneNameArray boneName
            append weightArray (round_number boneWeight)
        )

        returnVal.index = inVertIndex
        returnVal.boneArray = deepCopy boneArray
        returnVal.boneIDArray = deepCopy boneIDArray
        returnVal.boneNameArray = deepCopy boneNameArray
        returnVal.weightArray = deepCopy weightArray

        returnVal
    ),

    fn get_skin_weights inputObj = (
        local returnVal = #()
        if allBonesArray.count > 0 then (
            skinWeightsArray = #()
            local numVerts = skinOps.GetNumberVertices skinMod
            for i = 1 to numVerts do (
                append skinWeightsArray (get_vert_weight inputObj i)
            )
            returnVal = deepCopy skinWeightsArray
        )
        returnVal
    ),

    fn select_zeroWeight_vertex inputObj = (
        local returnArray = #()
        if not(select_skinObj inputObj) then return returnArray

        local numVerts = skinOps.GetNumberVertices skinMod
        for v = 1 to numVerts do (
            local weights = (get_vert_weight inputObj v).weightArray
            local weightVal = 0.0
            for item in weights do if item != undefined then weightVal += item
            if weightVal == 0.0 then append returnArray v
        )
        skinOps.SelectVertices skinMod returnArray
        redrawViews()

        returnArray
    ),

    fn replace_bone inputObj oriBone newBone removeOldBone:true = (
        if (find_skin inputObj) == 0 then return false
        skinOps.addbone skinMod newBone 1
        get_all_bones inputObj
        if allBonesArray.count < 2 then return false

        get_skin_weights inputObj
        local prevSkinWeightsArray = deepCopy skinWeightsArray
        local oriBoneIndex = get_bone_index inputObj oriBone
        if oriBoneIndex == 0 then return false
        local newBoneIndex = get_bone_index inputObj newBone
        local vertNum = skinOps.GetNumberVertices skinMod

        --prog.start_progress "Replace Bones..."
        for v = 1 to vertNum do (
            local finedBoneID = findItem prevSkinWeightsArray[v].boneIDArray oriBoneIndex
            if finedBoneID != 0 then (
                prevSkinWeightsArray[v].boneIDArray[finedBoneID] = newBoneIndex
                skinOps.ReplaceVertexWeights skinMod v prevSkinWeightsArray[v].boneIDArray skinWeightsArray[v].weightArray
            )
            --prog.update_progress v vertNum
        )
        if removeOldBone == true then skinOps.removebone skinMod oriBoneIndex
        --prog.end_progress()

        return true
    ),

    fn copy_weight_between_bones_in_skin inputObj oriBone newBone removeOldBone:false = (
        if (find_skin inputObj) == 0 then return false

        get_skin_weights inputObj
        local prevSkinWeightsArray = deepCopy skinWeightsArray
        local oriBoneIndex = get_bone_index inputObj oriBone
        if oriBoneIndex == 0 then return false
        local newBoneIndex = get_bone_index inputObj newBone
        local vertNum = skinOps.GetNumberVertices skinMod

        --prog.start_progress "Copy weights..."
        for v = 1 to vertNum do (
            local finedBoneID = findItem prevSkinWeightsArray[v].boneIDArray oriBoneIndex
            if finedBoneID != 0 then (
                prevSkinWeightsArray[v].boneIDArray[finedBoneID] = newBoneIndex
                skinOps.ReplaceVertexWeights skinMod v prevSkinWeightsArray[v].boneIDArray skinWeightsArray[v].weightArray
            )
            --prog.update_progress v vertNum
        )
        if removeOldBone == true then skinOps.removebone skinMod oriBoneIndex
        --prog.end_progress()

        return true
    ),

    fn replace_multi_bones inputObj oriBoneArray newBoneArray = (
        if oriBoneArray.count == newBoneArray.count then (
            if (find_skin inputObj) == 0 then return false

            for item in newBoneArray do (
                skinOps.addbone skinMod item 1
            )

            get_skin_weights inputObj
            local delBones = #{1..allBonesArray.count}
            local prevSkinWeightsArray = deepCopy skinWeightsArray

            --prog.start_progress "Replace multi bones..." totalStep:2
            local vertNum = skinOps.GetNumberVertices skinMod
            for i= 1 to oriBoneArray.count do (
                local oriBoneIndex = get_bone_index inputObj oriBoneArray[i]
                local newBoneIndex = get_bone_index inputObj newBoneArray[i]
                if oriBoneIndex != 0 then (
                    delBones[oriBoneIndex] = false
                    for v = 1 to vertNum do (
                        local finedBoneID = findItem prevSkinWeightsArray[v].boneIDArray oriBoneIndex
                        if finedBoneID != 0 then (
                            prevSkinWeightsArray[v].boneIDArray[finedBoneID] = newBoneIndex
                            skinOps.ReplaceVertexWeights skinMod v prevSkinWeightsArray[v].boneIDArray skinWeightsArray[v].weightArray
                        )
                    )
                )
                --prog.update_progress i oriBoneArray.count
            )

            for i = allBonesArray.count to 1 by -1 where (delBones[i] == false) do (
                skinOps.SelectBone skinMod i
                skinOps.RemoveBone skinMod
                --prog.update_progress (allBonesArray.count - i + 1) allBonesArray.count inCurrentStep:2
            )
            --prog.end_progress()
            return true
        )

        return false
    ),

    fn replace_bones_by_baseName inObj inNewBaseName = (
        if (find_skin inObj) == 0 then return false
        get_all_bones inObj

        if allBonesArray.count != 0 then (
            local newBoneNamesArray = #()
            for item in allBoneNamesArray do (
                local newBoneName = name.replace_base item.name inNewBaseName
                append newBoneNamesArray newBoneName
            )

            local newBonesArray = #()
            for item in newBoneNamesArray do (
                local tempNewBone = getNodeByName item
                if tempNewBone != undefined then append newBonesArray tempNewBone
                else (
                    format "Cant Find %\n" item
                    return false
                )
            )

            replace_multi_bones inObj allBonesArray newBonesArray

            return true
        )

        return false
    ),

    fn copy_skin sourceObj targetObj = (
        get_skin_weights sourceObj
        max modify mode
        select targetObj
        addModifier targetObj (copy skinMod)

        local targetSkinMod
        for i = 1 to targetObj.modifiers.count do (
            if (classof targetObj.modifiers[i]) == Skin then targetSkinMod = targetObj.modifiers[i]
        )
        local targetObjNumVert = skinOps.GetNumberVertices targetSkinMod
        for v = 1 to targetObjNumVert do (
            skinOps.ReplaceVertexWeights targetSkinMod v skinWeightsArray[v].boneIDArray skinWeightsArray[v].weightArray
        )
    ),

    fn select_bone inObj inBoneObj = (
        local returnVal = false

        local boneIndex = get_bone_index inObj inBoneObj
        if boneIndex > 0 then (
            skinOps.SelectBone skinMod boneIndex
            returnVal = true
        )

        returnVal
    ),

    fn optimize_skin SkinMod boneLimit:8 skinTolerance:0.01 = (
        local ListOfBones = #()

        --Skin Modifier Setup
        SkinMod.enableDQ = false
        SkinMod.bone_Limit = boneLimit
        SkinMod.clearZeroLimit = skinTolerance
        skinOps.RemoveZeroWeights SkinMod
        SkinMod.clearZeroLimit = 0

        if skinOps.getNumberBones SkinMod > 1 do
        (
            ListOfBones = #{1..skinOps.GetNumberBones SkinMod}
            for v = 1 to skinOps.GetNumberVertices SkinMod do
            (
                for b = 1 to (skinOps.GetVertexWeightCount SkinMod v) do
                (
                    ListOfBones[skinOps.GetVertexWeightBoneID SkinMod v b] = false
                )
            )

            ListOfBones = ListOfBones as array
            for i = 1 to ListOfBones.count do
            (
                skinOps.SelectBone SkinMod ListOfBones[ListOfBones.count-i+1] -- Max 2014 sp5 hack
                skinOps.removebone SkinMod ListOfBones[ListOfBones.count-i+1]
            )
            if skinOps.getNumberBones SkinMod > 1 do skinOps.SelectBone SkinMod 1
            Format "Obj:% Removed:% Left:%\n" $.name ListOfBones.count (skinOps.GetNumberBones SkinMod)
        )
    ),

    fn optimize_skin_process objs:(selection as array) optimAllSkinMod:False bLimit:8 sTolerance:0.01 = (
        max modify mode
        if objs.count != 0 then
        (
            for obj in objs where (has_skin obj:obj) == True do
            (
                local modID = for m=1 to obj.modifiers.count where classOf obj.modifiers[m] == Skin collect m

                if optimAllSkinMod == False then modID = #(modID[1])
                for each in modID do
                (
                    modPanel.setCurrentObject obj.modifiers[each]
                    optimize_skin obj.modifiers[each] boneLimit:bLimit skinTolerance:sTolerance
                )
            )
            select objs
        )
    ),

    fn sel_vert_from_bones skin_mod threshold:0.01 = (
        local FinalVerts2Sel = #()
        if skin_mod != undefined then (
            leBone = skinops.getSelectedBone skin_mod
            svc = skinOps.GetNumberVertices skin_mod

            for o = 1 to svc do (
                local lv
                lv = skinOps.GetVertexWeightCount skin_mod o
                for k = 1 to lv where (skinOps.GetVertexWeightBoneID skin_mod o k) == leBone do (
                    if skinOps.GetVertexWeight skin_mod o k >= threshold then (
                        appendIfUnique FinalVerts2Sel o
                    )
                )
            )
            skinOps.SelectVertices skin_mod FinalVerts2Sel
        )

        FinalVerts2Sel
    ),

    fn make_rigid_skin skin_mod vert_list = (
        WeightArray = #()
        VertCount = 0
        BoneArray = #()
        FinalWeight = #()

        for v in vert_list do (
            for CurBone = 1 to (skinOps.GetVertexWeightCount skin_mod v) do (
                CurID = (skinOps.GetVertexWeightBoneID skin_mod v CurBone)
                if WeightArray[CurID] == undefined do WeightArray[CurID] = 0

                CurWeight = (skinOps.GetVertexWeight skin_mod v CurBone)
                WeightArray[CurID] += CurWeight
                VertCount += CurWeight
            )

            for i = 1 to WeightArray.count where WeightArray[i] != undefined and WeightArray[i] > 0 do (
                NewVal = (WeightArray[i] / VertCount)
                if NewVal > 0.01 do (append BoneArray i; append FinalWeight NewVal)
            )
        )
        return #(BoneArray, FinalWeight)
    ),

    fn load_skin obj file_path loadBindPose:false keepSkin: = (
        if keepSkin != true then keepSkin = false

        select obj
        Data = #()
        missingBones = #()

        MyFile = openFile file_path mode:"rt"
        if MyFile == undefined do return ()

        while (not eof MyFile) do
            append Data (execute (readLine MyFile));
        Close MyFile

        if (Data.count-1)!=obj.verts.count or obj.verts.count==0 then
            print "Bad number of verts";
        else
        (
            for m=obj.modifiers.count to 1 by -1 where classof obj.modifiers[m] == Skin do deleteModifier obj m

            setCommandPanelTaskMode #modify
            NewSkin = Skin()
            addmodifier obj NewSkin before:(if keepSkin then 1 else 0)

            if keepSkin do
                NewSkin.name = "Skin_" + getfilenamefile file_path;

            modPanel.setCurrentObject NewSkin
            Data[1] = execute Data[1]
            Hierarchy = #()

            for i=1 to Data[1].count do
            (
                MyBone = for obj in objects where obj.name == Data[1][i] collect obj

                if MyBone.count == 0 do
                (
                    print ("Missing bone: " + Data[1][i])
                    tmp = dummy name:Data[1][i]
                    append MyBone tmp
                    append missingBones tmp
                )

                if MyBone.count>1 and Hierarchy.count!=0 do
                (
                    print ("Multiple bones are named: " + MyBone[1].name + " (" + Mybone.count as string + ")")
                    GoodBone = undefined
                    for o in MyBone where (finditem Hierarchy o) != 0 do GoodBone = o
                    if GoodBone != undefined do MyBone = #(GoodBone)
                )

                if MyBone.count > 1 do
                (
                    fn ObjFilter PickBone = (findItem (getCurrentSelection()) PickBone) != 0

                    unhide MyBone
                    unfreeze MyBone
                    select MyBone

                    PickBone = pickobject filter:ObjFilter message:("Multiple bones found, pick a " + MyBone[1].name)
                    if PickBone != undefined do MyBone[1] = PickBone
                    select obj
                )

                MyBone = MyBone[1]
                if (finditem Hierarchy MyBone) == 0 do
                (
                    append Hierarchy MyBone
                    for obj in Hierarchy do
                    (
                        for CurChild in obj.children do appendifunique Hierarchy CurChild
                        if obj.parent != undefined do appendifunique Hierarchy obj.parent
                    )
                )

                setCommandPanelTaskMode #modify
                skinOps.addbone NewSkin MyBone 1

                if loadBindPose then
                (-- load bind pose
                    MyFileBP = substring FileName 1 (FileName.count - 4) + "bp"; BindPoses = #()
                    if doesFileExist MyFileBP do
                    (
                        MyFile = openFile MyFileBP
                        while (not eof MyFile) do
                            append BindPoses (execute (readLine MyFile));
                        Close MyFile
                    )

                    if BindPoses[i] != undefined do skinUtils.SetBoneBindTM $ MyBone BindPoses[i]
                )
            )

            for i = 1 to obj.verts.count do
            (
                BoneID = #(); BoneWeight = #(); GoodBones = #{};
                AllBoneWeight = for b = 1 to Data[1].count collect 0

                for b=1 to Data[i+1][1].count do
                (
                    AllBoneWeight[Data[i+1][1][b]] += Data[i+1][2][b]
                    GoodBones[Data[i+1][1][b]] = true
                )
                for b in GoodBones do
                (
                    append BoneID b
                    append BoneWeight AllBoneWeight[b]
                )
                if BoneID.count != 0 do skinOps.SetVertexWeights NewSkin i BoneID[1] 1 -- Max 2014 sp5 hack
                skinOps.ReplaceVertexWeights NewSkin i BoneID BoneWeight
            )
            return missingBones
        )
    ),

    fn save_skin obj skin_mod file_path = (
        select obj
        max modify mode
        modPanel.setCurrentObject obj.modifiers[#Skin]

        if (classof obj.modifiers[#Skin] == Skin) and (skinOps.GetNumberBones obj.modifiers[#Skin]) > 0 then (
            local bone_list = "#("
            for i=1 to (skinOps.GetNumberBones skin_mod) do append bone_list ("\\\"" + (skinOps.GetBoneName skin_mod i 1) + "\\\", ")

            bone_list = substring bone_list 1 (bone_list.count-1); bone_list[bone_list.count] = ")"
            local skin_data = #(bone_list)
            skin_data.count = skinOps.GetNumberVertices skin_mod + 1

            for v=1 to skinOps.GetNumberVertices skin_mod do
            (
                local bone_array = #()
                local weight_array = #()
                for b = 1 to (skinOps.GetVertexWeightCount skin_mod v) do
                (
                    append bone_array (skinOps.GetVertexWeightBoneID skin_mod v b)
                    append weight_array (skinOps.GetVertexWeight skin_mod v b)
                )
                skin_data[v+1] = #(bone_array, weight_array)
            )

            file_path = CreateFile file_path
            print skin_data to:file_path
            Close file_path

            return file_path
        )
    )
)
