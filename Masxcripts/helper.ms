struct _Helper (
    name,

    fn create_point inName size:2 boxToggle:off crossToggle:on pointColor:(color 14 255 2) pos:[0,0,0] = (
        local returnPoint

        returnPoint = point()
        returnPoint.size = size
        returnPoint.box = boxToggle
        returnPoint.cross = crossToggle
        returnPoint.wireColor = pointColor
        returnPoint.name = inName
        returnPoint.pos = pos

        returnPoint.centermarker = off
        returnPoint.axistripod = off

        return returnPoint
    ),

    fn create_empty_point inName = (
        local returnPoint = create_point inName size:0 crossToggle:off
        returnPoint.centermarker = off
        returnPoint.axistripod = off
        freeze returnPoint

        return returnPoint
    ),

    fn gen_helper_name_from_obj inObj makeTwo:false isExp:false = (
        local pointName = ""
        local targetName = ""
        local typeName = name.get_dummyStr()
        local tempName = ""

        if isExp then typeName = name.get_exposeTMStr()

        tempName = name.replace_type inObj.name typeName
        if (name.get_type inObj.name) == typeName then (
            tempName = name.increase_index tempName 1
        )
        pointName = tempName

        if makeTwo then (
            targetName = name.add_sufix_to_realName tempName "Tgt"
        )

        return #(pointName, targetName)
    ),

    fn gen_helper_shape_from_obj inObj = (
        local helperSize = 2.0
        local crossToggle = false
        local boxToggle = true

        if (classOf inObj) == BoneGeometry then helperSize = amax #(inObj.width, inObj.height)
        if ((classOf inObj) == Point) or ((classOf inObj) == ExposeTm) then (
            helperSize = inObj.size + 0.5
            if inObj.cross then (
                crossToggle = false
                boxToggle = true
            )
            if inObj.box then (
                crossToggle = true
                boxToggle = false
            )
        )

        return #(helperSize, crossToggle, boxToggle)
    ),

    fn create_helper makeTwo:false = (
        local createdHelperArray = #()
        if selection.count > 0 then (
            local selArray = getCurrentSelection()
            local helperSize = 2.0
            local crossToggle = false
            local boxToggle = true
            local pointName = ""
            local targetName = ""

            for item in selArray do (
                -- Set size of create helpers
                local helperShapeArray = gen_helper_shape_from_obj item
                helperSize = helperShapeArray[1]
                crossToggle = helperShapeArray[2]
                boxToggle = helperShapeArray[3]

                -- Set name of create helpers
                local helperNameArray = gen_helper_name_from_obj item makeTwo:makeTwo
                pointName = helperNameArray[1]
                targetName = helperNameArray[2]

                -- For mouse right click
                if makeTwo then (
                    local targetPoint = create_point targetName size:helperSize boxToggle:off crossToggle:on pointColor:(color 14 255 2) pos:[0,0,0]
                    targetPoint.transform = item.transform
                    local genPoint = create_point pointName size:helperSize boxToggle:on crossToggle:off pointColor:(color 14 255 2) pos:[0,0,0]
                    genPoint.transform = item.transform

                    append createdHelperArray targetPoint
                    append createdHelperArray genPoint
                )
                else (
                    local genPoint = create_point pointName size:helperSize boxToggle:boxToggle crossToggle:crossToggle pointColor:(color 14 255 2) pos:[0,0,0]
                        genPoint.transform = item.transform
                    append createdHelperArray genPoint
                )
            )
        )
        else (
            local genPoint = Point wirecolor:(color 14 255 2)
            append createdHelperArray genPoint
        )
        select createdHelperArray
        return createdHelperArray
    ),

    fn create_parent_helper = (
        if selection.count > 0 then (
            local selArray = getCurrentSelection()
            local helperSize = 2.0
            local crossToggle = false
            local boxToggle = true
            local pointName = ""
            local targetName = ""

            for item in selArray do (
                local helperShapeArray = gen_helper_shape_from_obj item
                helperSize = helperShapeArray[1]
                crossToggle = helperShapeArray[2]
                boxToggle = helperShapeArray[3]

                -- Set name of create helpers
                local helperNameArray = gen_helper_name_from_obj item
                pointName = helperNameArray[1]
                targetName = helperNameArray[2]

                local genPoint = create_point pointName size:helperSize boxToggle:on crossToggle:off pointColor:(color 14 255 2) pos:[0,0,0]
                genPoint.transform = item.transform
                genPoint.parent = item.parent
                item.parent = genPoint
                genPoint.name = name.replace_type genPoint.name (name.get_parentStr())
            )
        )
    ),

    fn create_expTm = (
        local createdHelperArray = #()
        if selection.count > 0 then (
            local selArray = getCurrentSelection()
            local helperSize = 2.0
            local crossToggle = false
            local boxToggle = true
            local pointName = ""
            local targetName = ""

            for item in selArray do (
                -- Set size of create helpers
                local helperShapeArray = gen_helper_shape_from_obj item
                helperSize = helperShapeArray[1]
                crossToggle = helperShapeArray[2]
                boxToggle = helperShapeArray[3]

                -- Set name of create helpers
                local helperNameArray = gen_helper_name_from_obj item makeTwo:false isExp:true
                pointName = helperNameArray[1]
                targetName = helperNameArray[2]

                local genPoint = exposeTM name:pointName size:helperSize box:boxToggle cross:crossToggle wirecolor:(color 14 255 2) pos:[0,0,0]
                    genPoint.transform = item.transform
                append createdHelperArray genPoint
            )
        )
        else (
            local genPoint = exposeTM wirecolor:(color 14 255 2)
            append createdHelperArray genPoint
        )
        select createdHelperArray
        return createdHelperArray
    ),

    fn set_size inObj inNewSize = (
        if superClassOf inObj == helper then (
            inObj.size = inNewSize
            inObj
        )
    ),

    fn add_size inObj inAddSize = (
        if superClassOf inObj == helper then (
            inObj.size += inAddSize
            inObj
        )
    ),

    fn set_shape_to_center inObj = (
        if (classOf inObj == ExposeTm) or (classOf inObj == Point) then (
            inObj.centermarker = true
            inObj.box = true

            inObj.axistripod = false
            inObj.cross = false
        )
    ),

    fn set_shape_to_axis inObj = (
        if (classOf inObj == ExposeTm) or (classOf inObj == Point) then (
            inObj.axistripod = true

            inObj.centermarker = false
            inObj.box = false
            inObj.cross = false
        )
    ),

    fn set_shape_to_cross inObj = (
        if (classOf inObj == ExposeTm) or (classOf inObj == Point) then (
            inObj.cross = true

            inObj.box = false
            inObj.centermarker = false
            inObj.axistripod = false
        )
    ),

    fn set_shape_to_box inObj = (
        if (classOf inObj == ExposeTm) or (classOf inObj == Point) then (
            inObj.box = true

            inObj.centermarker = false
            inObj.axistripod = false
            inObj.cross = false
        )
    )
)
