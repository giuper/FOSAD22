import sys
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future import transaction 
from algosdk.future.transaction import AssetTransferTxn
from utilities import wait_for_confirmation, getClient

def optin(directory,holderMNEMFile,assetID):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()
    
    with open(holderMNEMFile,'r') as f:
        holderMnemo=f.read()
    holderSK=mnemonic.to_private_key(holderMnemo)
    holderAddr=mnemonic.to_public_key(holderMnemo)

    #check if account has already opted in
    accountInfo=algodClient.account_info(holderAddr)
    holding=False
    for asset in accountInfo['assets']:
        if (asset['asset-id']==assetID):
            holding = True
            break

    if holding:
        return

    txn=AssetTransferTxn(sender=holderAddr,
            sp=params,receiver=holderAddr,amt=0,index=assetID)
    transaction.write_to_file([txn],"assetOPTin.utxn")

    stxn=txn.sign(holderSK)
    transaction.write_to_file([stxn],"assetOPTin.stxn")

    txid=algodClient.send_transaction(stxn)
    print("TX Id: ",txid)
    wait_for_confirmation(algodClient,txid,4)


if __name__=="__main__":
    if (len(sys.argv)!=4):
        print("Usage: python3 "+sys.argv[0]+" <NodeDir> <holder MNEM file> <assetID>")
        exit()

    directory=sys.argv[1]
    holderMNEMFile=sys.argv[2]
    assetID=int(sys.argv[3])
    
    optin(directory,holderMNEMFile,assetID)

