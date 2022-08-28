import sys
import base64
#from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file
from algosdk.future.transaction import ApplicationOptInTxn,AssetTransferTxn
from utilities import wait_for_confirmation, getClient
import algosdk.encoding as e
from daoutilities import getAssetIdFromName
from utilities import wait_for_confirmation, getClient, getSKAddr

def optInDAO(MnemFile,appId,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(MnemFile)
    print("User addr:       ",Addr)

    appAddr=e.encode_address(e.checksum(b'appID'+appId.to_bytes(8, 'big')))
    accountInfo=algodClient.account_info(appAddr)
    print("App id:          ",appId)
    print("App addr:        ",appAddr)

    assetId1=getAssetIdFromName(appAddr,"FosadDAO-VotingRight3",algodClient)
    assetId2=getAssetIdFromName(appAddr,"FosadDAO3",algodClient)
    if assetId1 is None or assetId2 is None:
        print("Could not find asset")
        exit()
    print("Asset id1:       ",assetId1)
    print("Asset id2:       ",assetId2)
    txn=AssetTransferTxn(sender=Addr,
            sp=params,receiver=Addr,amt=0,index=assetId1)
    stxn=txn.sign(SK)
    txId=stxn.transaction.get_txid()
    algodClient.send_transaction(stxn)
    print("Transaction id:  ",txId)
    wait_for_confirmation(algodClient,txId,4)
    print("Done 1")
    txn=AssetTransferTxn(sender=Addr,
            sp=params,receiver=Addr,amt=0,index=assetId2)
    stxn=txn.sign(SK)
    txId=stxn.transaction.get_txid()
    algodClient.send_transaction(stxn)
    print("Transaction id:  ",txId)
    wait_for_confirmation(algodClient,txId,4)
    print("Done 2")

    utxn=ApplicationOptInTxn(sender=Addr,sp=params,index=appId,foreign_assets=[assetId1,assetId2])
    stxn=utxn.sign(SK)
    txId=stxn.transaction.get_txid()
    print("Transaction id:  ",txId)
    algodClient.send_transaction(stxn)
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    print("Opt in App id:   ",appId)


if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    directory=sys.argv[3]

    optInDAO(MnemFile,index,directory)
    
    
