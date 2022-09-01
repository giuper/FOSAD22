import sys
from algosdk import error
from algosdk.future.transaction import AssetConfigTxn
from utilities import wait_for_confirmation, getClient, getSKAddr

def destroyAsset(directory,managerMNEMFile,assetID):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()
    
    managerSK,managerADDR=getSKAddr(managerMNEMFile)
    

    txn=AssetConfigTxn(sender=managerADDR,sp=params,index=assetID,strict_empty_address_check=False)
    stxn=txn.sign(managerSK)

    try:
        txid=algodClient.send_transaction(stxn)
        wait_for_confirmation(algodClient,txid,4)
    except error.AlgodHTTPError as e:
        print(e)
        
    return 
    

if __name__=="__main__":
    if (len(sys.argv)!=4):
        print("Usage: python",sys.argv[0],"<manager MNEM file> <asset ID> <NodeDir>")
        exit()

    managerMNEMFile=sys.argv[1]
    assetID=sys.argv[2]
    directory=sys.argv[3]
    destroyAsset(directory,managerMNEMFile,assetID)

