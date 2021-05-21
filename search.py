#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Use the indexer to search for transactions on chain."""

__author__ = "Adriano Di Luzio <adriano@algorand.com>"


import json
import base64
import msgpack

from config import account_mnemonic
from connect import indexer_client
from account import Account


def search(sender):
    response = indexer_client.search_transactions_by_address(address=sender.address)

    print(json.dumps(response, indent=2, sort_keys=True))

    txns = response["transactions"]
    last_txn = txns[0]  # Txs are sorted from most to least recent.
    note = last_txn["note"]

    print()
    print(f"✍️  Most recent note:\n{msgpack.unpackb(base64.b64decode(note))}")


if __name__ == "__main__":
    sender = Account.from_mnemonic(account_mnemonic)
    search(sender)
