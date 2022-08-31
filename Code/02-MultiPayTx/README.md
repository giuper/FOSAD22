# *Introduction to blockchain and smart contract design*
## FOSAD 22 ##

## Code for multi signatures ##
### All in one ###
1. [createMultiAddr.py](./createMultiAddr.py) creates a 2 out of 3
multi signature address.
It takes three addresses and a filename where the multisignature address is
to be stored.


    The following snippet creates a multisignature address. In order
    to be valid, a transaction needs at least *threshold* signatures
    of the addresses in the list *accounts*

```python
    msig=Multisig(version, threshold, accounts)
    maddr=msig.address()
```
Note that a multisignature address has no secret key.

2. [multiPayTXComplete.py](./multiPayTXComplete.py) 
creates, signs and submits a transaction from a multi signature address. The intermediate transactions are stored for inspection in folder TX.

3. the whole process is executed by [example02.sh](./example02.sh)

### Step by step ### 
The scripts above assume that all signing keys are available to the script. This is not will happen in practice. Rather, the following process is executed

1. The multi signature address is created by executing [createMultiAddr.py](./createMultiAddr.py)

2. The unsigned transaction is created by executing [signMultiPayTX.py](./signMultiPayTX.py). 
    That is, the first party to sign takes the unsigned transaction and adds its signature producing a 
    transaction with one signature. Then the second party adds its signature to the transaction produced by the first party.         This until we have the sufficient number of signatures (in the example, 2 signatures are sufficient).

3. The fully-signed transaction is submitted to the blockchain.
    
