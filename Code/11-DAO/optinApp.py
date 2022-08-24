import sys
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file
from algosdk.future.transaction import ApplicationOptInTxn,AssetTransferTxn
from utilities import wait_for_confirmation, getClient

def main(MnemFile,appId,assetId,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    with open(MnemFile,'r') as f:
        Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)
    print("User addr:       ",Addr)
    print("Asset:           ",assetId)
    txn=AssetTransferTxn(sender=Addr,
            sp=params,receiver=Addr,amt=0,index=assetId)
    stxn=txn.sign(SK)
    txId=stxn.transaction.get_txid()
    algodClient.send_transaction(stxn)
    print("Transaction id:  ",txId)
    wait_for_confirmation(algodClient,txId,4)
    print("Done")

    print("Application:     ",appId)
    utxn=ApplicationOptInTxn(sender=Addr,sp=params,index=appId,foreign_assets=[assetId])
    stxn=utxn.sign(SK)
    txId=stxn.transaction.get_txid()
    print("Transaction id:  ",txId)
    algodClient.send_transaction(stxn)
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    print("OptIn to app-id: ",txResponse['txn']['txn']['apid'])  


if __name__=='__main__':
    if len(sys.argv)!=5:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <assetId> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    assetId=int(sys.argv[3])
    directory=sys.argv[4]

    main(MnemFile,index,assetId,directory)
    
    
