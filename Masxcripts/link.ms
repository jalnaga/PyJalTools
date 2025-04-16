struct _Link (
    fn link_to_last_sel = (
        if selection.count > 1 then (
            for i = 1 to (selection.count - 1) do (
                selection[i].parent = selection[selection.count]
            )
        )
    ),

    fn link_to_first_sel = (
        if selection.count > 1 then (
            for i = 2 to selection.count do (
                selection[i].parent = selection[1]
            )
        )
    ),

    fn unlink_selection = (
        if selection.count > 0 then (
            for item in selection do (
                item.parent = undefined
            )
        )
    ),

    fn unlink_children = (
        if selection.count == 1 then (
            for item in selection[1].children do (
                item.parent = undefined
            )
        )
    )
)
