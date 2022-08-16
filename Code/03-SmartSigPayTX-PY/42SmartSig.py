import sys
import base64

from algosdk.future import transaction
from algosdk import mnemonic
from algosdk.v2client import algod
from utilities import wait_for_confirmation, getClient

def main():
    if len(sys.argv)!=4:
        print("Usage: ",sys.argv[0],"<receiver ADDR file> <TEAL program file> <nodeDir>")
        exit()
    
    receiverADDRFile=sys.argv[1]
    with open(receiverADDRFile,'r') as f:
        receiver=f.read()

    directory=sys.argv[3]
    algodClient=getClient(directory)
    
    # Read TEAL program
    TEALprogram=sys.argv[2]
    with open(TEALprogram, 'r') as f:
        data=f.read()
    # Compile TEAL program
    response=algodClient.compile(data)

    sender=response['hash']
    closeremainderto=receiver
    amount=230_000
    params=algodClient.suggested_params()
    txn = transaction.PaymentTxn(
            sender,params,receiver,amount,closeremainderto)
    
    
    # Create logic sig
    programstr=response['result']

    print("Response Result =",programstr)
    print("Response Hash   =",sender)
    
    t=programstr.encode()
    program=base64.decodebytes(t)
    
    # Create arg to pass if TEAL program requires an arg,
    # if not, omit args param
    # string parameter
    
    arg_str="42"
    arg1=arg_str.encode()
    lsig=transaction.LogicSig(program, args=[arg1])
    
    # Create the LogicSigTransaction with contract account LogicSig
    lstx=transaction.LogicSigTransaction(txn,lsig)
    transaction.write_to_file([lstx],sys.argv[0][:-3]+".stxn")

    # Send raw LogicSigTransaction to network
    try:
        txid = algodClient.send_transaction(lstx)
        print("Transaction ID  = "+txid)
    except Exception as e:
        print(e)
        exit()
    
    wait_for_confirmation(algodClient, txid,4)

if __name__=='__main__':
    main()
