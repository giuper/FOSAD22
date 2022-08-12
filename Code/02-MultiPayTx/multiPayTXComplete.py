import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import Multisig, MultisigTransaction, PaymentTxn, write_to_file


def multiPayTX(sKey,mSig,rAddr,amount,algodClient):

    if len(sKey)<mSig.threshold:
        print("Error")
        exit()

    # build transaction
    params = algodClient.suggested_params()
    note="Ciao MultiPino!!!".encode()

    sAddr=mSig.address()
    #create transaction
    unsignedTx=PaymentTxn(sAddr,params,rAddr,amount,None,note)
    write_to_file([unsignedTx],"TX/MultiPay.utx")

    mTx=MultisigTransaction(unsignedTx,mSig)
    write_to_file([mTx],"TX/MultiPayWithPK.utx")

    
    # sign transaction
    for i in range(mSig.threshold):
        mTx.sign(mnemonic.to_private_key(sKey[i]))
        
    write_to_file([mTx],"TX/MultiPay.stx")

    # submit transaction
    txid=algodClient.send_transaction(mTx)
    #print("Signed transaction with txID: {}".format(txid))
    print(f'{"Signed transaction with txID:":32s}{txid:s}')
    print()

# wait for confirmation 
    try:
        confirmed_txn=wait_for_confirmation(algodClient,txid,4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    account_info = algodClient.account_info(sAddr)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

# utility function for waiting on a transaction confirmation
def wait_for_confirmation(client, transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait    
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return 
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:  
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)                   
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))


def main():
    if len(sys.argv)!=8:
        print("usage: python3 "+sys.argv[0]+" <Addr1> <Addr2> <Addr3> <Key1> <Key2> <AddrRec> <node directory>")
        exit()

    amount=1_000_000
    version=1
    threshold=2
    
    accounts=[]
    for i in range(1,4):
        f=open(sys.argv[i]+".addr",'r')
        acc=f.read()
        accounts.append(acc)
        f.close()
    mSig=Multisig(version,threshold,accounts)
    print(f'{"Multisig Address: ":32s}{mSig.address():s}')

    keys=[]
    for i in range(4,6):
        f=open(sys.argv[i]+".mnem",'r')
        Key=f.read()
        keys.append(Key)
        f.close()
    
    f=open(sys.argv[6]+".addr",'r')
    receiver=f.read()
    f.close()
    
    directory=sys.argv[7]
    f=open(directory+"/algod.net",'r')
    algodAddr="http://"+f.read()[:-1]   #to remove the trailing newline
    f.close()
    f=open(directory+"/algod.token",'r')
    algodTok=f.read()
    f.close()
    algodClient = algod.AlgodClient(algodTok,algodAddr)

    account_info = algodClient.account_info(mSig.address())
    balance=account_info.get('amount')
    print(f'{"Account balance:":22s}{balance:d}{" microAlgos"}')

    multiPayTX(keys,mSig,receiver,amount,algodClient)


if __name__=='__main__':
    main()
