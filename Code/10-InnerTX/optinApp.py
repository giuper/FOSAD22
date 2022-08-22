import sys
import base64
import algosdk.encoding as e
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk.future.transaction import ApplicationOptInTxn, PaymentTxn
from utilities import wait_for_confirmation, getClient

def main(MnemFile,index,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    appAddr=e.encode_address(e.checksum(b'appID'+index.to_bytes(8, 'big')))
    print("app id:          ",index)
    print("app Addr:        ",appAddr)

    with open(MnemFile,'r') as f:
        Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    playerAddr=account.address_from_private_key(SK)

    note="Opt in fee"
    payTx=PaymentTxn(playerAddr,params,appAddr,500_000,None,note)
    optTx=ApplicationOptInTxn(playerAddr,params,index)

    gid=transaction.calculate_group_id([payTx, optTx])
    payTx.group=gid
    optTx.group=gid

    sPayTx=payTx.sign(SK)
    sOptTx=optTx.sign(SK)


    txId=algodClient.send_transactions([sPayTx,sOptTx])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)


if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    directory=sys.argv[3]

    main(MnemFile,index,directory)
    
    
