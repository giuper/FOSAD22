import sys
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future import transaction 
from algosdk.future.transaction import AssetTransferTxn
import algosdk.encoding as e
from utilities import wait_for_confirmation, getClient

def transfer(directory,senderMNEMFile,appId):
    
    algodClient=getClient(directory)
    params=algodClient.suggested_params()
    
    with open(senderMNEMFile,'r') as f:
        senderMnemo=f.read()
    senderSK=mnemonic.to_private_key(senderMnemo)
    senderAddr=mnemonic.to_public_key(senderMnemo)

    appAddr=e.encode_address(e.checksum(b'appID'+appId.to_bytes(8, 'big')))
    accountInfo=algodClient.account_info(appAddr)
    print("App id:   ",appId)
    print("App addr: ",appAddr)
    assetId=None
    for asset in accountInfo['created-assets']:
        if asset['params']['name']=="FosadDAO-VotingRight3":
            assetId=asset['index']
            break
    if assetId==None:
        print("Could not find asset")
    print("Asset id: ",assetId)
    txn=AssetTransferTxn(sender=senderAddr,sp=params,
                receiver=appAddr,amt=1,index=assetId)
    stxn=txn.sign(senderSK)

    txid=algodClient.send_transaction(stxn)
    print("TX Id: ",txid)

    wait_for_confirmation(algodClient,txid,4)
    exit()


if __name__=="__main__":
    if (len(sys.argv)!=4):
        print("Usage: python3 "+sys.argv[0],"<sender MNEM file> <appId> <NodeDir>")
        exit()
    senderMNEMFile=sys.argv[1]
    appId=int(sys.argv[2])
    directory=sys.argv[3]

    transfer(directory,senderMNEMFile,appId)
