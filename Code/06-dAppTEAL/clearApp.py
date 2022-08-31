import sys
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import ApplicationClearStateTxn
from utilities import wait_for_confirmation, getClient, getSKAddr

def main(MnemFile,index,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    SK,Addr=getSKAddr(MnemFile):

    utxn=ApplicationClearStateTxn(Addr,params,index)
    stxn=utxn.sign(SK)
    txId=stxn.transaction.get_txid()
    print("Transaction id: ",txId)

    algodClient.send_transactions([stxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    print("app-id cleared: ",txResponse['txn']['txn']['apid'])  


if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    directory=sys.argv[3]

    main(MnemFile,index,directory)
    
    
