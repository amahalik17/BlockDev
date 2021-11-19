# import packages/dependencies
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS, FORKED_LOCAL_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest

def test_can_f_and_w():

    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx = fund_me.fund({'from': account, 'value': entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({'from': account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0
    
def test_only_owner_withdraw():

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    # test to make sure only owner can withdraw
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    #fund_me.withdraw({"from": bad_actor})

    # now add raise exception error from pytest
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})

