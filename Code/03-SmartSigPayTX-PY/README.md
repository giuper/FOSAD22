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


### FORTYTWO ###

[fortytwo.teal](./fortytwo.teal) is a simple TEAL program that
outputs *1* if and only if the following two conditions are met.
For each condition we describe the TEAL fragment that verifies the
condition.

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

### Passphrase ###

[passphrase.teal](./passphrase.teal) is a simple TEAL program that terminates with success 
if and only the following conditions are 

1. The transaction fee is reasonabe

```
    // Check the Fee is reasonable
    // In this case 10,000 microalgos
    txn Fee      //push the transaction fee onto the stack
    int 10000    //push integer 10_000 onto the stack
    <=           //pop two elements from the stack
                 //and push one iff the deeper of the two is smaller than
                 //the other
```

2. The passphrase provided as input is of the right length (73)

```
    // Check the length of the passphrase is correct
    arg 0   //push the first argument onto the the stack
    len     //pop one element from the stack and push back its length
    int 73  //push the integer 73 onto the stack
    ==      //pop two elements from the stack and replace with 1 
            //iff and only they are equal
    &&      //pop two elements from the stack 
            //(at this point the results of the first two checks)
            //and push the AND of the two elements
```

4.  The SHA256 value of the passphrase is the correct one

```
    arg 0    //push the first argument onto the the stack
    sha256   //replace the top of the stack with its SHA256 value
    byte base64 30AT2gOReDBdJmLBO/DgvjC6hIXgACecTpFDcP1bJHU=
            //push the byte string whose base64 encoding is provided
    ==      //pop two elements from the stack and push 1 iff they are equal
            //(at this point the hash of the first argument and the hash provided)
    &&     //pop two elements from the stack 
           //(at this point the result of the first two checks and of the third one)
           //and push the AND of the two elements
```

5. Check the CloseRemainderTo is equal to the receiver

```
    txn CloseRemainderTo  //push the closer of the transaction onto the stack
    txn Receiver //push the receiver of the transaction onto the stack
    ==      //pop two elements from the stack and push 1 iff they are equal
    &&
```

The passphrase is

```
    weather comfort erupt verb pet range endorse exhibit tree brush crane man
```

### Constructing and Signing with a Smart Signature ###

Python program [SmartSig.py](./SmartSig.py) prepares and submits a transaction
logically signed by a specified TEAL program.
The sender of the transaction will be the address of the TEAL program and the receiver is specified on the command line.
It is assumed that the TEAL program takes one single input that i s
passed to ```SmartSig.py``` as a command line argument.

To create the transaction we need to compute the address of the sender that is obtained
by compiling the TEAL program

```python
    # Read TEAL program
    with open(TEALprogram, 'r') as f:
        data=f.read()
    
    # Compile TEAL program
    response=algodClient.compile(data)
    sender=response['hash']           #the address of the TEAL program
```

The transaction is then constructed as any other transaction by calling

```python
    txn = transaction.PaymentTxn(sender,params,receiver,amount,closeremainderto)
```

The logic signature of the transaction is then computed as follows

```python

    programstr=response['result']   #the bytecode
    t=programstr.encode()
    program=base64.decodebytes(t)

    # Adding arguments
    arg_str=sys.argv[3]
    arg1=arg_str.encode()
    
    #The logic signature is program + arguments
    lsig=transaction.LogicSig(program, args=[arg1])
    #The signed transaction is txn + logic signature
    lstx=transaction.LogicSigTransaction(txn,lsig)


```


