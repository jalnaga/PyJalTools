struct _Select (
    name, bone,

    fn set_selectionSet_to_all = (
        SetSelectFilter 1
    ),

    fn set_selectionSet_to_bone = (
        SetSelectFilter 8
    ),

    fn reset_selectionSet = (
        SetSelectFilter 1
    ),

    fn set_selectionSet_to_helper = (
        SetSelectFilter 6
    ),

    fn set_selectionSet_to_point = (
        SetSelectFilter 10
    ),

    fn set_selectionSet_to_spline = (
        SetSelectFilter 3
    ),

    fn set_selectionSet_to_mesh = (
        SetSelectFilter 2
    ),

    fn filter_bip = (
        local selArray = getCurrentSelection()
        if selArray.count > 0 then (
            local filteredSel = for item in selArray where ((classOf item) == Biped_Object) collect item
            clearSelection()
            select filteredSel
        )
    ),

    fn filter_bone = (
        local selArray = getCurrentSelection()
        if selArray.count > 0 then (
            local filteredSel = for item in selArray where ((classOf item) == BoneGeometry) collect item
            clearSelection()
            select filteredSel
        )
    ),

    fn filter_helper = (
        local selArray = getCurrentSelection()
        if selArray.count > 0 then (
            local filteredSel = for item in selArray where (((classOf item) == Point) or ((classOf item) == IK_Chain_Object)) collect item
            clearSelection()
            select filteredSel
        )
    ),

    fn filter_expTm = (
        local selArray = getCurrentSelection()
        if selArray.count > 0 then (
            local filteredSel = for item in selArray where ((classOf item) == ExposeTm) collect item
            clearSelection()
            select filteredSel
        )
    ),

    fn filter_spline = (
        local selArray = getCurrentSelection()
        if selArray.count > 0 then (
            local filteredSel = for item in selArray where ((superClassOf item) == shape) collect item
            clearSelection()
            select filteredSel
        )
    ),

    fn select_children inObj includeSelf:false = (
        local children = #()
        if includeSelf then (
            children = (execute ("$'" + inObj.name + "'/*/.../*")) as array
            insertItem inObj children 1
        ) 
        else children = (execute ("$'" + inObj.name + "'/*/.../*")) as array

        children
    ),

    fn distinguish_hierachy_objects inArray = (
        local returnArray = #()
        local seperatedNodesArray = #()
        local hierachyNodesArray = #()

        for item in inArray do (
            if item.parent == undefined and item.children.count == 0 then append seperatedNodesArray item
            else append hierachyNodesArray item
        )

        returnArray[1] = seperatedNodesArray
        returnArray[2] = hierachyNodesArray

        return returnArray
    ),

    fn get_nonLinked_objects inArray = (
        return (distinguish_hierachy_objects inArray)[1]
    ),

    fn get_linked_objects inArray = (
        return (distinguish_hierachy_objects inArray)[2]
    ),

    fn sort_by_hierachy inArray = (
        return bone.sort_bones_as_hierarchy inArray
    ),

    fn sort_by_index inArray = (
        if inArray.count > 0 then (
            struct indexSorting (oriIndex, newIndex)

            local sortedArray = #()
            local structArray = #()

            for i = 1 to inArray.count do (
                local tempIndex = name.get_index_as_digit inArray[i].name
                if tempIndex == false then (
                    structArray[i] = indexSorting i 0
                )
                else structArray[i] = indexSorting i tempIndex
            )

            qsort structArray (fn myLevel v1 v2 = (v1.newIndex - v2.newIndex))

            for i = 1 to inArray.count do append sortedArray inArray[structArray[i].oriIndex]

            return sortedArray
        )
        return #()
    ),

    fn sort_objects inArray = (
        local returnArray = #()
        local aloneObjArray = get_nonLinked_objects inArray
        local hierachyObjArray = get_linked_objects inArray

        local sortedAloneObjArray = #()
        local sortedHierachObjArray = #()
        local isAloneImporter = false

        local firstIndexOfAloneObj = 10000
        local firstIndexOfHierachyObj = 10000

        sortedAloneObjArray = sort_by_index aloneObjArray
        sortedHierachObjArray = sort_by_hierachy hierachyObjArray
        
        if sortedAloneObjArray.count > 0 then (
            local indexDigit = name.get_index_as_digit sortedAloneObjArray[1].name
            if indexDigit == false then firstIndexOfAloneObj = 0
            else firstIndexOfAloneObj = indexDigit
        )
        if sortedHierachObjArray.count > 0 then (
            local indexDigit = name.get_index_as_digit sortedHierachObjArray[1].name
            if indexDigit == false then firstIndexOfHierachyObj = 0
            else firstIndexOfHierachyObj = indexDigit
        )
        
        if firstIndexOfAloneObj < firstIndexOfHierachyObj then isAloneImporter = true
        if isAloneImporter then (
            for item in sortedAloneObjArray do append returnArray item
            for item in sortedHierachObjArray do append returnArray item
        )
        else (
            for item in sortedHierachObjArray do append returnArray item
            for item in sortedAloneObjArray do append returnArray item
        )

        return returnArray
    )
)
