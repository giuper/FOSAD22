# *Introduction to blockchain and smart contract design*
## FOSAD 22 ##

## Smart Signatures in Atomic Groups ##

Atomic groups consists of transactions that will either be all accepted
or all rejected, independentely of how the transaction is signed.
In this unit we will use atomic groups of transactions in which 
one of the transactions is signed with a logic signature.

Specifically, we consider the game of NIM of the previous unit in which
the dealer imposes a fee of 1 Algo for each move. This is implemented
by requiring that move implemented by an application call transaction is
in an atomic group with a 1 Algo transaction to the dealer.

### Constructing the atomic group ###
Python program [03-makeMove.py](03-makeMove.py) constructs and submit
the group of transaction. The following fragment does most of the work.

```python
    mtxn=ApplicationNoOpTxn(Addr,params,index,appArgs)
    ptxn=transaction.PaymentTxn(sender=Pk,sp=params,receiver=Dealer,amt=1_000_000)
    gid=transaction.calculate_group_id([ptxn,mtxn])

    ptxn.group=gid
    sptxn=ptxn.sign(SK)

    mtxn.group=gid
    smtxn=mtxn.sign(SK)
```


### The approval program ###
The approval program is similar to the one used in the previous unit
with the added check that the application is called as part
of a group of two transactions of which the first transaction
is a payment transaction to the dealer of at least 1 Algo.

```python
                    And(Global.group_size()==Int(2),
                        Gtxn[0].type_enum()==TxnType.Payment,
                        Gtxn[0].receiver()==Dealer,
                        Gtxn[0].amount()>=Int(1_000_000),
```
