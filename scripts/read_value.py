from brownie import SimpleStorage, accounts, config



def read_contracts():
    # for most recent deployment(one less than the length)
    # brownie auto knows the abi and address from the json files created
    simple_storage = SimpleStorage[-1]
    print(simple_storage.retrieve())




def main():
    read_contracts()