import sys
import base64

from algosdk.future import transaction
from algosdk import mnemonic
from algosdk.v2client import algod
from pyteal import *
from utilities import *

if len(sys.argv)!=3:
    print("Usage: ",sys.argv[0],"<TEAL program file> <nodeDir>")
    exit()

myprogram=sys.argv[1]
directory=sys.argv[2]
algodClient=getClient(directory)

# Read TEAL program
data=open(myprogram, 'r').read()

# Compile TEAL program
response=algodClient.compile(data)
sender=response['hash']
print("Response Hash   = ",sender)

