import datetime
import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file
from algosdk.future.transaction import ApplicationNoOpTxn
from algosdk.future.transaction import OnComplete
from algosdk.future.transaction import StateSchema
from utilities import wait_for_confirmation, getClient

def main(MnemFile,index,move,directory):


    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    with open(MnemFile,'r') as f:
        Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)


    appArgs=[move.to_bytes(8,'big')]
    utxn=ApplicationNoOpTxn(Addr,params,index,appArgs)

    stxn=utxn.sign(SK)

    txId=stxn.transaction.get_txid()
    print("Transaction id: ",txId)
    algodClient.send_transactions([stxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    print("Calling app:    ",txResponse['txn']['txn']['apid'])  

if __name__=='__main__':
    if len(sys.argv)!=5:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <move> <node directory>")
        exit()
    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    move=int(sys.argv[3])
    directory=sys.argv[4]
    main(MnemFile,index,incr,directory)
    
    
