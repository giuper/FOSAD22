# *Introduction to blockchain and smart contract design*
## FOSAD 22 ##

## Single payer transactions ##

1. Script [createSingle.py](createSingle.py) creates an Algorand address.
    It takes an account name as a command line argument and writes
    the address and the mnemonic and in the ```addr``` and ```mnem``` file,
    respectively.

    The pair of public and private key is generated by invoking

    ```python
        privateKey,publicKey=account.generate_account()
    ```

    The public key is called the *address* of the account.
    The private key is binary and is typically stored in the form of 
    a *mnemonic*, a passphrase consisting of 25 English words.

    The mnemonic is obtained by invoking

    ```python
        mnemonic=mnemonic.from_private_key(privateKey)
    ```

2. Script [payTX.py](payTX.py) creates a payment transaction.
    It takes the (name of the file containing) the mnemonic of the sender,
    the (name of the file containing) the address of the receiver, and
    the directory containing the information of the node to which the
    signed transaction is submitted.

    The transaction is generated, signed and submitted as in the following
    snippet

    ```python
        unsignedTx=PaymentTxn(sAddr,params,rAddr,amount,None,note)
        signedTx=unsignedTx.sign(sKey)
        txid=algodClient.send_transaction(signedTx)
    ```

    The unsigned and signed transactions are found [here](TX/Pay.utx) 
    and [here](TX/Pay.stx). Use the following command to inspect the 
    transactions.

```
        goal clerk inspect
```

