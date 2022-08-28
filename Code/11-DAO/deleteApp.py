import sys
#import base64
from algosdk.future.transaction import ApplicationDeleteTxn
from utilities import wait_for_confirmation, getClient, getSKAddr
import algosdk.encoding as e
from daoutilities import getAssetIdFromName, DAOGovName, DAOtokenName

def deleteApp(mnemFile,appId,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(mnemFile)
    print("User addr:",Addr)

    appAddr=e.encode_address(e.checksum(b'appID'+appId.to_bytes(8, 'big')))
    accountInfo=algodClient.account_info(appAddr)
    print("App id:   ",appId)
    print("App addr: ",appAddr)
    
    assetId1=getAssetIdFromName(appAddr,DAOGovName,algodClient)
    if assetId1 is None:
        print("Could not find asset",DAOGovName)
        exit()
    
    assetId2=getAssetIdFromName(appAddr,DAOtokenName,algodClient)
    if assetId2 is None:
        print("Could not find asset",DAOtokenName)
        exit()


    utxn=ApplicationDeleteTxn(sender=Addr,sp=params,index=appId,foreign_assets=[assetId1,assetId2])
    stxn=utxn.sign(SK)
    txId=stxn.transaction.get_txid()
    print("Tx id:    ",txId)
    algodClient.send_transactions([stxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    print("Deleted:  ",txResponse['txn']['txn']['apid'])  


if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    appId=int(sys.argv[2])
    directory=sys.argv[3]

    deleteApp(MnemFile,appId,directory)
    
    
