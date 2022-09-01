# *Introduction to blockchain and smart contract design*
## FOSAD 22 ##

## A Simple DAO (Distributed Autonomous Organization) ##

This contains a simple implementation of a DAO.
The DAO mints and owns a certain number of *Fosad22Token*
that are sold in exchange for Algo's. 
The price is set by the holders of the governor token *FOSAD22-Gov*.
Initially the governors coincide with the three founders of the DAO but they can decide to
exchange the governor token for Algo's or other assets.

We have the following steps:

1. The TEAL code of the DAO is compiled from the the PyTEAL code found in [dao.py](dao.py).
At this stage, the (files containing) the addresses of the three founders are specified on the command line.
    
2. The DAO is created by having one of the founder run [create.py](create.py).
    
3. The DAO is started by running [start.py](start.py) that calls the application by passing *s* (for start) as a parameter.
and creates the assets. For example,the following is the PyTEAL code for creating the *FOSAD22Token* asset.

```python
     InnerTxnBuilder.Begin(),
     InnerTxnBuilder.SetFields({
        TxnField.type_enum: TxnType.AssetConfig,
        TxnField.config_asset_total: Int(1_000_000),
        TxnField.config_asset_decimals: Int(3),
        TxnField.config_asset_name: Bytes(DAOtokenName),
        TxnField.config_asset_unit_name: Bytes("fsd3"),
        TxnField.config_asset_url: Bytes("https://sites.google.com/uniurb.it/fosad/home/fosad-2022"),
        TxnField.config_asset_manager: Global.current_application_address(),
        TxnField.config_asset_reserve: Global.current_application_address(),
        TxnField.config_asset_freeze: Global.current_application_address(),
        TxnField.config_asset_clawback: Global.current_application_address()
      }),
      TxnBuilder.Submit(),
```

The application call is part of group of transaction by which the DAO also receives some initial funding to be used
to pay the fees of the transaction that will be executed.

4. The founder can check in by executing [optinFounder.py](optinFounder.py) and they receive one governor token.
```python
    InnerTxnBuilder.Begin(),
    InnerTxnBuilder.SetFields({
        TxnField.type_enum: TxnType.AssetTransfer,
        TxnField.asset_receiver: Txn.sender(),
        TxnField.asset_amount: Int(1),
        TxnField.xfer_asset: App.globalGet(Bytes("assetIDGov"))
    }),
    InnerTxnBuilder.Submit(),
```

Other users can check in by executing [optinUder.py](optinUder.py)

5. Holder of the governor tokens can propose to set the selling price using program [price.py](price.py).
If the proposed price is backed by another governor it becomes effective.
To make a price proposal the governor must make a group of two transactions: the first transfers the governor token (and thus
shows that the user has the right to make a proposal) and the second makes the actual call to the application.
The DAO then issues another transaction to return the token to the same address that made the application call.

```python
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetTransfer,
            TxnField.asset_receiver: Txn.sender(),
            TxnField.asset_amount: Int(1),
            TxnField.xfer_asset: App.globalGet(Bytes("assetIDGov"))
        }),
        InnerTxnBuilder.Submit(),
```

6. Program [buy.py](buy.py) can be used to buy some tokens at the current selling price.
The application call must come together with a payment transaction.
We first check that the payment is sufficient given the number of tokens requested
(as specified by the second argument of the second transaction of the group) and if the
check is succeful the desired amount is transferred by the inner transaction.

```python
    handle_buy=If(And(Global.group_size()==Int(2),
                  Gtxn[0].type_enum()==TxnType.Payment,
                  Gtxn[0].receiver()==Global.current_application_address(),
                  Gtxn[0].amount()>=Btoi(Gtxn[1].application_args[1])*App.globalGet(Bytes("scurrentPrice")))
            ).Then(Seq([
                     InnerTxnBuilder.Begin(),
                     InnerTxnBuilder.SetFields({
                         TxnField.type_enum: TxnType.AssetTransfer,
                         TxnField.asset_receiver: Txn.sender(),
                         TxnField.asset_amount: Btoi(Gtxn[1].application_args[1]),
                         TxnField.xfer_asset: App.globalGet(Bytes("assetIDToken"))
                      }),
                      InnerTxnBuilder.Submit(),
                      Approve()
            ])
            ).Else(Reject())
```


