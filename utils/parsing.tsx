export function parseNetworkDataPaper(data: any) {

    let nodes = [];
    let links = [];

    data.forEach(token => {

        switch (token.title) {
            case 'AGORA':
                nodes.push({ "id": token.ssPaperId.toString(), 'color': 'darkblue' })
                break
            default:
                nodes.push({ "id": token.ssPaperId.toString(), 'color': 'black' })
        }

        /*
        token.cited.forEach(cited => {
            nodes.push({ "id": cited.toString(), 'color': '#8e4100' })
            const citationObj = { 'source': cited.toString(), "target": data[0].name.toString() }
            links.push(citationObj)
        })
        token.cites.forEach(cites => {
            if (cites == 'AGORA') {
                nodes.push({ "id": cites.toString(), 'color': 'darkblue' })
            }
            else {
                nodes.push({ "id": cites.toString(), 'color': '#A2A2A1FF' })
            }
            const citationObj = { 'source': data[0].name.toString(), "target": cites.toString() }
            links.push(citationObj)
        })
        */
    })

    const returnedObj = {
        "nodes": nodes,
        "links": links
    }

    return returnedObj

}

export function parseTokenNetworkGraph(paper: any){
    let nodes = [];
    let links = [];
    nodes.push({ "id": paper.ssPaperId.toString(), 'color': 'black' })
    const returnedObj = {
        "nodes": nodes,
        "links": links
    }
    return returnedObj
}

export function nodeNameToToken(ssPaperId, tokensList) {
    let tokenChosen
    tokensList.forEach(token => {
        if (token.ssPaperId == ssPaperId) {
            tokenChosen = token
        }
    })
    return tokenChosen
}

export function seperateGraphPaperPools(returnedDataArray) {

    let returnedPannel = []

    //retrieving a list of all pools
    let listPoolsId = []
    returnedDataArray[returnedDataArray.length - 1].data[0]['whitelistPools'].forEach(WLpool => {
        listPoolsId.push(WLpool.id)
    })

    listPoolsId.forEach(poolId => {
        returnedDataArray.forEach(blockObj => {
            blockObj.data[0].whitelistPools.forEach(pool => {
                if (pool.id = poolId) {
                    returnedPannel.push({
                        block: blockObj.block,
                        id: pool.id,
                        createdAtBlockNumber: pool.createdAtBlockNumber,
                        token0Name: pool.token0.name,
                        token0Id: pool.token0.id,
                        token1Name: pool.token1.name,
                        token1Id: pool.token1.id,
                        token1Price: pool.token1Price,
                        token0Price: pool.token0Price
                    })
                }
            })
        })
    })

    return {returnedPannel, listPoolsId}
}

export function filterGraphPaperPools(pannel, poolId) {
    let returnedPannel = []
    pannel.forEach(obs => {
        if (obs.id == poolId) {
            returnedPannel.push(obs)
        }
    })
    return returnedPannel
}

export function strTruncator(str: string){
    if (str.length > 500) {
        return str.substring(0, 250) + "...";
    }
    else{
        return str
    }
}

export function timeToWrt(time: Number, wrt:string, data: any){
    let returnedWrt
    data.forEach(obs => {
        if(obs.TIMESTAMP == time){
            returnedWrt = obs[wrt]
        } 
    })
    return returnedWrt
}

export function timeToVolume(time: Number, data: any){
    let returnedVolume
    data.forEach(obs => {
        if(obs.time == time){
            returnedVolume = obs.value
        } 
    })
    return returnedVolume
}