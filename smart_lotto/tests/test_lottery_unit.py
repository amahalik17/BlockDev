from brownie import Lottery, accounts, config, network, exceptions
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link, get_contract
import pytest


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
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # arrange
    lottery = deploy_lottery()
    # act
    # assuming 4,000 eth/usd
    # usdEntryFee = 50
    # 4000/1 == 50/x == 0.0125
    expected_entrance_fee = Web3.toWei(0.0125, "ether")
    entrance_fee = lottery.getEntranceFee()
    # assert
    assert expected_entrance_fee == entrance_fee


def test_no_enter_til_start():
    # arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    # act / assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter():
    # arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    # act / assert
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    assert lottery.players(0) == account


def test_can_end():
    # arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    # act /assert
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    assert lottery.lottery_state() == 2


def test_can_pick_winner_correct():
    # arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    # act / assert
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    transaction = lottery.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )
    starting_balance_of_acct = account.balance()
    balance_of_lottery = lottery.balance()
    # 777 % 3 = 259 evenly, so mod is 0 (0th index account)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_acct + balance_of_lottery

