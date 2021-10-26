from solcx import compile_standard, install_solc
import json

install_solc('0.6.0')

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile our solidity contracts

compiled_sol = compile_standard(
    {"language": "Solidity",
    "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
    "settings": {
        "outputSelection": {
            "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
        }
    },
    },
    solc_version="0.6.0",
)
print(compiled_sol)

with open("compiled_code.json", "W") as file:
    json.dump(compiled_sol, file)

    # get bytecode to we can deploy
