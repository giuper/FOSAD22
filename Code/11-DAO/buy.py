import sys
import base64
#from algosdk import account, mnemonic
#from algosdk.v2client import algod
#from algosdk.future import transaction
from algosdk.future.transaction import ApplicationNoOpTxn, PaymentTxn,calculate_group_id
from utilities import wait_for_confirmation, getClient, getSKAddr
import algosdk.encoding as e
from daoutilities import getAssetIdFromName, getSellingPrice, DAOtokenName

def buy(MnemFile,appIndex,nAssets,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(MnemFile)
    print("User Addr:",Addr)

    appAddr=e.encode_address(e.checksum(b'appID'+appIndex.to_bytes(8, 'big')))
    print("App Addr: ",appAddr)

    price=getSellingPrice(appIndex,algodClient)
    if price is None:
        print("Cannot find price")
        exit()
    print("Price:    ",price)

    assetId=getAssetIdFromName(appAddr,DAOtokenName,algodClient)
    if assetId is None:
        print(f'Asset {assetName} not found')
    print("Asset Id: ",assetId)



    ptxn=PaymentTxn(sender=Addr,sp=params,receiver=appAddr,amt=price*nAssets)
    ctxn=ApplicationNoOpTxn(sender=Addr,sp=params,index=appIndex,app_args=["b".encode(),nAssets.to_bytes(8,'big')],foreign_assets=[assetId])
    appAddr=e.encode_address(e.checksum(b'appID'+appIndex.to_bytes(8, 'big')))
    gid=calculate_group_id([ptxn,ctxn])
    ptxn.group=gid
    ctxn.group=gid
    
    sptxn=ptxn.sign(SK)
    sctxn=ctxn.sign(SK)
    try:
        txId=algodClient.send_transactions([sptxn,sctxn])
    except Exception as err:
        print("***********")
        print(err)
        return
    confirmed_txn=wait_for_confirmation(algodClient,txId,4)  


if __name__=='__main__':
    if len(sys.argv)!=5:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <nAssets> <node directory>")
        exit()

    mnemFile=sys.argv[1]
    appIndex=int(sys.argv[2])
    nAssets=int(sys.argv[3])
    directory=sys.argv[4]
    buy(mnemFile,appIndex,nAssets,directory)
    
