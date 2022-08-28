import sys
import base64
from algosdk import account, mnemonic
from algosdk.future.transaction import ApplicationCreateTxn
from algosdk.future.transaction import OnComplete, StateSchema
from utilities import wait_for_confirmation, getClient, getSKAddr
import algosdk.encoding as e

def main(creatorMnemFile,approvalFile,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()

    creatorSK,creatorAddr=getSKAddr(creatorMnemFile)
    print("Creator address: ",creatorAddr)


    # declare application state storage (immutable)
    # define global schema
    global_ints=8
    global_bytes=3
    globalSchema=StateSchema(global_ints,global_bytes)

    # define local schema
    local_ints=0
    local_bytes=0
    localSchema=StateSchema(local_ints,local_bytes)

    clearProgramSource=b"""#pragma version 4 int 1 """
    clearProgramResponse=algodClient.compile(clearProgramSource.decode('utf-8'))
    clearProgram=base64.b64decode(clearProgramResponse['result'])
    
    with open(approvalFile,'r') as f:
        approvalProgramSource=f.read()
    approvalProgramResponse=algodClient.compile(approvalProgramSource)
    approvalProgram=base64.b64decode(approvalProgramResponse['result'])

    on_complete=OnComplete.NoOpOC.real
    utxn=ApplicationCreateTxn(creatorAddr,params,on_complete, \
                                        approvalProgram,clearProgram, \
                                        globalSchema,localSchema)
    stxn=utxn.sign(creatorSK)

    txId=stxn.transaction.get_txid()
    print("Transaction id:  ",txId)
    algodClient.send_transactions([stxn])
    wait_for_confirmation(algodClient,txId,4)
    txResponse=algodClient.pending_transaction_info(txId)
    appId=txResponse['application-index']
    print("App id:          ",appId);
    print("App address:     ",e.encode_address(e.checksum(b'appID'+appId.to_bytes(8, 'big'))))

if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <creator mnem> <approval file> <node directory>")
        exit()

    creatorMnemFile=sys.argv[1]
    approvalFile=sys.argv[2]
    directory=sys.argv[3]

    main(creatorMnemFile,approvalFile,directory)
    
    
