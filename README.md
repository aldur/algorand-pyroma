# PyRoma <> Algorand

## Introduction to blockchain and Algorand:

- Distributed systems and replicated storage.
- Pure Proof of Stake (and green! 🪴) vs Proof of Work.
  - Verifiable Random Functions (VRFs) and leader election.
- Why Algorand?
  - Blockchain trilemma;
  - scalability;
  - performance.

## Developer workspace:

- How to interact with the Algorand node:
  - High level overview of nodes, SDKs, sandboxes.

## First steps

### Writing (`algod`) and reading (`indexer`) from the blockchain.

```python
# Source from ./connect.py
```

### Creating an account

- Public keys, private keys, accounts, and mnemonics.
  - Key table and _rekyeing_.

```python
# Source from ./account.py
```

### Funding the account

To fund the account, we can use `goal` (the CLI interface to `algod`):

```bash
goal clerk send -a 1000000 --from $CREATOR_ACCOUNT --to $RECEIVER_ACCOUNT
```

⛲ ...or we can use the [dispenser](https://testnet.algoexplorer.io/dispenser),
since we are working on the _testnet_.

Also, remember to setup the `config.py` file to hold the mnemonic of the account
you just funded 💰.

### First transaction (with note ✍️)

```python
# Source from ./tx.py
```

### Reading transactions

- You can take a look at transactions using
  [AlgoExplorer](https://algoexplorer.io) (remember to select the _testnet_ if
  you are developing :)
- From Python, we can use the _indexer_.

```python
# Source from ./search.py
```

### A first smart contract

- Stateful vs Stateless Smart Contracts (ASC1)
- Let's look at simple smart contract (and TEAL!)

```python
# Source from ./stateless.py
```

### There's a lot more!

- Standard Assets (ASA)
  - NFTs, utility and security tokens, shares.
- Atomic Transfers (AT)
- Multi-signature accounts (_k_ out of _n_)
- 🧱 building blocks to a world of decentralized applications.
