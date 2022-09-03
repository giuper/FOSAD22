import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import Multisig, MultisigTransaction, PaymentTxn
from algosdk.future.transaction import retrieve_from_file
from utilities import *


def main():
    if len(sys.argv)<2:
        print("usage: python "+sys.argv[0]+" <Signed TX> [<node directory>]")
        exit()

    signedTXFile=sys.argv[1]
    if len(sys.argv)==3:
        directory=sys.argv[2]
    else:
        directory=""
    algodClient=getClient(directory)

    txInL=retrieve_from_file(signedTXFile)
    for tx in txInL:
        txid=algodClient.send_transaction(tx)
        print(f'{"Signed transaction with txID:":32s}{txid:s}')
        print()
        try:
            confirmed_txn=wait_for_confirmation(algodClient,txid,4)  
        except Exception as err:
            print(err)
            return

        print("Transaction information: {}".format(
            json.dumps(confirmed_txn, indent=2)))
        print("Decoded note: {}".format(base64.b64decode(
            confirmed_txn["txn"]["txn"]["note"]).decode()))

if __name__=='__main__':
    main()
