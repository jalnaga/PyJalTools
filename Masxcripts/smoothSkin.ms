fn smooth_skin SmoothSkinData:#(#(), #(), #(), #(), #(), #(), #()) vertGroupMode:1 smoothRadius:5.0 keepMax:false SmoothSkinMaxUndo:10 UndoWeights:#() = (
	obj = $
	skinMod = modPanel.getCurrentObject()
	FinalBoneArray = #()
	FinalWeightArray = #()
	o = 1
		
	UseOldData = (obj == SmoothSkinData[1][1]) and (obj.verts.count == SmoothSkinData[1][2])
	if not UseOldData do SmoothSkinData = #(#(), #(), #(), #(), #(), #(), #())
	SmoothSkinData[1][1] = obj; SmoothSkinData[1][2] = obj.verts.count

	tmpObj = copy Obj
	tmpObj.modifiers[skinMod.name].enabled = false

	fn DoNormalizeWeight Weight = (
		WeightLength = 0
		NormalizeWeight = #()
		for w = 1 to Weight.count do WeightLength += Weight[w]
		if WeightLength != 0 then for w = 1 to Weight.count do NormalizeWeight[w] = Weight[w] * (1 / WeightLength)
			else NormalizeWeight[1] = 1.0
		return NormalizeWeight
	)
		
	skinMod.clearZeroLimit = 0.00
	skinOps.RemoveZeroWeights skinMod
		
	posarray = for a in tmpObj.verts collect a.pos
		
	if (SmoothSkinData[8] != smoothRadius) do (SmoothSkinData[6] = #(); SmoothSkinData[7] = #())
		
	for v = 1 to obj.verts.count where (skinOps.IsVertexSelected skinMod v == 1) and (not keepMax or (skinOps.GetVertexWeightCount skinmod v != 1)) do 
	(
		-- 			print v
		VertBros = #{}; VertBrosRatio = #()
		Weightarray = #(); BoneArray = #(); FinalWeight = #()
		WeightArray.count = skinOps.GetNumberBones skinMod
			
		if vertGroupMode == 1 and (SmoothSkinData[2][v] == undefined) do (
			if (classof tmpObj == Editable_Poly) or (classof tmpObj == PolyMeshObject) then (
				CurEdges = polyop.GetEdgesUsingVert tmpObj v
				for CE in CurEdges do VertBros += (polyop.getEdgeVerts tmpObj CE) as bitArray
			)else (
				CurEdges = meshop.GetEdgesUsingvert tmpObj v
				for i in CurEdges do CurEdges[i] = (getEdgeVis tmpObj (1+(i-1)/3)(1+mod (i-1) 3))
				for CE in CurEdges do VertBros += (meshop.getVertsUsingEdge tmpObj CE) as bitArray
			)
				
			VertBros = VertBros as array
			SmoothSkinData[2][v] = #()
			SmoothSkinData[3][v] = #()
				
			if VertBros.count > 0 do (
				for vb in VertBros do (
					CurDist = distance posarray[v] posarray[vb]
					if CurDist == 0 then append VertBrosRatio 0 else append VertBrosRatio (1 / CurDist)
				)
				
				VertBrosRatio = DoNormalizeWeight VertBrosRatio
				VertBrosRatio[finditem VertBros v] = 1
				SmoothSkinData[2][v] = VertBros
				SmoothSkinData[3][v] = VertBrosRatio
			)
		)
		
		if vertGroupMode == 2 do (
			SmoothSkinData[4][v] = for vb = 1 to posarray.count where (skinOps.IsVertexSelected skinMod vb == 0) and (distance posarray[v] posarray[vb]) < smoothRadius collect vb
			SmoothSkinData[5][v] = for vb in SmoothSkinData[4][v] collect
				(CurDist = distance posarray[v] posarray[vb]; if CurDist == 0 then 0 else (1 / CurDist))
			SmoothSkinData[5][v] = DoNormalizeWeight SmoothSkinData[5][v]
			for i = 1 to SmoothSkinData[5][v].count do SmoothSkinData[5][v][i] *= 2
		)
			
		if vertGroupMode == 3 and (SmoothSkinData[6][v] == undefined) do (
			SmoothSkinData[6][v] = for vb = 1 to posarray.count where (distance posarray[v] posarray[vb]) < smoothRadius collect vb
			SmoothSkinData[7][v] = for vb in SmoothSkinData[6][v] collect
				(CurDist = distance posarray[v] posarray[vb]; if CurDist == 0 then 0 else (1 / CurDist))
			SmoothSkinData[7][v] = DoNormalizeWeight SmoothSkinData[7][v]
			for i = 1 to SmoothSkinData[7][v].count do SmoothSkinData[7][v][i] *= 2
		)
			

		if vertGroupMode != 4 do (		
			VertBros = SmoothSkinData[vertGroupMode * 2][v]
			VertBrosRatio = SmoothSkinData[(vertGroupMode * 2) + 1][v]
				
			for z = 1 to VertBros.count do for CurBone = 1 to (skinOps.GetVertexWeightCount skinMod VertBros[z]) do (
				CurID = (skinOps.GetVertexWeightBoneID skinMod VertBros[z] CurBone)
				if WeightArray[CurID] == undefined do WeightArray[CurID] = 0
				WeightArray[CurID] += (skinOps.GetVertexWeight skinMod VertBros[z] CurBone) * VertBrosRatio[z]
			)
			
			for i = 1 to WeightArray.count where WeightArray[i] != undefined and WeightArray[i] > 0 do (
				NewVal = (WeightArray[i] / 2)
				if NewVal > 0.01 do (append BoneArray i; append FinalWeight NewVal)
			)
			FinalBoneArray[v] = BoneArray
			FinalWeightArray[v] = FinalWeight
		)
	)
		
	if vertGroupMode == 4 then (
		convertTopoly tmpObj
		polyObj = tmpObj
			
		-- Only test selected
		VertSelection = for v = 1 to obj.verts.count where (skinOps.IsVertexSelected skinMod v == 1) collect v
		DoneEdge = (polyobj.edges as bitarray) - polyop.getEdgesUsingVert polyObj VertSelection
		DoneFace = (polyobj.faces as bitarray) - polyop.getFacesUsingVert polyObj VertSelection

		-- Elements
		SmallElements = #()
		for f = 1 to polyobj.faces.count where not DoneFace[f] do (
			CurElement = polyop.getElementsUsingFace polyObj #{f}
				
			CurVerts = polyop.getVertsUsingFace polyobj CurElement; MaxDist = 0
			for v1 in CurVerts do for v2 in CurVerts where MaxDist < (smoothRadius * 2) do (
				dist = distance polyobj.verts[v1].pos polyobj.verts[v2].pos
				if dist > MaxDist do MaxDist = dist
			)
			if MaxDist < (smoothRadius * 2) do append SmallElements CurVerts
			DoneFace += CurElement
		)

		-- Loops
		EdgeLoops = #()
		for ed in SmallElements do DoneEdge += polyop.getEdgesUsingVert polyobj ed
		for ed = 1 to polyobj.edges.count where not DoneEdge[ed] do (
			polyobj.selectedEdges = #{ed}
			polyobj.ButtonOp #SelectEdgeLoop
			CurEdgeLoop = (polyobj.selectedEdges as bitarray)
			if CurEdgeLoop.numberSet > 2 do (
				CurVerts = (polyop.getvertsusingedge polyobj CurEdgeLoop); MaxDist = 0
				for v1 in CurVerts do for v2 in CurVerts where MaxDist < (smoothRadius * 2) do (
					dist = distance polyobj.verts[v1].pos polyobj.verts[v2].pos
					if dist > MaxDist do MaxDist = dist
				)
				if MaxDist < (smoothRadius * 2) do append EdgeLoops CurVerts
			)
			DoneEdge += CurEdgeLoop
		)
			
		modPanel.setCurrentObject SkinMod; subobjectLevel = 1
		for z in #(SmallElements, EdgeLoops) do for i in z do (
			VertList = for v3 in i where (skinOps.IsVertexSelected skinMod v3 == 1) collect v3
			NewWeights = odcSkin.make_rigid_skin SkinMod VertList
			for v3 in VertList do (FinalBoneArray[v3] = NewWeights[1]; FinalWeightArray[v3] = NewWeights[2])
		)
	)
		
	SmoothSkinData[8] = smoothRadius
		
	delete tmpObj
	OldWeightArray = #()
	OldBoneArray = #()
	LastWeights = #()
	for sv = 1 to FinalBoneArray.count where FinalBonearray[sv] != undefined and FinalBoneArray[sv].count != 0 do (
		-- Home-Made undo
		NumItem = skinOps.GetVertexWeightCount skinMod sv
		OldWeightArray.count = OldBoneArray.count = NumItem
		for CurBone = 1 to NumItem do (
			OldBoneArray[CurBone] = (skinOps.GetVertexWeightBoneID skinMod sv CurBone)
			OldWeightArray[CurBone] = (skinOps.GetVertexWeight skinMod sv CurBone)
		)
		
		append LastWeights #(skinMod, sv, deepcopy OldBoneArray, deepcopy OldWeightArray)
		if UndoWeights.count >= SmoothSkinMaxUndo do deleteItem UndoWeights 1
			--
		skinOps.ReplaceVertexWeights skinMod sv FinalBoneArray[sv] FinalWeightArray[sv]
	)
	append UndoWeights LastWeights
) 

fn smooth_skin_iter vertGroupMode:1 smoothRadius:5.0 keepMax:false maxIter:3 SmoothSkinMaxUndo:10 = (
	if selection.cout != 1 then return false

	local UndoWeights = #()
	local SmoothSkinData = #(#(), #(), #(), #(), #(), #(), #())
	
	p=0
	for iter = 1 to maxIter do 
	(
		p+=1
		smooth_skin SmoothSkinData:SmoothSkinData vertGroupMode:vertGroupMode smoothRadius:smoothRadius keepMax:keepMax SmoothSkinMaxUndo:SmoothSkinMaxUndo UndoWeights:UndoWeights
		
		prog = ((p as float / maxIter as float) * 100.0)
		print(prog)
	)
)
