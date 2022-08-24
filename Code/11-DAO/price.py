import datetime
import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import write_to_file
from algosdk.future.transaction import ApplicationNoOpTxn, AssetTransferTxn
from utilities import wait_for_confirmation, getClient
import algosdk.encoding as e


def setPrice(MnemFile,appIndex,assetId,price,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    with open(MnemFile,'r') as f:
        Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)

    ctxn=ApplicationNoOpTxn(sender=Addr,sp=params,index=appIndex,app_args=["p".encode(),price.to_bytes(8,'big')],foreign_assets=[assetId])
    appAddr=e.encode_address(e.checksum(b'appID'+appIndex.to_bytes(8, 'big')))
    print("App addr:  ",appAddr)
    print("Asset Id:  ",assetId)
    ttxn=AssetTransferTxn(sender=Addr,sp=params,
                receiver=appAddr,amt=1,index=assetId)
    gid=transaction.calculate_group_id([ttxn,ctxn])
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
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <assetId> <price> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    appIndex=int(sys.argv[2])
    assetId=int(sys.argv[3])
    price=int(sys.argv[4])
    directory=sys.argv[5]
    setPrice(MnemFile,appIndex,assetId,price,directory)
    

