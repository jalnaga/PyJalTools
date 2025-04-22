from pymxs import runtime as rt

def jal_align_mirror_x():
    if rt.selection.count == 0:
        return False
    
    pObj = None
    defMirrorAxis = 0
    oriObjArray = rt.getCurrentSelection()
    boneArray = []
    helperArray = []
    nonBoneArray = []
    
    mirroredBoneArray = []
    mirroredHelperArray = []
    mirroredNonBoneArray = []
    
    mirroredObjArray = []
    
    defMirrorAxis = 1
    
    for item in oriObjArray:
        if rt.classOf(item) == rt.BoneGeometry:
            boneArray.append(item)
        elif rt.superClassOf(item) == rt.Helper:
            helperArray.append(item)
        else:
            nonBoneArray.append(item)
    
    if boneArray.count != 0:
        mirroredBoneArray = jal.mirror.mirror_bone(boneArray, mAxis=defMirrorAxis)
    if helperArray.count != 0:
        mirroredHelperArray = jal.mirror.mirror_geo(helperArray, mAxis=defMirrorAxis, pivotObj=pObj, cloneStatus=2)
    if nonBoneArray.count != 0:
        mirroredNonBoneArray = jal.mirror.mirror_geo(nonBoneArray, mAxis=defMirrorAxis, pivotObj=pObj, cloneStatus=2)
    
    mirroredObjArray.extend(mirroredBoneArray)
    mirroredObjArray.extend(mirroredHelperArray)
    mirroredObjArray.extend(mirroredNonBoneArray)
    
    rt.clearSelection()
    rt.select(mirroredObjArray)
    
rt.jal_align_mirror_x = jal_align_mirror_x

macroscript_name = 'jal_align_mirror_x'
macroscript_category = 'jalTools'
macroscript_tooltip = 'Mirror X'
macroscript_text = 'jal_align_mirror_x'
macroscript_content = 'jal_align_mirror_x()'

rt.macros.new(
    macroscript_category,
    macroscript_name,
    macroscript_tooltip,
    macroscript_text,
    macroscript_content
)