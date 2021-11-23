from brownie import Lottery, accounts, config, network
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery

# eth is aprox 4k currently, so 50$ fee is roughly .0125 eth
# eth to wei decimals 120000000000000000


# create test script to test sol funcs
# def test_get_entrance_fee():
    # account = accounts[0]
    # lottery = Lottery.deploy(
    #     config["networks"][network.show_active()]["eth_usd_price_feed"],{"from": account})
    # dont use this method, this was just a quick test to grab current eth price for entrance fee function
    # assert lottery.getEntranceFee() > Web3.toWei(0.012, "ether")
    # assert lottery.getEntranceFee() < Web3.toWei(0.022, "ether")

def test_get_entrance_fee():
    # arrange
    lottery = deploy_lottery()
    # act
    # assuming 4,000 eth/usd
    # usdEntryFee = 50
    # 4000/1 == 50/x == 0.0125
    expected_entrance_fee = Web3.toWei(0.012, "ether")
    entrance_fee = lottery.getEntranceFee()
    # assert
    assert expected_entrance_fee == entrance_fee
