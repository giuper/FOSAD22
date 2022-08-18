import sys
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future import transaction 
from algosdk.future.transaction import AssetTransferTxn
from utilities import wait_for_confirmation, getClient

def transfer(directory,senderMNEMFile,receiverADDRFile,assetID):
    
    algodClient=getClient(directory)
    params=algodClient.suggested_params()
    
    with open(senderMNEMFile,'r') as f:
        senderMnemo=f.read()
    senderSK=mnemonic.to_private_key(senderMnemo)
    senderAddr=mnemonic.to_public_key(senderMnemo)

    
    with open(receiverADDRFile,'r') as f:
        receiverAddr=f.read()
    
    txn=AssetTransferTxn(sender=senderAddr,sp=params,
                receiver=receiverAddr,amt=10,index=assetID)
    transaction.write_to_file([txn],"assetTrans.utxn")
    
    stxn=txn.sign(senderSK)
    transaction.write_to_file([stxn],"assetTrans.stxn")

    txid=algodClient.send_transaction(stxn)
    print("TX Id: ",txid)

    wait_for_confirmation(algodClient,txid,4)
    exit()


if __name__=="__main__":
    if (len(sys.argv)!=5):
        print("Usage: python3 "+sys.argv[0]+" <NodeDir> <sender MNEM file> <receiver ADDR file> <assetID>")
        exit()
    directory=sys.argv[1]
    senderMNEMFile=sys.argv[2]
    receiverADDRFile=sys.argv[3]
    assetID=int(sys.argv[4])

    transfer(directory,senderMNEMFile,receiverADDRFile,assetID)
