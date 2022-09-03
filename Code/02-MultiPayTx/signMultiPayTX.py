import sys
from algosdk import mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file, retrieve_from_file
import base64

def main():
    if len(sys.argv)!=4:
        print("usage: python "+sys.argv[0]+" <Key> <TXin> <TXout>")
        exit()

    keyFileName=sys.argv[1]
    TXinFileName=sys.argv[2]
    TXoutFileName=sys.argv[3]

    txInL=retrieve_from_file(TXinFileName)
    
    with open(keyFileName,'r') as keyFile:
        key=keyFile.read()
    for txn in txInL:
        txnd=txn.dictify()
        print("Signing txn for amount: ",txnd['txn']['amt'])
        txn.sign(mnemonic.to_private_key(key))
    
    write_to_file(txInL,TXoutFileName)


if __name__=='__main__':
    main()
