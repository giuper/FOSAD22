import sys
import base64
from algosdk.v2client import algod
from algosdk.future.transaction import ApplicationNoOpTxn, PaymentTxn, calculate_group_id
from utilities import wait_for_confirmation, getClient, getSKAddr
import algosdk.encoding as e


def startApp(mnemFile,index,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(mnemFile)
    print("User address:    ",Addr)

    #transfer to fund the application
    appAddr=e.encode_address(e.checksum(b'appID'+index.to_bytes(8, 'big')))
    ptxn=PaymentTxn(Addr,params,appAddr,2_000_000)

    #application call to start as indicated by argument s
    ctxn=ApplicationNoOpTxn(sender=Addr,sp=params,index=index,app_args=["s".encode()])

    gid=calculate_group_id([ptxn,ctxn])
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
    
