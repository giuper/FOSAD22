import sys
import base64

from algosdk.future import transaction
from algosdk import mnemonic
from algosdk.v2client import algod
from utilities import wait_for_confirmation, getClient

def main():
    if len(sys.argv)!=5:
        print("Usage: ",sys.argv[0],"<receiver ADDR file> <TEAL program file> <argument> <nodeDir>")
        exit()
    
    receiverADDRFile=sys.argv[1]
    myprogram=sys.argv[2]
    arg_str=sys.argv[3]
    directory=sys.argv[4]
    
    print(arg_str)
    algodClient=getClient(directory)
    amount=230_000
    
    # Read TEAL program
    with open(myprogram, 'r') as f:
        data=f.read()
    
    # Compile TEAL program
    response=algodClient.compile(data)
    sender=response['hash']
    programstr=response['result']
    print("Response Result = "+programstr)
    print("Response Hash   = "+sender)
    
    # Create logic sig
    t=programstr.encode()
    program=base64.decodebytes(t)
    
    # Create arg to pass if TEAL program requires an arg,
    # if not, omit args param
    # string parameter
    
    #arg_str="weather comfort erupt verb pet range endorse exhibit tree brush crane man"

    arg_str="827154396965327148341689752593468271472513689618972435786235914154796823239841567"
    arg1=arg_str.encode()
    lsig=transaction.LogicSig(program, args=[arg1])
    with open(receiverADDRFile,'r') as f:
        receiver=f.read()
    closeremainderto=receiver
    params=algodClient.suggested_params()
    txn = transaction.PaymentTxn(
            sender,params,receiver,amount,closeremainderto)
    
    # Create the LogicSigTransaction with contract account LogicSig
    lstx=transaction.LogicSigTransaction(txn,lsig)
    transaction.write_to_file([lstx],sys.argv[0][:-3]+".stxn")
    # Send raw LogicSigTransaction to network
    try:
        txid=algodClient.send_transaction(lstx)
        print("Transaction ID  = "+txid)
    except Exception as e:
        print(e)
        exit()
    
    wait_for_confirmation(algodClient,txid,4)

if __name__=='__main__':
    main()
