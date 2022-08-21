from pyteal import *

rowVal=ScratchVar(TealType.bytes)
rowIdx=ScratchVar(TealType.uint64)
rowacc=ScratchVar(TealType.uint64)

colIdx=ScratchVar(TealType.uint64)
colacc=ScratchVar(TealType.uint64)

sqacc=ScratchVar(TealType.uint64)
sqq=ScratchVar(TealType.uint64)

s=ScratchVar(TealType.bytes)
sint=ScratchVar(TealType.uint64)
i=ScratchVar(TealType.uint64)
j=ScratchVar(TealType.uint64)


def checkRowandCols():

    program=Seq([
             For(rowIdx.store(Int(0)),rowIdx.load()<Int(9),rowIdx.store(rowIdx.load()+Int(1))).Do(
                Seq([
                     rowVal.store(Arg(rowIdx.load())),
                     rowacc.store(Int(0)),
                     colacc.store(Int(0)),
                     For(colIdx.store(Int(0)),colIdx.load()<Int(9),colIdx.store(colIdx.load()+Int(1))).Do(
                        Seq(
                            [s.store(Substring(rowVal.load(),colIdx.load(),colIdx.load()+Int(1))),
                             sint.store(Minus(Btoi(s.load()),Int(48))),
                             rowacc.store(SetBit(rowacc.load(),sint.load(),Int(1))),

                             s.store(Substring(Arg(colIdx.load()),rowIdx.load(),rowIdx.load()+Int(1))),
                             sint.store(Minus(Btoi(s.load()),Int(48))),
                             colacc.store(SetBit(colacc.load(),sint.load(),Int(1))),
                            ]
                            )
                    ),
                    If(rowacc.load()!=Int(1022),Reject()),
                    If(colacc.load()!=Int(1022),Reject()),
                    ]
                )
            
            ),
            Approve(),
        ])
    return program


def checkSquares():

    program=Seq([
    For(sqq.store(Int(0)),sqq.load()<Int(9),sqq.store(sqq.load()+Int(1))).Do(
        Seq([
        rowIdx.store(Mul(Div(sqq.load(),Int(3)),Int(3))),
        colIdx.store(Mul(Mod(sqq.load(),Int(3)),Int(3))),
        sqacc.store(Int(0)),
        For(i.store(Int(0)),i.load()<Int(3),i.store(i.load()+Int(1))).Do(
          Seq([
            rowVal.store(Arg(rowIdx.load()+i.load())),
            For(j.store(Int(0)),j.load()<Int(3),j.store(j.load()+Int(1))).Do(
              Seq([
                s.store(Substring(rowVal.load(),colIdx.load()+j.load(),colIdx.load()+j.load()+Int(1))),
                sint.store(Minus(Btoi(s.load()),Int(48))),
                sqacc.store(SetBit(sqacc.load(),sint.load(),Int(1))),
              ]),
            ),
          ]),
        ),
        If(sqacc.load()!=Int(1022),Reject()),
      ]),
    ),
        ])

    return program

    
    

def blockedCell(bc):
    row,col,val=bc
    program=Seq([
                rowVal.store(Arg(Int(row))),
                colIdx.store(Int(col)),
                s.store(Substring(rowVal.load(),colIdx.load(),colIdx.load()+Int(1))),
                sint.store(Minus(Btoi(s.load()),Int(48))),
                If(sint.load()!=Int(val),Reject())
                ])
    return program
    

def sigProg(listBC):
    conds=[]
    for bc in listBC:
        conds.append(blockedCell(bc))
    conds.append(checkSquares())
    conds.append(checkRowandCols())
    program=Seq(conds)
    return compileTeal(program, Mode.Signature, version=5)

def main():
##Solution
##   827154396
##   965327148
##   341689752
##   593468271
##   472513689
##   618972435
##   786235914
##   154796823
##   239841567"

    program=sigProg([[0,1,2],[1,0,9],[1,1,6],[8,8,7]])
    with open("sudoku.teal","w") as f:
        f.write(program)

if __name__=='__main__':
    main()

