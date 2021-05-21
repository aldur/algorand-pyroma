#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create an Algorand account.
"""

__author__ = "Adriano Di Luzio <adriano@algorand.com>"

import dataclasses

# pip install py-algorand-sdk
import algosdk
from algosdk import mnemonic


@dataclasses.dataclass
class Account:
    address: str
    private_key: str

    def mnemonic(self) -> str:
        return mnemonic.from_private_key(self.private_key)

    @classmethod
    def create_account(cls):
        private_key, address = algosdk.account.generate_account()
        return cls(private_key=private_key, address=address)

    @classmethod
    def from_mnemonic(cls, mnemonic_string):
        private_key, address = (
            mnemonic.to_private_key(mnemonic_string),
            mnemonic.to_public_key(mnemonic_string),
        )
        return cls(private_key=private_key, address=address)

    def __str__(self):
        return (
            f"Address: {first_account.address}\n"
            f"Mnemonic: {first_account.mnemonic()}"
        )


if __name__ == "__main__":
    first_account = Account.create_account()
    print(first_account)
