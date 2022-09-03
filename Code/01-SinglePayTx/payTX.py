import sys
import json
import base64
from algosdk import account
from algosdk.future.transaction import PaymentTxn, write_to_file

from utilities import *

def payTX(sKey,sAddr,rAddr,amount,algodClient,verbose=True):

    params = algodClient.suggested_params()
    note="Ciao Pino!!!".encode()
    unsignedTx=PaymentTxn(sAddr,params,rAddr,amount,None,note)

    if verbose:
        write_to_file([unsignedTx],"TX/Pay.utx")

    signedTx=unsignedTx.sign(sKey)
    if verbose:
        write_to_file([signedTx],"TX/Pay.stx")

    txid=algodClient.send_transaction(signedTx)
    print(f'{"Signed transaction with txID:":32s}{txid:s}')
    print()

# wait for confirmation 
    try:
        confirmed_txn=wait_for_confirmation(algodClient,txid,4)  
    except Exception as err:
        print(err)
        return

    print(f'{"Decoded note:":32s}{format(base64.b64decode(confirmed_txn["txn"]["txn"]["note"]).decode())}')
    account_info=algodClient.account_info(sAddr)
    balance=account_info.get('amount')
    print(f'{"Account balance:":32s}{balance:>8d} microAlgos')

    print(f'Transaction information:\n{format(json.dumps(confirmed_txn,indent=2))}')

def makePayment(senderKeyF,receiverAddrF,directory):

    amount=1_000_000 #one million microAlgos=1 Algo

    algodClient=getClient(directory)
    sKey,sAddr=getSKAddr(senderKeyF)
    account_info = algodClient.account_info(sAddr)
    balance=account_info.get('amount')
    print(f'{"Sender address:":32s}{sAddr:s}')
    print(f'{"Account balance:":32s}{balance:>8d} microAlgos')

    with open(receiverAddrF,'r') as f:
        rAddr=f.read()
    print(f'{"Receiver address:":32s}{rAddr:s}')

    if (amount>balance):
        print("Insufficient funds")
        return
    payTX(sKey,sAddr,rAddr,amount,algodClient)

if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python",sys.argv[0],"<file with sender mnem> <file with receiver addr> <node directory>")
        exit()
    senderKeyF=sys.argv[1]
    receiverAddrF=sys.argv[2]
    directory=sys.argv[3]
    makePayment(senderKeyF,receiverAddrF,directory)
