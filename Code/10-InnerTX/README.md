# *Introduction to blockchain and smart contract design*
## FOSAD 22 ##

## Inner transactions ##

Furthering our NIM implementation on Algorand, let us consider 
one extra feature. Now that players pay for each move it seems only fair
that they receive something in return.
Let us then modify our NIM so that each player pays a fee to the
application (not to the creator of the application as in the previous
case) when they optin the app and the winning player receives
some Algo at the end of the game from the application. 

Two questions arise:

1. How can the application receive Algo?

    This is very simple as an application is associated to an 
    address that is computed from its index in the following way

```python
    import algosdk.encoding as e
    appAddr=e.encode_address(e.checksum(b'appID'+index.to_bytes(8, 'big')))
```

    So we modify PyTEAL to check that the OptingIn transaction is 
    an a group with a payment transaction to the application

```
   handle_optin=If(And(Global.group_size()==Int(2),
                        Gtxn[0].type_enum()==TxnType.Payment,
                        Gtxn[0].receiver()==Global.current_application_address(),
                        Gtxn[0].amount()>=Int(500_000),
                    )).Then(Approve()).Else(Reject())
```


2. How can the application send out Algo?
    
    We add to the code for ```Noop``` a check for ```heap==0```.
    In this case the application generate an *inner transaction* that
    transfers some Algos to the sender of the application call being
    executed.

```
    If(App.globalGet(Bytes("heap"))==Int(0)).Then(
        Seq([
             InnerTxnBuilder.Begin(),
             InnerTxnBuilder.SetFields({
                TxnField.type_enum: TxnType.Payment,
                TxnField.amount: Int(899_000),
                TxnField.receiver: Txn.sender()
             }),
             InnerTxnBuilder.Submit(),
             Approve()])
     ).Else(Approve())
```
