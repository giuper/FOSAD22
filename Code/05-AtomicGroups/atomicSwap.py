import sys
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future import transaction
from algosdk.future.transaction import AssetTransferTxn
from utilities import wait_for_confirmation, getClient
from utilityAsset import print_asset_holding


def swap(account1,account2,assetId,directory):

    algodClient=getClient(directory)
    params=algodClient.suggested_params()
    with open(account1,'r') as f:
        mnemo1=f.read()
        pk1=mnemonic.to_public_key(mnemo1)
        sk1=mnemonic.to_private_key(mnemo1)

    with open(account2,'r') as f:
        mnemo2=f.read()
        pk2=mnemonic.to_public_key(mnemo2)
        sk2=mnemonic.to_private_key(mnemo2)

##account2 pays account1 1Algo 
    txn0=transaction.PaymentTxn(
        sender=pk2,sp=params,receiver=pk1,amt=1_000_000)
    transaction.write_to_file([txn0],"A2toA1.utnx")


##account1 transfers 4 unit of the asset to account2 
    txn1 = transaction.AssetTransferTxn(
        sender=pk1,sp=params,receiver=pk2,amt=4,index=assetId)
    transaction.write_to_file([txn1],"A1toA2.utnx")

##create the group
    gid=transaction.calculate_group_id([txn0, txn1])

#account2 signs the payment transaction txn0
    txn0.group=gid
    transaction.write_to_file([txn0],"A2toA1withGID.utnx")
    stxn0=txn0.sign(sk2)
    transaction.write_to_file([stxn0],"A2toA1withGID.stnx")

#account 1 signs the asset transfer
    txn1.group=gid
    transaction.write_to_file([txn1],"A1toA2withGID.utnx")
    stxn1=txn1.sign(sk1)
    transaction.write_to_file([stxn1],"A1toA2withGID.stnx")

    print("Asset holding before the transaction")
    print("Account 1:      ",pk1)
    print_asset_holding(algodClient,pk1,assetId)
    print()
    print("Account 2:      ",pk2)
    print_asset_holding(algodClient,pk2,assetId)

    signedTL=[stxn0,stxn1]
    txid=algodClient.send_transactions(signedTL)
    print("Transaction id: ",txid)

    wait_for_confirmation(algodClient,txid,4)

    print()
    print("Asset holding after the transaction")
    print("Account 1:      ",pk1)
    print_asset_holding(algodClient,pk1,assetId)
    print()
    print("Account 2:      ",pk2)
    print_asset_holding(algodClient,pk2,assetId)


if __name__=="__main__":
    if (len(sys.argv)!=5):
        print("Usage: "+sys.argv[0]+" <account1> <account2> <assetId> <directory>")
        exit()

    account1=sys.argv[1]
    account2=sys.argv[2]
    assetId=int(sys.argv[3])
    directory=sys.argv[4]
    swap(account1,account2,assetId,directory)
