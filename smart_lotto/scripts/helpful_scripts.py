# import dependencies
from brownie import (
    network, config, accounts, interface,
    Contract,
    MockV3Aggregator, 
    VRFCoordinatorMock, 
    LinkToken
)
from web3 import Web3


FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'ganache-local']

DECIMALS = 8
STARTING_PRICE = 400000000000

def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env_var")
    # accounts.load("id")
    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS 
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    return accounts.add(config['wallets']['from_key'])

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator, 
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken
}

def get_contract(contract_name):
    """This function will grab the contract addresses from brownie config if defined, 
    otherwise it will deploy a mock version of that contract, and return that mock contract.
    args: contract_name(string)
    returns: brownie.network.contract.ProjectContract: the most recently 
    deployed version of this contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            # MockV3Aggregator
            deploy_mocks()
        # most recent mock
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address, abi, mockv3.abi
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract


def deploy_mocks(decimals=DECIMALS, starting_price=STARTING_PRICE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, starting_price, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    # if len(MockV3Aggregator) <= 0:
    #     MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {'from': get_account()})
    print(f'The active network is {network.show_active()}')
    print('Mocks deployed!')


def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # another way to do this, comment out above line and uncomment these two below
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Fund contract")
    return tx



