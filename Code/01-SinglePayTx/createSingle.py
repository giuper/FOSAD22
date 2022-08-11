import sys
from algosdk import account, mnemonic

if (len(sys.argv)!=2):
    print("Usage: "+sys.argv[0]+" <account name>")
    exit()

accountName=sys.argv[1]
addrFile=accountName+".addr"
mnemFile=accountName+".mnem"

privateKey,address=account.generate_account()
mnemonic=mnemonic.from_private_key(privateKey)
with open(addrFile,'w') as f:
    f.write(address)
with open(mnemFile,'w') as f:
    f.write(mnemonic)

print(f'{"Account address:":20s}{address}')
print(f'{"File with address:":20s}{addrFile}')
print(f'{"File with mnem:":20s}{mnemFile}')
print(f'{"Account passphrase:":20s}{mnemonic}')
print("Please go to: https://bank.testnet.algorand.network/ to fund account.")



