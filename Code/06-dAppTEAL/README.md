# *Introduction to blockchain and smart contract design*
## FOSAD 22 ##

## Distributed Applications (aka dApps) ##

Smart contracts (or *distributed applications* or *dApps*), 
unlike smart signatures, have a state that consists of
*global* variables (i.e., all addresses see the same value) 
and *local* (i.e., per address) variables.

In this unit we design and deploy 
a simple dApp that exemplifies the use of global and local state.
Specifically, the dApp maintains one global counter 
```gcnt1```  that is incremented by 1 at each invocation
and one local counter 
```lcnt``` that is incremented by 7 at each invocation per address.

### Creating a dApp ###

The distributed application is created on the blockchain with a special 
application creation transaction

```python
    utxn=ApplicationCreateTxn(creatorAddr,params,on_complete, \
                                        approvalProgram,clearProgram, \
                                        globalSchema,localSchema)
```
The transactions specifies the address of the creator,
two programs, the ```approvalProgram``` and the ```clearProgram```, 
and the global and local schema.

The ```clearProgram``` is executed when the an address wants to remove
the dApp from its balance account.
In our case the clear program just terminates
with success by pushing *1* onto the stack.

```python
    clearProgramSource=b"""#pragma version 4 int 1 """
    clearProgramResponse=algodClient.compile(clearProgramSource.decode('utf-8'))
    clearProgram=base64.b64decode(clearProgramResponse['result'])
```

The ```approvalProgram``` instead specifies how the application behaves
in the following cases:

1. ```NoOp``` generic execution call of the dApp.
2. ```OptIn``` an address decides to participate to the dApp and its local
storage is enabled.
3. ```DeleteApplication``` when the dApp is removed
4. ```UpdateApplication``` when the dApp TEAL program is updated
5. ```CloseOut``` close the address participation in the dApp without
 removing it from the address balance.

Typically the ```approvalProgram``` is read from a file before being compiled as in the following fragment

```python
    with open(approvalFile,'r') as f:
        approvalProgramSource=f.read()
    approvalProgramResponse=algodClient.compile(approvalProgramSource)
    approvalProgram=base64.b64decode(approvalProgramResponse['result'])
```

The ```globalScheme``` specifies the number of integer and string global
variables. In our case we have the following

```python
    global_ints=2
    global_bytes=1
    globalSchema=StateSchema(global_ints,global_bytes)
```
and similarly for local variables

```python
    local_ints=2
    local_bytes=1
    localSchema=StateSchema(local_ints,local_bytes)
```

Python program [createApp.py](createApp.py) creates a dApp. 
It takes three command line arguments: 
the filename containing the mnemonic of the creator account,
the filename containing the TEAL of the approval program,
and the directory of the node.
Take note of the application index that will be needed for the following steps.

Note that you must use the creator address in the approval program. 

[Here](./TX/create.stxn) is the signed transaction that creates an application.
Use command ```goal clerk inspect create.stxn``` to view its content.

### Opting in a dApp ###
Any address must opt in a dApp before being able to call the dApp.
The opt-in transaction is constructed as follows

```python
    utxn=ApplicationOptInTxn(Addr,params,index)
```
where ```Addr``` is the address opting in, ```params``` are the transaction parameters
and ```index``` is the id of the dApp.

Python program [optinApp.py](optinApp.py) takes three command line arguments: 
the filename containing the mnemonic of the address that wishes to opt in, 
the application index, and the directory of the node.

[Here](./TX/optin.stxn) is the signed transaction to opt in an application.
Use command ```goal clerk inspect optin.stxn``` to view its content.

### Calling a dApp ###
The transaction to call an application is constructed as follows

```python
    utxn=ApplicationNoOpTxn(Addr,params,index)
```
where ```Addr``` is the address calling the app, 
```params``` are the transaction parameters
and ```index``` is the id of the dApp.

Python program [callApp.py](callApp.py) call a dApp and 
it takes three command line arguments: 
the filename containing the mnemonic of the address that wishes to call
the application, the application index, and the directory of the node.
    
[Here](./TX/noop.stxn) is the signed transaction to invoke an application.
Use command ```goal clerk inspect noop.stxn``` to view its content.

The output shows the current values of the global and local variables and
can be obtained from the ```response``` returned by the transaction once it 
has completed 
(in the fields ```global-state-delta``` and ```local-state-delta```, respectively).
Note that only variables whose values have changed are reported 
(whence the ```delta```).

Alternatively, the local state can be obtained from the field ```apps-local-state``` 
of the ```account_info``` obtained from the node about the address that has called the application.

The global state can also be obtained from the script ```readGlobalValues.py``` that accesses 
    the ```account_info``` of the creator of the application.

### Calling a dApp and passing arguments###

It is possible to pass arguments to a dApp. 
Arguments must be properly encoded as shown below. 
The string variable ```stringVar``` is encoded by the ```encode``` method
and the integer variables ```intVar``` is encoded by the `methos 
```to_bytes```.
How arguments are treated by the TEAL and PyTEAL program is discussed
in the next unit.

```python
    appArgs=[stringVar.encode(),intVar.to_bytes(8,'big')]
    utxn=ApplicationNoOpTxn(Addr,params,index,appArgs)
```


### Deleting the application ###

The transaction that clears an application from an address balance is 
```python
    utxn=ApplicationDeleteTxn(Addr,params,index)
```
Python program [deleteApp.py](deleteApp.py) can be used to delete an application

### Clearing a dApp ###

The transaction that clears an application from an address balance is 
```python
    utxn=ApplicationClearStateTxn(Addr,params,index)
```
where ```Addr``` is the address calling the app, 
```params``` are the transaction parameters
and ```index``` is the id of the dApp.


### The TEAL approval file ###

The [approval file](01-class.teal) handles the 5 possible operations.
The operation to be performed can be read by the TEAL program 
by executing ```txn OnCompletion``` and checking the
value obtained with the codes associated to the operations.

The generic execution call identified with code ```NoOp```
is performed by the code starting with label ```handle_noop```


```
handle_noop:
// Handle NoOp
// Check for creator
addr AAI56Y7PPE3ZBTEG3GUEOUKNSC2J3UNQCGRYWNNX5EI22M4RH4AHPH5GDU
txn Sender
==
bnz handle_optin
//

// read global state
byte "gcnt1"
dup
app_global_get

// increment the value by 1
int 1
+

// store to scratch space
dup
store 0

// update global state
app_global_put

// read local state for sender
int 0
byte "lcnt"
app_local_get

// increment the value
int 7
+
store 1

// update local state for sender
int 0
byte "lcnt"
load 1
app_local_put

// load return value as approval
load 0
return
```


For all other operations, the TEAL program just approves the operation without
performing any action.
    
### Passing arguments to a dApp ###

Creation and opting in are the same.
To pass an argument to the dApp, we pass an extra argument to the call to
execute the dApp. The following fragment passes one argument, the python variable
```incr``` after encoding it as a byte sequence.

```python
    appArgs=[incr.to_bytes(8,'big')]
    utxn=ApplicationNoOpTxn(Addr,params,index,appArgs)
```
[This](callIntArgApp.py) python program 
takes four command line arguments: 
the filename containing the mnemonic of the address that wishes to execute the application,
the application index, the increment and the directory of the node.

### Reading Arguments from TEAL ###

We modify the teal program so that the local value is incremented by a user provided 
integer (and not by 1 as before). [Here](02-class.teal) is the revised source and
following is the relevant snippet of code.

```
// read local state for sender and sum the argument to it
int 0
byte "lcnt"
app_local_get
txn ApplicationArgs 0
btoi
+
store 3
```


