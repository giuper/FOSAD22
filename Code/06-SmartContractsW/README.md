# *Introduction to blockchain and smart contract design*
## FOSAD 22 ##

## Distributed Applications (aka dApps) ##

Smart contracts (or *distributed applications* or *dApps*), 
unlike smart signatures, have a state that consists of
*global* variables (i.e., all addresses see the same value) 
and *local* (i.e., per address) variable.

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

The ```globalScheme``` specifies the number of the integer and string gloabl
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


### Step by step (no arguments) ###

1. Create the approval file [01-class.teal](01-class.teal)

The actual execution is performed by the code starting with label ```handle_noop``

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




2. Run [optinApp.py](optinApp.py) to allow addresses to opt in the application.
    It takes three command line arguments: the filename containing the mnemonic of the address
    that wishes to opt in, the application index, and the directory of the node.

    [Here](./TX/optin.stxn) is the signed transaction to opt in an application.
    Use command ```goal clerk inspect optin.stxn``` to view its content.
    
3. Run [callApp.py](callApp.py) to allow addresses to execute the application.
    It takes three command line arguments: the filename containing the mnemonic of the address
    that wishes to opt in, the application index, and the directory of the node.
    
    [Here](./TX/noop.stxn) is the signed transaction to invoke an application.
    Use command ```goal clerk inspect noop.stxn``` to view its content.

    The output shows the current values of the counters.
    The global and local counter can be obtained from the ```response``` returned by the transaction once it 
    has completed (in the fields ```global-state-delta``` and ```local-state-delta```, respectively).
    Note that only variables whose values have changed are reported (whence the ```delta```).

    Alternatively, the local state can be obtained from the field ```apps-local-state``` of the 
    ```account_info``` obtained from the node about the address that has called the application.

    The global state can also be obtained from the script ```readGlobalValues.py``` that accesses 
    the ```account_info``` of the creator of the application.

### Step by step (with arguments) ###

1.  We modify the teal program so that the local value is incremented by a user provided 
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

2. Opting is the same as before.

3. Run [callIntArgApp.py](callIntArgApp.py) to allow addresses to execute the application
    and pass the parameter.

    It takes four command line arguments: the filename containing the mnemonic of the address
    that wishes to opt in, the application index, the increment and the directory of the node.
    

### Deleting the application ###

1. Run [deleteApp.py](deleteApp.py) to delete the application