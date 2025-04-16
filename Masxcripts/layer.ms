struct _Layer (
    fn reset_layer = (
        local defaultLayer = layerManager.getLayer 0
        local layerNameArray = #()
        defaultLayer.current  = true

        if LayerManager.count > 1 then (
            for i = 1 to layerManager.count-1 do (
                ilayer = layerManager.getLayer i
                layerName = ilayer.name
                append layerNameArray layerName

                layer = ILayerManager.getLayerObject i
                layerNodes = refs.dependents layer

                for item in layerNodes do (
                    if (isValidNode item) then defaultLayer.addNode item
                )
            )
            for item in layerNameArray do LayerManager.deleteLayerByName item
        )
    ),

    fn get_nodes_from_layer inLayerNum = (
        if inLayerNum != false then (
            layer = layermanager.getLayer inLayerNum
            layer.nodes &theNodes
            return theNodes
        )
        else (
            local emptyArray = #()
            return emptyArray
        )
    ),

    fn get_layer_number inLayerName = (
        for i = 0 to (LayerManager.count - 1) do (
            ilayer = layerManager.getLayer i
            if ilayer.name == inLayerName then return i
        )

        return false
    ),

    fn get_nodes_by_layername inLayerName = (
        get_nodes_from_layer (get_layer_number inLayerName)
    ),

    fn del_empty_layer showLog:false = (
        DeletedLayerCount = 0
        local deflayer = layermanager.getlayer 0
        deflayer.current = true
        for i = Layermanager.count-1 to 1 by-1 do (
            layer = layermanager.getLayer i
            local thislayername = layer.name
            layer.nodes &theNodes
            if thenodes.count== 0 then (
                LayerManager.deleteLayerbyname thislayername
                DeletedLayerCount +=1
            )
        )

        if showLog then (
            if not DeletedLayerCount == 0 then Messagebox ("Number of layers removed - " + DeletedLayerCount as string) title:"Layer Manager"
        )
    ),

    fn create_layer_from_array inArray inLayerName = (
        local newLayer = undefined
        local layerIndex = get_layer_number inLayerName
        if layerIndex == false then (
            newLayer = LayerManager.newLayer()
            newLayer.setName inLayerName
        )
        else newLayer = layerManager.getLayer layerIndex
        for item in inArray do newLayer.addNode item

        return newLayer
    ),

    fn delete_layer inLayerName forceDelete:false = (
        local returnVal = false
        local deflayer = layermanager.getlayer 0
        deflayer.current = true
        local nodeArray = get_nodes_by_layername inLayerName
        if nodeArray.count > 0 then (
            if forceDelete then (
                delete nodeArray
                nodeArray = #()
            )
            else for item in nodeArray do deflayer.addNode item
        )
        returnVal = LayerManager.deleteLayerbyname inLayerName

        returnVal
    ),

    fn set_parent_layer inLayerName inParentName = (
        local returnVal = false
        local targetLayer = layermanager.getlayer (get_layer_number inLayerName)
        local parentLayer = layermanager.getlayer (get_layer_number inParentName)
        if targetLayer != undefined and parentLayer != undefined then (
            targetLayer.setParent parentLayer
            returnVal = true
        )

        returnVal
    ),

    fn rename_layer_from_index layer_index search_for replace_with = (
        cur_layer = LayerManager.getLayer layer_index
        layer_name =  cur_layer.name
        find_at = findString layer_name search_for

        if find_at != undefined then
        (
            found_string = substring layer_name find_at search_for.count
            new_name = (substituteString layer_name found_string replace_with)
            cur_layer.setName new_name
        )
    ),

    fn is_valid_layer layer_name: layer_index: = (
        local layer =
        (
            if layer_name!=unsupplied then ( LayerManager.getLayerFromName layer_name )
            else if layer_index!=unsupplied then ( LayerManager.getLayer layer_index )
            else(undefined)
        )
        if layer != undefined then ( return true )
        else ( return false )
    )
)
