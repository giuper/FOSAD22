import sys
from pyteal import *
import algosdk.encoding as e

t=ScratchVar(TealType.uint64)
arg=ScratchVar(TealType.uint64)
cmd=ScratchVar(TealType.bytes)
pp=ScratchVar(TealType.uint64)

def handle_start():
    h_start=If(And(Global.group_size()==Int(2),
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
                                App.globalPut(Bytes("fsdName"),InnerTxn.created_asset_id()),
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
    return h_start

def handle_priceTok(prefix):
    return Seq([
        If(Or(
           App.globalGet(Bytes(prefix+"pprice"))==Int(0),
           Btoi(Gtxn[1].application_args[1])!=App.globalGet(Bytes(prefix+"pprice")),
           Txn.sender()==App.globalGet(Bytes(prefix+"proposer"))
        )).
        Then(Seq([App.globalPut(Bytes(prefix+"pprice"),Btoi(Gtxn[1].application_args[1])),
                  App.globalPut(Bytes(prefix+"proposer"),Gtxn[1].sender())])).
        Else(Seq([App.globalPut(Bytes(prefix+"pprice"),Int(0)),
                  App.globalPut(Bytes(prefix+"currentPrice"),Btoi(Gtxn[1].application_args[1]))])),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetTransfer,
            TxnField.asset_receiver: Txn.sender(),
            TxnField.asset_amount: Int(1),
            TxnField.xfer_asset: App.globalGet(Bytes("votingTok"))
        }),
        InnerTxnBuilder.Submit(),
        Approve()])

def handle_price(prefix):
    h_price=Seq([
           If(And(Global.group_size()==Int(2),
                  Gtxn[0].type_enum()==TxnType.AssetTransfer,
                  Gtxn[0].asset_receiver()==Global.current_application_address(),
                  Gtxn[0].asset_amount()>=Int(1),
                  Gtxn[0].xfer_asset()==App.globalGet(Bytes("votingTok")),)
           ).Then(handle_priceTok(prefix)).Else(Reject())])
    return h_price

def approval_program(Alice,Bob,Charlie):

    handle_creation=Seq([
                    App.globalPut(Bytes("bpprice"),Int(0)),
                    App.globalPut(Bytes("bproposer"),Alice),
                    App.globalPut(Bytes("bcurrentPrice"),Int(900_000)),
                    App.globalPut(Bytes("spprice"),Int(0)),
                    App.globalPut(Bytes("sproposer"),Alice),
                    App.globalPut(Bytes("scurrentPrice"),Int(1_000_000)),
                    App.globalPut(Bytes("votingTok"),Int(0)),
                    App.globalPut(Bytes("fsdName"),Int(0)),
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

    handle_closeout=Approve()

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
                                        #TxnField.config_asset: Txn.assets[0]
                                        TxnField.config_asset: App.globalGet(Bytes("votingTok"))
                                    }),
                                InnerTxnBuilder.Submit(),
                                InnerTxnBuilder.Begin(),
                                    InnerTxnBuilder.SetFields({
                                        TxnField.type_enum: TxnType.AssetConfig,
                                        #TxnField.config_asset: Txn.assets[1]
                                        TxnField.config_asset: App.globalGet(Bytes("fsdName"))
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

    handle_buy=If(And(Global.group_size()==Int(2),
                  Gtxn[0].type_enum()==TxnType.Payment,
                  Gtxn[0].receiver()==Global.current_application_address(),
                  Gtxn[0].amount()>=Btoi(Gtxn[1].application_args[1])*App.globalGet(Bytes("scurrentPrice")))
            ).Then(Seq([
                     InnerTxnBuilder.Begin(),
                     InnerTxnBuilder.SetFields({
                         TxnField.type_enum: TxnType.AssetTransfer,
                         TxnField.asset_receiver: Txn.sender(),
                         TxnField.asset_amount: Btoi(Gtxn[1].application_args[1]),
                         TxnField.xfer_asset: App.globalGet(Bytes("fsdName"))
                      }),
                      InnerTxnBuilder.Submit(),
                      Approve()
            ])
            ).Else(Reject())

    handle_noop=Seq([
                cmd.store(Txn.application_args[0]),
                Cond([cmd.load()==Bytes("sp"),handle_price("s")],
                     [cmd.load()==Bytes("bp"),handle_price("b")],
                     [cmd.load()==Bytes("b"),handle_buy],
                     [cmd.load()==Bytes("s"),handle_start()],
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
