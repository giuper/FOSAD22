import sys
#import json
import base64
#from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import ApplicationClearStateTxn, AssetCloseOutTxn
from utilities import wait_for_confirmation, getClient, getSKAddr
import algosdk.encoding as e
from daoutilities import getAssetIdFromName, getAssetCreator, DAOtokenName

def clearDAO(MnemFile,appId,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(MnemFile)
    print("User addr:",Addr)

    appAddr=e.encode_address(e.checksum(b'appID'+appId.to_bytes(8, 'big')))
    accountInfo=algodClient.account_info(appAddr)
    print("App id:   ",appId)
    print("App addr: ",appAddr)

    
    assetId=getAssetIdFromName(appAddr,DAOtokenName,algodClient)
    if assetId is None:
        print("Could not find asset",DAOtokenName)
    else:
        creator=getAssetCreator(assetId,algodClient)
        print(f'Asset {DAOtokenName} found with id {assetId}')
        if creator!=Addr:
            print("Creator:  ",creator)
            utxn=AssetCloseOutTxn(sender=Addr,sp=params,receiver=creator,index=assetId)
            stxn=utxn.sign(SK)
            txId=algodClient.send_transaction(stxn)
            wait_for_confirmation(algodClient,txId,4)
            txResponse=algodClient.pending_transaction_info(txId)
            print(f'Asset {DAOtokenName} cleared')
        else:
            print(f'You are the creator')
            exit()

    utxn=ApplicationClearStateTxn(Addr,params,appId)
    stxn=utxn.sign(SK)
    txId=algodClient.send_transaction(stxn)
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    print(f'Application {appId} cleared')


if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    appId=int(sys.argv[2])
    directory=sys.argv[3]

    clearDAO(MnemFile,appId,directory)
    
    
