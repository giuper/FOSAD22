import sys
#from algosdk.v2client import algod
#from algosdk import account, mnemonic
#from algosdk.future import transaction 
from algosdk.future.transaction import AssetTransferTxn, write_to_file
from utilities import wait_for_confirmation, getClient, getSKAddr

def optin(directory,holderMNEMFile,assetID):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()
    
    holderSK,holderAddr=getSKAddr(holderMNEMFile)

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
    write_to_file([txn],"assetOPTin.utxn")

    stxn=txn.sign(holderSK)
    write_to_file([stxn],"assetOPTin.stxn")

    txid=algodClient.send_transaction(stxn)
    print("TX Id: ",txid)
    wait_for_confirmation(algodClient,txid,4)


if __name__=="__main__":
    if (len(sys.argv)!=4):
        print("Usage: python",sys.argv[0],"<holder MNEM file> <assetID> <NodeDir>")
        exit()

    holderMNEMFile=sys.argv[1]
    assetID=int(sys.argv[2])
    directory=sys.argv[3]
    
    optin(directory,holderMNEMFile,assetID)

