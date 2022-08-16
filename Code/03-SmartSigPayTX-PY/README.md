# *Introduction to blockchain and smart contract design*
## FOSAD 22 ##

## Logical Signatures ##

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

    3. the last line of the TEAL program consists of ```&&``` that pops two elements from the
    stack and pushes *1* if and only if they are both *1*

