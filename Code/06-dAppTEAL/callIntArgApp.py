import sys
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file, ApplicationNoOpTxn
from utilities import wait_for_confirmation, getClient

def main(MnemFile,index,incr,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    f=open(MnemFile,'r')
    Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)
    f.close()

    appArgs=[incr.to_bytes(8,'big')]
    utxn=ApplicationNoOpTxn(Addr,params,index,appArgs)
    write_to_file([utxn],"noop.utxn")
    stxn=utxn.sign(SK)
    write_to_file([stxn],"noop.stxn")
    txId=stxn.transaction.get_txid()
    print("Transaction id: ",txId)
    algodClient.send_transactions([stxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    print("Calling app:    ",txResponse['txn']['txn']['apid'])  

    print("\nGlobal values from the TX output")
    if "global-state-delta" in txResponse :
        #print(txResponse['global-state-delta'])
        for variable in txResponse['global-state-delta']:
            key=variable['key']
            key=base64.b64decode(key)
            key=key.decode('utf-8')
            print("Global Key: ",key)
            if 'uint' in variable['value']:
                print("Value:      ",variable['value']['uint'])
            else:
                print("Value:      0")

    print("\nLocal values from the TX output")
    if "local-state-delta" in txResponse :
        #print(txResponse['local-state-delta'])
        for variable in txResponse['local-state-delta'][0]['delta']:
            #key=txResponse['local-state-delta'][0]['delta'][0]['key']
            key=variable['key']
            key=base64.b64decode(key)
            key=key.decode('utf-8')
            print("Local Key:  ",key)
            if 'uint' in variable['value']:
                print("Value:      ",variable['value']['uint'])
            if 'bytes' in variable['value']:
                val=variable['value']['bytes']
                val=base64.b64decode(val)
                val=val.decode('utf-8')
                print("Value:      ",val)

    print("\nLocal values from account_info")
    result=algodClient.account_info(Addr)
    if 'apps-local-state' in result:
        localState=result['apps-local-state']
        for st in localState:
            if(st['id']==index):
                if 'key-value' in st:
                    for kk in st['key-value']:
                        key=kk['key']
                        key=base64.b64decode(key)
                        key=key.decode('utf-8')
                        print("Key:        ",key)
                        if 'uint' in kk['value']:
                            print("Value:      ",kk['value']['uint'])
         


if __name__=='__main__':
    if len(sys.argv)!=5:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <incr> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    incr=int(sys.argv[3])
    directory=sys.argv[4]

    main(MnemFile,index,incr,directory)
    
