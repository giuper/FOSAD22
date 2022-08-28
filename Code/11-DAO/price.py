import sys
import base64
from algosdk.future.transaction import ApplicationNoOpTxn, AssetTransferTxn, calculate_group_id
from utilities import wait_for_confirmation, getClient, getSKAddr
from daoutilities import getAssetIdFromName, DAOGovName, DAOtokenName
import algosdk.encoding as e


def proposePrice(MnemFile,appIndex,price,prefix,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(MnemFile)
    print("User addr:       ",Addr)

    appAddr=e.encode_address(e.checksum(b'appID'+appIndex.to_bytes(8, 'big')))
    print("App addr:        ",appAddr)

    assetId=getAssetIdFromName(appAddr,DAOGovName,algodClient)
    if assetId==None:
        print("Could not find asset")
        exit()
    print("Asset Id:        ",assetId)
    print("AssetName:       ",DAOGovName)

    ttxn=AssetTransferTxn(sender=Addr,sp=params,receiver=appAddr,amt=1,index=assetId)
    ctxn=ApplicationNoOpTxn(sender=Addr,sp=params,index=appIndex,app_args=[prefix.encode(),price.to_bytes(8,'big')],foreign_assets=[assetId])
    gid=calculate_group_id([ttxn,ctxn])
    ttxn.group=gid
    ctxn.group=gid
    
    sttxn=ttxn.sign(SK)
    sctxn=ctxn.sign(SK)
    try:
        txId=algodClient.send_transactions([sttxn,sctxn])
    except Exception as err:
        print("***********")
        print(err)
        return
    confirmed_txn=wait_for_confirmation(algodClient,txId,4)  


if __name__=='__main__':
    if len(sys.argv)!=6:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <price> s/b <node directory>")
        exit()

    MnemFile=sys.argv[1]
    appIndex=int(sys.argv[2])
    price=int(sys.argv[3])
    prefix=sys.argv[4]+"p"
    directory=sys.argv[5]
    proposePrice(MnemFile,appIndex,price,prefix,directory)
    

