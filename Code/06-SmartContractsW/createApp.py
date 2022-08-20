import sys
import json
import base64
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import write_to_file
from algosdk.future.transaction import ApplicationCreateTxn
from algosdk.future.transaction import OnComplete
from algosdk.future.transaction import StateSchema
from utilities import wait_for_confirmation, getClient

def main(creatorMnemFile,approvalFile,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    with open(creatorMnemFile,'r') as f:
        creatorMnem=f.read()
    creatorSK=mnemonic.to_private_key(creatorMnem)
    creatorAddr=account.address_from_private_key(creatorSK)
    print("Creator address: ",creatorAddr)

    on_complete=OnComplete.NoOpOC.real

    # declare application state storage (immutable)
    # define global schema
    global_ints=2
    global_bytes=1
    globalSchema=StateSchema(global_ints,global_bytes)

    # define local schema
    local_ints=3
    local_bytes=1
    localSchema=StateSchema(local_ints,local_bytes)

    clearProgramSource=b"""#pragma version 4 int 1 """
    clearProgramResponse=algodClient.compile(clearProgramSource.decode('utf-8'))
    clearProgram=base64.b64decode(clearProgramResponse['result'])
    
    with open(approvalFile,'r') as f:
        approvalProgramSource=f.read()
    approvalProgramResponse=algodClient.compile(approvalProgramSource)
    approvalProgram=base64.b64decode(approvalProgramResponse['result'])
    print("Hash: ",approvalProgramResponse['hash'])

    utxn=ApplicationCreateTxn(creatorAddr,params,on_complete, \
                                        approvalProgram,clearProgram, \
                                        globalSchema,localSchema)
    write_to_file([utxn],"create.utxn")

    stxn=utxn.sign(creatorSK)
    write_to_file([stxn],"create.stxn")

    txId=stxn.transaction.get_txid()
    print("Transaction id:  ",txId)
    algodClient.send_transactions([stxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    appId=txResponse['application-index']
    print("Created a new app with id: ",appId);

if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <creator mnem> <approval file> <node directory>")
        exit()

    creatorMnemFile=sys.argv[1]
    approvalFile=sys.argv[2]
    directory=sys.argv[3]

    main(creatorMnemFile,approvalFile,directory)
    
    
