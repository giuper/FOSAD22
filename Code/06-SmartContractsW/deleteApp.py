import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import ApplicationDeleteTxn
from utilities import wait_for_confirmation, getClient

def deleteApp(MnemFile,index,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    f=open(MnemFile,'r')
    Mnem=f.read()
    f.close()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)

    utxn=ApplicationDeleteTxn(Addr,params,index)
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
    index=int(sys.argv[2])
    directory=sys.argv[3]

    deleteApp(MnemFile,index,directory)
    
    
