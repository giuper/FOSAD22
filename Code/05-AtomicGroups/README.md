# *Introduction to blockchain and smart contract design*
## FOSAD 22 ##

## Transaction groups ##

Algorand supports *groups* of transactions  that 
are *atomic* in the sense that either all transactions of the group are accepted or none is.

To create a group of transactions from a list of transactions ``ListTX``, first obtain the
group id:

```python
    gid=transaction.calculate_group_id(ListTX)
```
then, add the group id to each transaction

```python
    txn.group=gid
```
and finally sign each transaction. Transaction could be signed by a single key, by multiple keys or
logically. The transactions need not to be signed by the same address but need to be submitted 
together
```python
    txid=algodClient.send_transactions(signedListTX)
```


### Step by step  ###
Next we discuss an example in which we construct and submitted 
an atomic group of two transactions:

1. Account1 sends 10 Algos to Account2
2. Account2 sends 4 instances of an ASA to Account1

Script [atomicSwap.py](./atomicSwap.py) takes as input two account addresses, an asset id,
and the directory of the node.

We have the following transactions (use ```goal clerk inspect``` to see the content of the transactions)

1.  [Unsigned transaction from Account1 to Account2](A1toA2.utnx)
2.  [Unsigned transaction from Account1 to Account2 with GID](A1toA2withGID.utnx)
3.  [Signed transaction from Account1 to Account2 with GID](A1toA2withGID.stnx)

and 
1.  [Unsigned transaction from Account2 to Account1](A2toA1.utnx)
2.  [Unsigned transaction from Account2 to Account1 with GID](A2toA1withGID.utnx)
3.  [Signed transaction from Account2 to Account1 with GID](A2toA1withGID.stnx)
    

