import sys
import base64
from algosdk.future.transaction import ApplicationOptInTxn, AssetTransferTxn, calculate_group_id
from utilities import wait_for_confirmation, getClient, getSKAddr
import algosdk.encoding as e
from daoutilities import getAssetIdFromName, DAOtokenName

def optInDAO(MnemFile,appId,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(MnemFile)
    print("User addr:       ",Addr)

    appAddr=e.encode_address(e.checksum(b'appID'+appId.to_bytes(8, 'big')))
    accountInfo=algodClient.account_info(appAddr)
    print("App id:          ",appId)
    print("App addr:        ",appAddr)

    assetId=getAssetIdFromName(appAddr,DAOtokenName,algodClient)
    if assetId is None:
        print("Could not find asset",DAOtokenName)
        exit()
    print("Asset name:      ",DAOtokenName)
    print("Asset id:        ",assetId)

    txn1=AssetTransferTxn(sender=Addr,sp=params,receiver=Addr,amt=0,index=assetId)
    txn2=ApplicationOptInTxn(sender=Addr,sp=params,index=appId,foreign_assets=[assetId])
    gid=calculate_group_id([txn1,txn2])
    txn1.group=gid
    txn2.group=gid

    stxn1=txn1.sign(SK)
    stxn2=txn2.sign(SK)

    txId=algodClient.send_transactions([stxn1,stxn2])
    print("Transaction id:  ",txId)
    wait_for_confirmation(algodClient,txId,4)


if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    directory=sys.argv[3]

    optInDAO(MnemFile,index,directory)
    
    
