from brownie import EasyToken, accounts, config
#from scripts.helpful import get_account
from web3 import Web3

initial_supply = Web3.toWei(1000000, "ether")
token_name = "EASYTOKEN"
token_symbol = "ET"

def main():
    account = accounts[0]
    easytoken = EasyToken.deploy(initial_supply, {"from": account})
