from brownie import SimpleStorage, accounts

def test_deploy():
    # arrange
    account = accounts[0]
    # act
    simple_storage = SimpleStorage.deploy({"from": account})
    start_value = simple_storage.retrieve()
    expected = 0
    # assert
    assert start_value == expected

def test_updating():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    
    expected = 15
    simple_storage.store(expected, {"from": account})
    
    assert expected == simple_storage.retrieve()
