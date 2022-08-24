import sys
from pyteal import *

t=ScratchVar(TealType.uint64)
arg=ScratchVar(TealType.uint64)
cmd=ScratchVar(TealType.bytes)
pp=ScratchVar(TealType.uint64)

def approval_program(Alice,Bob,Charlie):

    handle_start=If(And(Global.group_size()==Int(2),
                        Gtxn[0].type_enum()==TxnType.Payment,
                        Gtxn[0].receiver()==Global.current_application_address(),
                        Gtxn[0].amount()>=Int(500_000),
                    )).Then(
                         Seq([
                            InnerTxnBuilder.Begin(),
                            InnerTxnBuilder.SetFields({
                                TxnField.type_enum: TxnType.AssetConfig,
                                TxnField.config_asset_total: Int(1_000_000),
                                TxnField.config_asset_decimals: Int(3),
                                TxnField.config_asset_unit_name: Bytes("fsd3"),
                                TxnField.config_asset_name: Bytes("FosadDAO3"),
                                TxnField.config_asset_url: Bytes("https://fosad22.io"),
                                TxnField.config_asset_manager: Global.current_application_address(),
                                TxnField.config_asset_reserve: Global.current_application_address(),
                                TxnField.config_asset_freeze: Global.current_application_address(),
                                TxnField.config_asset_clawback: Global.current_application_address()
                                }),
                                InnerTxnBuilder.Submit(),
                                App.globalPut(Bytes("fsd"),InnerTxn.created_asset_id()),
                            InnerTxnBuilder.Begin(),
                            InnerTxnBuilder.SetFields({
                                TxnField.type_enum: TxnType.AssetConfig,
                                TxnField.config_asset_total: Int(3),
                                TxnField.config_asset_decimals: Int(0),
                                TxnField.config_asset_unit_name: Bytes("vr3"),
                                TxnField.config_asset_name: Bytes("FosadDAO-VotingRight3"),
                                TxnField.config_asset_url: Bytes("https://fosad22.io"),
                                TxnField.config_asset_manager: Global.current_application_address(),
                                TxnField.config_asset_reserve: Global.current_application_address(),
                                TxnField.config_asset_freeze: Global.current_application_address(),
                                TxnField.config_asset_clawback: Global.current_application_address()
                            }),
                            InnerTxnBuilder.Submit(),
                            App.globalPut(Bytes("votingTok"),InnerTxn.created_asset_id()),
                            Approve()
                        ])).Else(Reject())
 
    handle_price=Seq([
                        If(And(Global.group_size()==Int(2),
                            Gtxn[0].type_enum()==TxnType.AssetTransfer,
                            Gtxn[0].asset_receiver()==Global.current_application_address(),
                            Gtxn[0].asset_amount()>=Int(1),
                            Gtxn[0].xfer_asset()==App.globalGet(Bytes("votingTok")),
                            )).
                    Then(
                        Seq([
                        pp.store(Btoi(Gtxn[1].application_args[1])),
                        App.globalPut(Bytes("price"),pp.load()),
                        InnerTxnBuilder.Begin(),
                        InnerTxnBuilder.SetFields({
                                TxnField.type_enum: TxnType.AssetTransfer,
                                TxnField.asset_receiver: Txn.sender(),
                                TxnField.asset_amount: Int(1),
                                TxnField.xfer_asset: App.globalGet(Bytes("votingTok"))
                        }),
                        InnerTxnBuilder.Submit(),
                        Approve()])).
                    Else(Reject())
                     ])

    handle_creation=Seq([
                    App.globalPut(Bytes("price"),Int(1_000_000)),
                    App.globalPut(Bytes("votingTok"),Int(0)),
                    App.globalPut(Bytes("fsd"),Int(0)),
                    Approve()])

    handle_optin=If(Or(Txn.sender()==Alice,
                       Txn.sender()==Bob,
                       Txn.sender()==Charlie)).Then(
                    Seq([
                            InnerTxnBuilder.Begin(),
                            InnerTxnBuilder.SetFields({
                                TxnField.type_enum: TxnType.AssetTransfer,
                                TxnField.asset_receiver: Txn.sender(),
                                TxnField.asset_amount: Int(1),
                                TxnField.xfer_asset: App.globalGet(Bytes("votingTok"))
                            }),
                            InnerTxnBuilder.Submit(),
                            Approve()
                    ])).Else(Approve())

    handle_closeout=If(Or(
                Txn.sender()==Alice,
                Txn.sender()==Bob,
                Txn.sender()==Charlie)).Then(Approve()).Else(Reject())

    handle_updateapp=If(Or(Txn.sender()==Alice,
                           Txn.sender()==Bob,
                           Txn.sender()==Charlie)).Then(Approve()).Else(Reject())

    handle_deleteapp=If(Or(Txn.sender()==Alice,
                           Txn.sender()==Bob,
                           Txn.sender()==Charlie)).Then(
                             Seq([
                                InnerTxnBuilder.Begin(),
                                    InnerTxnBuilder.SetFields({
                                        TxnField.type_enum: TxnType.AssetConfig,
                                        TxnField.config_asset: Txn.assets[0]
                                    }),
                                InnerTxnBuilder.Submit(),
                                InnerTxnBuilder.Begin(),
                                    InnerTxnBuilder.SetFields({
                                        TxnField.type_enum: TxnType.AssetConfig,
                                        TxnField.config_asset: Txn.assets[1]
                                    }),
                                InnerTxnBuilder.Submit(),
                                InnerTxnBuilder.Begin(),
                                    InnerTxnBuilder.SetFields({
                                        TxnField.type_enum: TxnType.Payment,
                                        TxnField.amount: Int(0),
                                        TxnField.receiver: Charlie,
                                        TxnField.close_remainder_to: Charlie,
                                    }),
                                InnerTxnBuilder.Submit(),
                                Approve()])).Else(Reject())

    handle_noop=Seq([
                cmd.store(Txn.application_args[0]),
                Cond([cmd.load()==Bytes("p"),handle_price],
                     [cmd.load()==Bytes("s"),handle_start],
                ),Approve()]
    )

    program = Cond(
        [Txn.application_id()==Int(0), handle_creation],
        [Txn.on_completion()==OnComplete.OptIn, handle_optin],
        [Txn.on_completion()==OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion()==OnComplete.UpdateApplication, handle_updateapp],
        [Txn.on_completion()==OnComplete.DeleteApplication, handle_deleteapp],
        [Txn.on_completion()==OnComplete.NoOp, handle_noop]
    )

    return compileTeal(program, Mode.Application, version=5)

if __name__=='__main__':
    if len(sys.argv)!=4:
        print("Usage: ",sys.argv[0],"<Alice ADDR file> <Bob ADDR file> <Charlie ADDR file>")
        exit()

    with open(sys.argv[1]) as f:
        aliceA=f.read()
    alice=Addr(aliceA)
    with open(sys.argv[2]) as f:
        bobA=f.read()
    bob=Addr(bobA)
    with open(sys.argv[3]) as f:
        charlieA=f.read()
    charlie=Addr(charlieA)

    program=approval_program(alice,bob,charlie)
    with open("dao.teal","w") as f:
        f.write(program)
