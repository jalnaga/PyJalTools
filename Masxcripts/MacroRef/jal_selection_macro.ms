macroscript jal_selFilter_all category:"jalTools" tooltip:"Selection filter All" autoUndoEnabled:true (
    jal.sel.set_selectionSet_to_all()
    if selection.count > 0 then getCurrentSelection()
)

macroscript jal_selFilter_bone category:"jalTools" tooltip:"Selection filter Bone" autoUndoEnabled:true (
    jal.sel.set_selectionSet_to_bone()
    if selection.count > 0 then jal.sel.filter_bone()
)

macroscript jal_selFilter_bip category:"jalTools" tooltip:"Selection filter Bip" autoUndoEnabled:true (
    jal.sel.set_selectionSet_to_bone()
    if selection.count > 0 then jal.sel.filter_bip()
)

macroscript jal_selFilter_point category:"jalTools" tooltip:"Selection filter Point" autoUndoEnabled:true (
    jal.sel.set_selectionSet_to_point()
    if selection.count > 0 then jal.sel.filter_helper()
)

macroscript jal_selFilter_expTm category:"jalTools" tooltip:"Selection filter ExpTm" autoUndoEnabled:true (
    jal.sel.set_selectionSet_to_helper()
    if selection.count > 0 then jal.sel.filter_expTm()
)

macroscript jal_selFilter_spline category:"jalTools" tooltip:"Selection filter Spline" autoUndoEnabled:true (
    jal.sel.set_selectionSet_to_spline()
    if selection.count > 0 then jal.sel.filter_spline()
)