import datetime
import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import write_to_file
from algosdk.future.transaction import ApplicationNoOpTxn, PaymentTxn
from utilities import wait_for_confirmation, getClient
import algosdk.encoding as e


def startApp(MnemFile,index,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    with open(MnemFile,'r') as f:
        Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)
    Pk=mnemonic.to_public_key(Mnem)

    ctxn=ApplicationNoOpTxn(sender=Addr,sp=params,index=index,app_args=["s".encode()])

    appAddr=e.encode_address(e.checksum(b'appID'+index.to_bytes(8, 'big')))
    ptxn=PaymentTxn(Addr,params,appAddr,2_000_000)
    gid=transaction.calculate_group_id([ptxn,ctxn])
    ctxn.group=gid
    ptxn.group=gid
    
    sptxn=ptxn.sign(SK)
    sctxn=ctxn.sign(SK)
    txId=algodClient.send_transactions([sptxn,sctxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)


if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    directory=sys.argv[3]
    startApp(MnemFile,index,directory)
    
