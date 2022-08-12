import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import Multisig, MultisigTransaction, PaymentTxn, write_to_file
from utilities import *


def multiPayTX(mnems,mSig,rAddr,amount,algodClient):

    if len(mnems)<mSig.threshold:
        print("Error")
        exit()

    # build transaction
    params = algodClient.suggested_params()
    note="Ciao MultiPino!!!".encode()

    mAddr=mSig.address()
    #create transaction
    unsignedTx=PaymentTxn(mAddr,params,rAddr,amount,None,note)
    write_to_file([unsignedTx],"TX/MultiPay.utx")
    mTx=MultisigTransaction(unsignedTx,mSig)
    write_to_file([mTx],"TX/MultiPayWithPK.utx")

    # sign transaction
    for i in range(mSig.threshold):
        sk=mnemonic.to_private_key(mnems[i])
        mTx.sign(sk)
        
    write_to_file([mTx],"TX/MultiPay.stx")

    # submit transaction
    txid=algodClient.send_transaction(mTx)
    print(f'{"Signed transaction with txID:":31s}{txid:s}')

# wait for confirmation 
    try:
        confirmed_txn=wait_for_confirmation(algodClient,txid,4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    decodedNote=base64.b64decode(confirmed_txn["txn"]["txn"]["note"]).decode()
    print(f'{"Decoded note:":17s}{decodedNote:s}')

def main():
    if len(sys.argv)!=8:
        print("usage: python3 "+sys.argv[0]+" <Addr1> <Addr2> <Addr3> <Mnem1> <Mnem2> <Receiver Addr> <node directory>")
        exit()

    amount=1_000_000
    version=1
    threshold=2
    
    accounts=[]
    for filename in sys.argv[1:4]:
        with open(filename,'r') as f:
            acc=f.read()
        accounts.append(acc)
    mSig=Multisig(version,threshold,accounts)
    print(f'{"Multisig Address: ":31s}{mSig.address():s}')

    mnems=[]
    for i in range(4,6):
        with open(sys.argv[i],'r') as f:
            mnem=f.read()
        mnems.append(mnem)
    
    with open(sys.argv[6],'r') as f:
        receiver=f.read()
    
    directory=sys.argv[7]
    algodClient=getClient(directory)
    account_info=algodClient.account_info(mSig.address())
    balance=account_info.get('amount')
    print(f'{"Account balance:":31s}{balance:d}{" microAlgos"}')

    multiPayTX(mnems,mSig,receiver,amount,algodClient)

    account_info=algodClient.account_info(mSig.address())
    balance=account_info.get('amount')
    print(f'{"Account balance:":17s}{balance:d}{" microAlgos"}')

if __name__=='__main__':
    main()
