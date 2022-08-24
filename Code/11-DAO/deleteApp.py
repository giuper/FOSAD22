import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import ApplicationDeleteTxn
from utilities import wait_for_confirmation, getClient
import algosdk.encoding as e

def deleteApp(MnemFile,appId,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    with open(MnemFile,'r') as f:
        Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)

    appAddr=e.encode_address(e.checksum(b'appID'+appId.to_bytes(8, 'big')))
    accountInfo=algodClient.account_info(appAddr)
    print("App id:   ",appId)
    print("App addr: ",appAddr)
    assetId1=None
    assetId2=None
    for asset in accountInfo['created-assets']:
        if asset['params']['name']=="FosadDAO3":
            assetId1=asset['index']
        if asset['params']['name']=="FosadDAO-VotingRight3":
            assetId2=asset['index']
    if assetId1==None or assetId2==None:
        print("Could not find assets")
        exit()
    print("Asset id: ",assetId1)
    print("Asset id: ",assetId2)


    utxn=ApplicationDeleteTxn(sender=Addr,sp=params,index=appId,foreign_assets=[assetId1,assetId2])
    stxn=utxn.sign(SK)
    txId=stxn.transaction.get_txid()
    print("Transaction id: ",txId)
    algodClient.send_transactions([stxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    print("Deleted app-id: ",txResponse['txn']['txn']['apid'])  


if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    appId=int(sys.argv[2])
    directory=sys.argv[3]

    deleteApp(MnemFile,appId,directory)
    
    
