import sys
from algosdk.future.transaction import Multisig

def createMultiSig(accounts,outputFile):
    version=1   #multisig version
    threshold=2 #how many signatures are necessary
    msig=Multisig(version,threshold,accounts)
    maddr=msig.address()
    print(f'{"Multisig Address:":20s}{maddr:s}')
    print("Consisting of accounts: ")
    for addr in accounts:
        print(f'{"":20s}{addr:s}')

    with open(outputFile,'w') as f:
        f.write(maddr)

if __name__=='__main__':
    if len(sys.argv)!=5:
        print("usage: python",sys.argv[0],"<file P1 addr> <file P2 addr> <file P3 addr> <file Multi addr>")
        exit()
    accounts=[]
    for filename in sys.argv[1:4]:
        with open(filename,'r') as f:
            account=f.read()
        accounts.append(account)
    outputFile=sys.argv[4]
    createMultiSig(accounts,outputFile)
    print("\nPlease go to: https://bank.testnet.algorand.network/ to fund multisig account.")
