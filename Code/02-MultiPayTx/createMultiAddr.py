import sys
from algosdk import mnemonic
from algosdk.future.transaction import Multisig

if __name__=='__main__':
    if len(sys.argv)!=5:
        print("usage: "+sys.argv[0]+" <file P1 addr> <file P2 addr> <file P3 addr> <file Multi addr>")
        exit()

#read the account addresses
    accounts=[]
    for filename in sys.argv[1:4]:
        with open(filename,'r') as f:
            account=f.read()
        accounts.append(account)

# create a multisig account
    version=1  # multisig version
    threshold=2  # how many signatures are necessary
    msig=Multisig(version, threshold, accounts)
    maddr=msig.address()
    print("Multisig Address:",maddr)
    maddrFile=sys.argv[4]
    with open(maddrFile,'w') as f:
        f.write(maddr)

print("Please go to: https://bank.testnet.algorand.network/ to fund multisig account.")
