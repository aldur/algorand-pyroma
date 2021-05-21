#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Connect to `algod` and to an `indexer`."""

__author__ = "Adriano Di Luzio <adriano@algorand.com>"

# pip install py-algorand-sdk
from algosdk.v2client import algod, indexer


# ALGOD_ADDRESS = "http://localhost:4001"  # Default port
# ALGOD_TOKEN = "a" * 64
# INDEXER_ADDRESS = "http://localhost:8980"  # Default port
# INDEXER_TOKEN = "a" * 64

ALGOD_ADDRESS = "https://testnet-algorand.api.purestake.io/ps2"
ALGOD_TOKEN = "mpgzbZLnJO77lSSIgfmC6WBF0H6goHg7KXw6noo6"
INDEXER_ADDRESS = "https://testnet-algorand.api.purestake.io/idx2"
INDEXER_TOKEN = ALGOD_TOKEN
# ...hold your horses, I have registered a temporary account for this demo _only_ 🐎

# Some services (e.g. Purestake) require additional headers.
ALGOD_HEADERS = {
    "X-API-Key": ALGOD_TOKEN,
}
INDEXER_HEADERS = {
    "X-API-Key": INDEXER_TOKEN,
}

algod_client = algod.AlgodClient(
    algod_token=ALGOD_TOKEN, algod_address=ALGOD_ADDRESS, headers=ALGOD_HEADERS
)
indexer_client = indexer.IndexerClient(
    indexer_token=INDEXER_TOKEN,
    indexer_address=INDEXER_ADDRESS,
    headers=INDEXER_HEADERS,
)

if __name__ == "__main__":
    print(algod_client.health())  # Returns None if the node is running, ¯\_(ツ)_/¯
    print(indexer_client.health())

    __import__('pprint').pprint(algod_client.status())
