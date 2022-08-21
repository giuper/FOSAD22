import sys
import base64

from algosdk.future import transaction
from algosdk.v2client import algod
from utilities import wait_for_confirmation, getClient

def smartSig(receiver,myprogram,directory):
    
    algodClient=getClient(directory)
    
    # Read TEAL program and compile
    with open(myprogram, 'r') as f:
        data=f.read()
    response=algodClient.compile(data)
    sender=response['hash']
    print("Response Hash   = ",sender)
    programstr=response['result']

    # Create logic sig program+args
    t=programstr.encode()
    program=base64.decodebytes(t)
    args=["827154396".encode(),
          "965327148".encode(),
          "341689752".encode(),
          "593468271".encode(),
          "472513689".encode(),
          "618972435".encode(),
          "786235914".encode(),
          "154796823".encode(),
          "239841567".encode()]
    lsig=transaction.LogicSig(program, args)

    #Create transaction
    params=algodClient.suggested_params()
    amount=230_000
    closeremainderto=receiver
    txn = transaction.PaymentTxn(
            sender,params,receiver,amount,closeremainderto)

    lstx=transaction.LogicSigTransaction(txn,lsig)

    # Send raw LogicSigTransaction to network
    try:
        txid=algodClient.send_transaction(lstx)
        print("Transaction ID  = ",txid)
    except Exception as e:
        print(e)
        exit()
    
    wait_for_confirmation(algodClient,txid,4)

if __name__=='__main__':
    if len(sys.argv)!=4:
        print("Usage: ",sys.argv[0],"<receiver ADDR file> <TEAL program file> <nodeDir>")
        exit()

    receiverADDRFile=sys.argv[1]
    with open(receiverADDRFile,'r') as f:
        receiver=f.read()
    myprogram=sys.argv[2]
    directory=sys.argv[3]
    smartSig(receiver,myprogram,directory)
