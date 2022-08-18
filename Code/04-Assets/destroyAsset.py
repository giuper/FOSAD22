import sys
from algosdk.v2client import algod
from algosdk import account, mnemonic, error
from algosdk.future import transaction 
from algosdk.future.transaction import AssetConfigTxn
from utilities import wait_for_confirmation, getClient
import urllib

def destroyAsset(directory,managerMNEMFile,assetID):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()
    
    with open(managerMNEMFile,'r') as f:
        managerMNEM=f.read()
    managerSK=mnemonic.to_private_key(managerMNEM)
    managerADDR=mnemonic.to_public_key(managerMNEM)
    

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
        print("Usage: python3 "+sys.argv[0]+" <NodeDir> <manager MNEM file> <asset ID>")
        exit()

    directory=sys.argv[1]
    managerMNEMFile=sys.argv[2]
    assetID=sys.argv[3]
    destroyAsset(directory,managerMNEMFile,assetID)

