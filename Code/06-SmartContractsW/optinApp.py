import sys
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file
from algosdk.future.transaction import ApplicationOptInTxn
from utilities import wait_for_confirmation, getClient

def main(MnemFile,index,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    f=open(MnemFile,'r')
    Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)
    f.close()

    utxn=ApplicationOptInTxn(Addr,params,index)
    write_to_file([utxn],"optin.utxn")
    stxn=utxn.sign(SK)
    write_to_file([stxn],"optin.stxn")
    txId=stxn.transaction.get_txid()
    print("Transaction id:  ",txId)
    algodClient.send_transactions([stxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    print("OptIn to app-id: ",txResponse['txn']['txn']['apid'])  


if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    directory=sys.argv[3]

    main(MnemFile,index,directory)
    
    
