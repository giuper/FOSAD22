import sys
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future import transaction 
from utilities import getClient

def listAssets(directory,creatorADDRFile):

    algodClient=getClient(directory)
    
    with open(creatorADDRFile,'r') as f:
        creatorADDR=f.read()

    print("Assets for address: ",creatorADDR)
    accountInfo=algodClient.account_info(creatorADDR)
    for asset in accountInfo['created-assets']:
        print("Index: ",asset['index'])
        print("\t",asset['params']['name'])
        print("\t","Creator: ",asset['params']['creator'])
        print("\t","Manager: ",asset['params']['manager'])
        print()
    return
    

if __name__=="__main__":
    if (len(sys.argv)!=3):
        print("Usage: python3 "+sys.argv[0]+" <NodeDir> <creator ADDR file>")
        exit()

    directory=sys.argv[1]
    creatorADDRFile=sys.argv[2]
    listAssets(directory,creatorADDRFile)

