import base64
from algosdk import account

DAOtokenName="FOSAD22Token"
DAOGovName="FOSAD22-Gov"

#return list of all assets
def getAllAssets(Addr,algodClient):
    accountInfo=algodClient.account_info(Addr)
    return [asset['asset-id'] for asset in accountInfo['assets']]

#get id of asset created by Addr with name assetName
def getAssetIdFromName(Addr,assetName,algodClient):
    accountInfo=algodClient.account_info(Addr)
    assetId=None
    for asset in accountInfo['created-assets']:
        if asset['params']['name']==assetName:
            assetId=asset['index']
            break
    return assetId

#get the value of a global variable
def getGlobalVar(appIndex,varName,algodClient):
    app=algodClient.application_info(appIndex)
    for kk in app['params']['global-state']:
        key=kk['key']
        key=base64.b64decode(key)
        key=key.decode('utf-8')
        if key==varName:
            return kk['value']['uint']

#get the selling price
def getSellingPrice(appIndex,algodClient):
   return getGlobalVar(appIndex,"scurrentPrice",algodClient)

#returns the list of all opeted-in apps 
def getAllApps(Addr,algodClient):
    accountInfo=algodClient.account_info(Addr)
    return [app['id'] for app in accountInfo["apps-local-state"]]


#generic used for debugging
def assetInfo(index,algodClient):
    assetInfo=algodClient.asset_info(index)
    print(assetInfo.keys())
    print(assetInfo['index'])
    print(assetInfo['params'])

def getAssetClawback(index,algodClient):
    try:
        assetInfo=algodClient.asset_info(index)
    except Exception as err:
        return None
    return assetInfo['params']['clawback']

def getAssetCreator(index,algodClient):
    try:
        assetInfo=algodClient.asset_info(index)
    except Exception as err:
        return None
    return assetInfo['params']['creator']
    
def getAmountAssetFromAddrIndex(Addr,index,algodClient):
    accountInfo=algodClient.account_info(Addr)
    for asset in accountInfo['assets']:
        if asset['asset-id']==index:
            return asset['amount']
        
def getAssetFromAddr(Addr,algodClient):
    accountInfo=algodClient.account_info(Addr)
    print(accountInfo['assets'][0].keys())
