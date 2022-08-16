# *Introduction to blockchain and smart contract design*
## FOSAD 22 ##

## Logic (or Smart) Signatures ##

A transaction can be logically signed. That is the sender of the transaction is an 
address associated with a TEAL program and the transaction specifies arguments
such that if the program is 
run with the arguments provided, then it terminates with success.
A TEAL program is considered to have terminated with success if the stack contains
exactly one element and that element is *1*.

Each TEAL program has an address that is the hash of its bytecode.

We next discuss two simple logical signatures.


### FOURTYTWO ###

[fourtytwo.teal](./fourtytwo.teal) is a simple TEAL program that
outputs *1* if and only if 

1. the first argument is 42 

```
    byte "42"   //push string "42" onto the stack
    arg 0       //push the first argument onto the stack
    ==          //pop two elements from the stack and push 1 iff they are equal
```

2. the closer and the receiver of the transaction are the same 
```
    txn CloseRemainderTo  //push the address of the closer onto the stack
    txn Receiver          //push the address of the receiver onto the stack
    ==                    //pop two element of the stack and push 1 iff they are equal
```

The last line of the TEAL program consists of instructions ```&&``` that pops two elements from the stack 
(the output of the first two equality checks) and pushes *1* if and only if they are both *1*

Script [00compile.sh](00compile.sh) computes the address of TEAL program  ```fortytwo.teal```.

Python program [42SmartSig.py](./42SmartSig.py) prepares and submits a transaction
logically signed by providing an argument that satisfies TEAL program  ```fortytwo.teal```.
The sender of the transaction will be the address of the TEAL program and the receiver is specified
on the command line.

To create the transaction we need to compute the address of the sender that is obtained
by compiling the TEAL program

```python
    # Read TEAL program
    with open(TEALprogram, 'r') as f:
        data=f.read()
    
    # Compile TEAL program
    response=algodClient.compile(data)
    sender=response['hash']
```

The transaction is then constructed as any other transaction by calling

```python
    txn = transaction.PaymentTxn(sender,params,receiver,amount,closeremainderto)
```

The logic signature of the transaction is then computed as follows

```python

    programstr=response['result']
    t=programstr.encode()
    program=base64.decodebytes(t)

    # Adding arguments
    arg_str="42"
    arg1=arg_str.encode()
    
    #The logic signature is program + arguments
    lsig=transaction.LogicSig(program, args=[arg1])
    #The signed transaction is txn + logic signature
    lstx=transaction.LogicSigTransaction(txn,lsig)


```


### Passphrase ###

[passphrase.teal](./passphrase.teal) is a simple TEAL program that terminates with success 
if and only the following conditions are 

