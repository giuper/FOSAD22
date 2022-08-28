import sys
import base64
#from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file
from algosdk.future.transaction import ApplicationOptInTxn,AssetTransferTxn
from utilities import wait_for_confirmation, getClient, getSKAddr
import algosdk.encoding as e
from daoutilities import getAssetIdFromName

def optInDAO(MnemFile,appId,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(MnemFile)
    print("User addr:       ",Addr)

    appAddr=e.encode_address(e.checksum(b'appID'+appId.to_bytes(8, 'big')))
    accountInfo=algodClient.account_info(appAddr)
    print("App id:          ",appId)
    print("App addr:        ",appAddr)

    assetName="FosadDAO3"
    assetId=getAssetIdFromName(appAddr,assetName,algodClient)
    if assetId is None:
        print("Could not find asset",assetName)
        exit()
    print("Asset name:      ",assetName)
    print("Asset id:        ",assetId)

    txn=AssetTransferTxn(sender=Addr,
            sp=params,receiver=Addr,amt=0,index=assetId)
    stxn=txn.sign(SK)
    txId=stxn.transaction.get_txid()
    algodClient.send_transaction(stxn)
    print("Transaction id:  ",txId)
    wait_for_confirmation(algodClient,txId,4)
    print("Done opt-in:     ",assetName)

    utxn=ApplicationOptInTxn(sender=Addr,sp=params,index=appId,foreign_assets=[assetId])
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
    
    
