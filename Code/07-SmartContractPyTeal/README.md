# *Introduction to blockchain and smart contract design*
## FOSAD 22 ##

## dApps with PyTeal ##


In the previous unit we designed and deployed
a simple dApp. We wrote the approval program directly in TEAL.
For more complex applications it could be easier to write the approval
program (and the clear program) using PyTEAL,
a python package that produces TEAL code.

We exemplify the use of PyTEAL by constructing
a simple dApp that allows two parties to play a simple version of NIM.
Two players take turn in removing at least one element and at most *max* elements from a heap.
The player unable to move because the heap is empty loses.


### Approval program: type of invocation ###
The following fragment checks which type
of invocation we are handling and produces the appropriate code.  The syntax is self-explanatory
```python
    program = Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )
```

### Approval program: *handle_creation* ###
When the application is being created (and thus its id is still 0),
the TEAL code executed by the application is output by the following fragment.
Specifically, three global variables are initialized: 
*turn* is initialized to 0, 
*heap* is inizialized to 4, and 
*max* is initialiazed to 3.


```python
    handle_creation = Seq([
        App.globalPut(Bytes("turn"), Int(0)),
        App.globalPut(Bytes("heap"), Int(4)),
        App.globalPut(Bytes("max"), Int(3)),
        Return(Int(1))
    ])
```

### Approval program: *handle_noop* ###
The following fragments performs various checks and if they are all passed,
the move is executed. Otherwise, all remains the same.
```python
    handle_noop=If(Seq([arg.store(Btoi(Txn.application_args[0])),
                    And(arg.load()<=App.globalGet(Bytes("max")),
                        arg.load()>Int(0),
                        arg.load()<=App.globalGet(Bytes("heap")),
                        Or(
                            And(Txn.sender()==Alice,App.globalGet(Bytes("turn"))==Int(0)),
                            And(Txn.sender()==Bob,App.globalGet(Bytes("turn"))==Int(1))
                          )
                    )
                ])
    ).Then(
        Seq([
            t.store(App.globalGet(Bytes("heap"))),
            App.globalPut(Bytes("heap"),Minus(t.load(),Btoi(Txn.application_args[0]))),
            t.store(App.globalGet(Bytes("turn"))),
            App.globalPut(Bytes("turn"),Minus(Int(1),t.load())),
            Approve()
           ])
    ).Else(
        Approve()
    )
```
Specifically,
the number of elements to be removed, passed to the application as the first argument, is stored
in a scratch variable ```arg``` after being converted to an integer
```python
       arg.store(Btoi(Txn.application_args[0])),
```
The number of elements to be removed must be
at most the maximum number allowed in one move as specified by the global variable *max*,
at least *1*, and at most the number of elements still in the heap, as specified by
the global variable *heap*

```python
                    And(arg.load()<=App.globalGet(Bytes("max")),
                        arg.load()>Int(0),
                        arg.load()<=App.globalGet(Bytes("heap")),
```

The right player is taking the move. That is, if *turn=0* then Alice is supposed to move
otherwise Bob.

```python
                        Or(
                            And(Txn.sender()==Alice,App.globalGet(Bytes("turn"))==Int(0)),
                            And(Txn.sender()==Bob,App.globalGet(Bytes("turn"))==Int(1))
                          )
```
If the conditions above are satisfied then the move is performed.
That is, ```heap``` is updated to be ```heap-arg``` and
```turn``` is updated to ```1-turn```

```python
            t.store(App.globalGet(Bytes("heap"))),
            App.globalPut(Bytes("heap"),Minus(t.load(),Btoi(Txn.application_args[0]))),
            t.store(App.globalGet(Bytes("turn"))),
            App.globalPut(Bytes("turn"),Minus(Int(1),t.load())),
```

### Outputting the approval program ###
The ```program`` is compiled and then written to a file. The resulting TEAL file can be used
as seen in the previous unit.

```python
        compileTeal(program, Mode.Application, version=5)
```

### Deployment ###
Use the python program of the previous unit to deploy and use the nim application

