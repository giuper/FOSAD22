import sys
from algosdk.future.transaction import AssetTransferTxn
import algosdk.encoding as e
from utilities import wait_for_confirmation, getClient, getSKAddr
from daoutilities import getAssetIdFromName, DAOGovName

def transfer(directory,senderMNEMFile,appId):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()
    
    senderSK,senderAddr=getSKAddr(senderMNEMFile)

    appAddr=e.encode_address(e.checksum(b'appID'+appId.to_bytes(8, 'big')))

    assetId=getAssetIdFromName(appAddr,DAOGovName,algodClient)
    if assetId==None:
        print("Could not find asset")
    print("Asset id: ",assetId)
    txn=AssetTransferTxn(sender=senderAddr,sp=params,receiver=appAddr,amt=1,index=assetId)
    stxn=txn.sign(senderSK)
    txid=algodClient.send_transaction(stxn)
    print("Tx id:    ",txid)

    wait_for_confirmation(algodClient,txid,4)
    exit()


if __name__=="__main__":
    if (len(sys.argv)!=4):
        print("Usage: python3 "+sys.argv[0],"<sender MNEM file> <appId> <NodeDir>")
        exit()
    senderMNEMFile=sys.argv[1]
    appId=int(sys.argv[2])
    directory=sys.argv[3]

    transfer(directory,senderMNEMFile,appId)
