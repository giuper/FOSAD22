import sys
import base64
from algosdk import account
from algosdk.v2client import algod
from utilities import wait_for_confirmation, getClient


def check(AddrFile,index,directory):

    algodClient=getClient(directory)

    f=open(AddrFile,'r')
    Addr=f.read()
    f.close()

    print(f"Reading the global values of instance {index} of `Nim on Algorand'")
    results=algodClient.account_info(Addr)
    appsCreated=results['created-apps']

    status={}

    for app in appsCreated :
        if app['id']==index :
            #print(f"global_state for app_id {index}: ", app['params']['global-state'])
            for kk in app['params']['global-state']:
                key=kk['key']
                key=base64.b64decode(key)
                key=key.decode('utf-8')
                #print(key,kk['value'])
                status[key]=kk['value']['uint']
    if status['heap']==0:
        if status['turn']==0:
            print("Bob won")
        else:
            print("Alice won")
    else:
        if status['turn']==0:
            print(f"Next: Alice")
        else:
            print(f"Next: Bob")
        print(f"Heap: {status['heap']:3d}")
        print(f"Max:  {status['max']:3d}")


if __name__=='__main__':
    if len(sys.argv)!=4:
        print("usage: python3 "+sys.argv[0]+" <addr> <app index> <node directory>")
        exit()

    AddrFile=sys.argv[1]
    index=int(sys.argv[2])
    directory=sys.argv[3]

    check(AddrFile,index,directory)
    
