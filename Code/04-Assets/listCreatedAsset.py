import sys
from algosdk import account
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
        print("Usage: python",sys.argv[0],"<creator ADDR file> <NodeDir> ")
        exit()

    creatorADDRFile=sys.argv[1]
    directory=sys.argv[2]
    listAssets(directory,creatorADDRFile)

