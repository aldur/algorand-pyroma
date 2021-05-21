#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A simple, stateless smart contract."""

__author__ = "Adriano Di Luzio <adriano@algorand.com>"


import base64

# pip install py-algorand-sdk
from algosdk.future import transaction
from algosdk.future.transaction import PaymentTxn

# pip install pyteal
from pyteal import (
    And,
    Assert,
    Bytes,
    Global,
    Int,
    Mode,
    Return,
    Seq,
    Txn,
    compileTeal,
)

from account import Account
from connect import algod_client
from config import account_mnemonic
from tx import wait_for_confirmation

TEAL_VERSION = 3
FEE = 1000  # microalgos


def escrow_account(note):
    precondition = And(
        Global.group_size() == Int(1),
        Txn.note() == Bytes(note),

        # Safety checks
        Txn.rekey_to() == Global.zero_address(),
        Txn.close_remainder_to() == Global.zero_address(),
        Txn.fee() <= Int(FEE),
    )

    return Seq([
        Assert(precondition),
        Return(Int(1))
    ])


def compile_stateless(escrow):
    return compileTeal(escrow, Mode.Signature, version=TEAL_VERSION)


def stateless_to_lsig(note):
    escrow = escrow_account(note)
    teal_escrow = compile_stateless(escrow)

    # Write the teal program on disk for inspectability 🧐
    with open('escrow.teal', 'w') as f:
        f.write(teal_escrow)

    compiled = algod_client.compile(teal_escrow)

    program = base64.decodebytes(compiled["result"].encode())
    lsig = transaction.LogicSig(program)

    return Account(address=lsig.address(), private_key=None), lsig


def escrow_pay(sender, lsig, receiver, note, client):
    params = client.suggested_params()
    params.flat_fee = True
    params.fee = FEE  # microalgos

    amount = int(10 ** 6)  # microalgos
    unsigned_txn = PaymentTxn(
        sender.address,
        params,
        receiver.address,
        amount,
        close_remainder_to=None,
        note=note,
    )

    signed_txn = transaction.LogicSigTransaction(unsigned_txn, lsig)
    client.send_transactions([signed_txn])

    tx_id = signed_txn.transaction.get_txid()
    return wait_for_confirmation(client, tx_id)


def main():
    note = "pyroma"

    escrow_account, lsig = stateless_to_lsig(note)
    print(f"LogicSig account address: {escrow_account.address}")
    input("Please take a moment and fund that account ⛲... Press Enter to continue")

    receiver = Account.from_mnemonic(account_mnemonic)
    escrow_pay(escrow_account, lsig, receiver, note, algod_client)


if __name__ == "__main__":
    main()
