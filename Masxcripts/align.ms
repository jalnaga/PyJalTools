struct _Align (
    fn align_to_last_sel_center = (
        if selection.count > 1 then (
            for i = 1 to (selection.count - 1) do (
                selection[i].transform = selection[selection.count].transform
                selection[i].pos = selection[selection.count].center
            )
        )
    ),

    fn align_to_last_sel = (
        if selection.count > 1 then (
            for i = 1 to (selection.count - 1) do (
                selection[i].transform = selection[selection.count].transform
            )
        )
    ),

    fn align_to_last_sel_pos = (
        if selection.count > 1 then (
            for i = 1 to (selection.count - 1) do (
                local posDumPoint = Point()
                local posConst = Position_Constraint()
                local rotConst = Orientation_Constraint()
                posDumPoint.position.controller = posConst
                posDumPoint.rotation.controller = rotConst
                posConst.appendTarget selection[selection.count] 100.0
                rotConst.appendTarget selection[i] 100.0

                selection[i].transform = posDumPoint.transform
                delete posDumPoint
            )
        )
    ),

    fn align_to_last_sel_rot = (
        if selection.count > 1 then (
            for i = 1 to (selection.count - 1) do (
                local rotDumPoint = Point()
                local posConst = Position_Constraint()
                local rotConst = Orientation_Constraint()
                rotDumPoint.position.controller = posConst
                rotDumPoint.rotation.controller = rotConst
                posConst.appendTarget selection[i] 100.0
                rotConst.appendTarget selection[selection.count] 100.0

                selection[i].transform = rotDumPoint.transform
                delete rotDumPoint
            )
        )
    )
)
