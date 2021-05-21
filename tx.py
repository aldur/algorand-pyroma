#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import msgpack

# pip install py-algorand-sdk
from algosdk.future.transaction import PaymentTxn

from config import account_mnemonic
from connect import algod_client
from account import Account


def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is confirmed before
    proceeding.
    """
    last_round = client.status().get("last-round")
    txinfo = client.pending_transaction_info(txid)

    while not txinfo.get("confirmed-round", -1) > 0:
        print(f"Waiting for transaction {txid} confirmation.")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)

    print(f"Transaction {txid} confirmed in round {txinfo.get('confirmed-round')}.")
    return txid, txinfo


def send_transaction(sender, receiver, client):
    params = client.suggested_params()
    params.flat_fee = True
    params.fee = 1000  # microalgos

    note = msgpack.packb({"eventType": "PyRoma", "greeting": "Hello, you all!"})

    amount = 42  # microalgos
    unsigned_txn = PaymentTxn(
        sender.address,
        params,
        receiver.address,
        amount,
        close_remainder_to=None,
        note=note,
    )

    signed_txn = unsigned_txn.sign(sender.private_key)  # Sign txn
    client.send_transactions([signed_txn])  # Send txn

    tx_id = signed_txn.transaction.get_txid()
    return wait_for_confirmation(client, tx_id)


def main():
    sender = Account.from_mnemonic(account_mnemonic)
    receiver = sender  # This will be a transaction to self ➰

    txid, _ = send_transaction(sender, receiver, algod_client)
    print(f"🌎 Explore it here: https://testnet.algoexplorer.io/tx/{txid}")


if __name__ == "__main__":
    main()
