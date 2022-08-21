# *Introduction to blockchain and smart contract design*
## FOSAD 22 ##

## Smart Signatures with PyTeal ##


In a previous unit we designed and deployed
a simple smart signature by writing the approval program directly in TEAL.
PyTEAL can be used also for smart signature and in this unit we deploy a simple smart
signature that realeses some algo to the first to propose a solution for a given sudoku puzzle.
In other words, we have a TEAL program that takes as input 9 strings of integers from 1 to 9
and terminates with success if and only if the proposed solution is valid for the puzzle specified.

The sudoku verification program is written in PyTEAL and can be found [here](./sudoku.py).
The work is coordinated by the ```sigProg``` function that takes as input the list of blocked cells
with their values.
In the example the list is very minimal
```
    program=sigProg([[0,1,2],[1,0,9],[1,1,6],[8,8,7]])
```
The ```sigProg``` function constructed a a list ```conds``` of conditions and the final program is
obtained by setting ```program=Seq(conds).```
The list ```conds``` is obtained by appending the conditions for each blocked cell  ```bc```,
obtained by ```blockedCell(bc),```
the conditions for the 9 squares given by ```checkSquares``` and the conditions for
rows and columns given by ```checkRowandCols```

The TEAL program is obtained by running ```python sudoku.py``` and then smart signature is invoked
by running [SmartSig.py](SmartSig.py). Do not forget to fund the smart signature. The address of
the smart signature can be computed by running [compile.sh](compile.sh).
