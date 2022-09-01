import sys
from algosdk.v2client import algod
#from algosdk import account, mnemonic
#from algosdk.future import transaction 
from algosdk.future.transaction import AssetTransferTxn, write_to_file
from utilities import wait_for_confirmation, getClient, getSKAddr

def transfer(directory,senderMNEMFile,receiverADDRFile,assetID):
    
    algodClient=getClient(directory)
    params=algodClient.suggested_params()
    
    senderSK,senderAddr=getSKAddr(senderMNEMFile)

    with open(receiverADDRFile,'r') as f:
        receiverAddr=f.read()
    
    txn=AssetTransferTxn(sender=senderAddr,sp=params,
                receiver=receiverAddr,amt=10,index=assetID)
    write_to_file([txn],"assetTrans.utxn")
    
    stxn=txn.sign(senderSK)
    write_to_file([stxn],"assetTrans.stxn")

    txid=algodClient.send_transaction(stxn)
    print("TX Id: ",txid)

    wait_for_confirmation(algodClient,txid,4)
    exit()


if __name__=="__main__":
    if (len(sys.argv)!=5):
        print("Usage: python3",sys.argv[0],"<sender MNEM file> <receiver ADDR file> <assetID> <NodeDir>")
        exit()
    senderMNEMFile=sys.argv[1]
    receiverADDRFile=sys.argv[2]
    assetID=int(sys.argv[3])
    directory=sys.argv[4]

    transfer(directory,senderMNEMFile,receiverADDRFile,assetID)
