from brownie import HyperFund, accounts, config
#from scripts.helpful import get_account
from web3 import Web3

initial_supply = Web3.toWei(1000000, "ether")
token_name = "HYPERFUND"
token_symbol = "HF"

def main():
    account = accounts[0]
    hyperfund = HyperFund.deploy(initial_supply, token_name, token_symbol, {"from": account})
