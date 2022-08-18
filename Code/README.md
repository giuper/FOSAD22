# *Introduction to blockchain and smart contract design*
## FOSAD 22 ##

## Atomic Swaps ##

### Step by step  ###

Script [atomicSwap.py](./atomicSwap.py) takes as input two account addresses, an asset id,
and the directory of the node.

It constructs an atomic group of two transactions:

1. Account1 sends 10 Algos to Account2
2. Account2 sends 4 instances of the asset to Account1

The group of transactions is atomic in the sense that either both are accepted or neither is.

We have the following transactions (use ```goal clerk inspect``` to see the content of the transactions)

1.  [Unsigned transaction from Account1 to Account2](A1toA2.utnx)
2.  [Unsigned transaction from Account1 to Account2 with GID](A1toA2withGID.utnx)
3.  [Signed transaction from Account1 to Account2 with GID](A1toA2withGID.stnx)

and 
1.  [Unsigned transaction from Account2 to Account1](A2toA1.utnx)
2.  [Unsigned transaction from Account2 to Account1 with GID](A2toA1withGID.utnx)
3.  [Signed transaction from Account2 to Account1 with GID](A2toA1withGID.stnx)
    

