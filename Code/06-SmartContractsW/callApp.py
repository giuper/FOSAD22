import sys
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file, ApplicationNoOpTxn
from utilities import wait_for_confirmation, getClient

def main(MnemFIle,index,directory)

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    f=open(MnemFile,'r')
    Mnem=f.read()
    SK=mnemonic.to_private_key(Mnem)
    Addr=account.address_from_private_key(SK)
    f.close()


    utxn=ApplicationNoOpTxn(Addr,params,index)
    write_to_file([utxn],"noop.utxn")
    stxn=utxn.sign(SK)
    write_to_file([stxn],"noop.stxn")
    txId=stxn.transaction.get_txid()
    print("Transaction id: ",txId)
    algodClient.send_transactions([stxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    print("Calling app:    ",txResponse['txn']['txn']['apid'])  

    print("Global values from the TX output")
    if "global-state-delta" in txResponse:
        #print(txResponse['global-state-delta'])
        for variable in txResponse['global-state-delta']:
            key=variable['key']
            key=base64.b64decode(key)
            key=key.decode('utf-8')
            print("\tGlobal Key: ",key)
            #print(variable)
            if 'uint' in variable['value']:
                print("\tValue     : ",variable['value']['uint'])
            else:
                print("\tValue     : 0")

    print("Local values from the TX output")
    if "local-state-delta" in txResponse :
        #print(txResponse['local-state-delta'])
        for variable in txResponse['local-state-delta'][0]['delta']:
            #key=txResponse['local-state-delta'][0]['delta'][0]['key']
            key=variable['key']
            key=base64.b64decode(key)
            key=key.decode('utf-8')
            print("\tLocal Key : ",key)
            if 'uint' in variable['value']:
                print("\tValue     : ",variable['value']['uint'])
            else:
                print("\tValue did not change")

    print("Local values from account_info")
    result=algodClient.account_info(Addr)
    localState=result['apps-local-state']
    for st in localState:
        if(st['id']==index):
            for kk in st['key-value']:
                key=kk['key']
                key=base64.b64decode(key)
                key=key.decode('utf-8')
                print("\tKey    : ",key)
                print("\tValue  : ",kk['value']['uint'])
        

if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <mnem> <app index> <node directory>")
        exit()

    MnemFile=sys.argv[1]
    index=int(sys.argv[2])
    directory=sys.argv[3]

    main(MnemFIle,index,directory)
    
    
