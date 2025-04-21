-- Jal Align Macro
-- Python Implementation Version

macroscript jal_align_to_last category:"jalTools" tooltip:"Align to last" autoUndoEnabled:true (
    python.execute "jal.align.align_to_last_sel()"
)

macroscript jal_align_to_last_center category:"jalTools" tooltip:"Align to last center" autoUndoEnabled:true (
    python.execute "jal.align.align_to_last_sel_center()"
)

macroscript jal_align_pos_only category:"jalTools" tooltip:"Align Position only" autoUndoEnabled:true (
    python.execute "jal.align.align_to_last_sel_pos()"
)

macroscript jal_align_rot_only category:"jalTools" tooltip:"Align Rotation only" autoUndoEnabled:true (
    python.execute "jal.align.align_to_last_sel_rot()"
)

macroscript jal_align_mirror_x category:"jalTools" tooltip:"Mirror X" autoUndoEnabled:true (
    
)

macroscript jal_align_mirror_y category:"jalTools" tooltip:"Mirror Y" autoUndoEnabled:true (
    
)