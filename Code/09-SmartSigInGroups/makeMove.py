import datetime
import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import write_to_file
from algosdk.future.transaction import ApplicationNoOpTxn
from utilities import wait_for_confirmation, getClient


def makeMove(MnemFile,DealerFile,index,move,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    with open(MnemFile,'r') as f:
        Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)
    Pk=mnemonic.to_public_key(Mnem)

    with open(DealerFile,'r') as f:
        Dealer=f.read()

    appArgs=[move.to_bytes(8,'big')]
    mtxn=ApplicationNoOpTxn(Addr,params,index,appArgs)
    ptxn=transaction.PaymentTxn(sender=Pk,sp=params,receiver=Dealer,amt=1_000_000)
    gid=transaction.calculate_group_id([ptxn,mtxn])

    ptxn.group=gid
    sptxn=ptxn.sign(SK)

    mtxn.group=gid
    smtxn=mtxn.sign(SK)
    
    atomic=[sptxn,smtxn]
    
    txId=algodClient.send_transactions(atomic)
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    print("Nim on Algorand")
    print("Player with address: ",Addr)
    print("\tMove:              ",move)
    print("\tInstance:          ",index)


if __name__=='__main__':
    if len(sys.argv)!=6:
        print("usage: python3 "+sys.argv[0]+" <player mnem> <dealer addr> <app index> <move> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    DealerFile=sys.argv[2]
    index=int(sys.argv[3])
    move=int(sys.argv[4])
    directory=sys.argv[5]
    makeMove(MnemFile,DealerFile,index,move,directory)
    
