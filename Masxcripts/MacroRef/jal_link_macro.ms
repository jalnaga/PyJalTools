macroscript jal_link_to_last category:"jalTools" tooltip:"Link to last" autoUndoEnabled:true (
    jal.link.link_to_last_sel()
)

macroscript jal_link_to_first category:"jalTools" tooltip:"Link to first" autoUndoEnabled:true (
    jal.link.link_to_first_sel()
)

macroscript jal_unLink category:"jalTools" tooltip:"Unlink" autoUndoEnabled:true (
    jal.link.unlink_selection()
)

macroscript jal_unLink_children category:"jalTools" tooltip:"Unlink children" autoUndoEnabled:true (
    jal.link.unlink_children()
)