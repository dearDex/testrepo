from web3 import Web3
import json
import time

monad_rpc = 'https://testnet-rpc.monad.xyz'
w3 = Web3(provider=Web3.HTTPProvider(
    endpoint_uri=monad_rpc
))

if not w3.is_connected():
    raise Expection("Не удалось подключиться RPC к сети Monad")

private_key = ''
my_address = ''
account = w3.eth.account.from_key(private_key=private_key)


octo_contract_address = Web3.to_checksum_address('0xCa9A4F46Faf5628466583486FD5ACE8AC33ce126')
octo_contract_abi = json.load(open('data/abis/default_token.json'))
octo_contract = w3.eth.contract(address=octo_contract_address, abi=octo_contract_abi)

octoswap_contract_address = Web3.to_checksum_address('0xb6091233aAcACbA45225a2B2121BBaC807aF4255')
octoswap_contract_abi = json.load(open('data/abis/octoswap.json'))
octoswap_contract = w3.eth.contract(address=octoswap_contract_address, abi=octoswap_contract_abi)

gmon_address = Web3.to_checksum_address('0xaEef2f6B429Cb59C9B2D7bB2141ADa993E8571c3')
gmon_contract = w3.eth.contract(address= gmon_address, abi=octo_contract_abi)

decimals = gmon_contract.functions.decimals().call()
gmon_amount = int(1 * (10 ** decimals))

    # gmon_price = 1.92
    # gmon_amount = 0.05
    # gmon_decimals = 18

    # slippage = 0.5
    # min_to_amount = gmon_price * gmon_amount * (1 - slippage / 100)

    # octo_decimals = octo_contract.functions.decimals().call()
    # gmon_amount = int(gmon_amount * 10 ** gmon_decimals)
    # octo_amount = int(min_to_amount * 10 ** octo_decimals)



approve_txn = gmon_contract.functions.approve(octoswap_contract_address, gmon_amount).build_transaction({
    'from': my_address,
    'nonce': w3.eth.get_transaction_count(my_address),
    'gas': 100000,
    'gasPrice': w3.eth.gas_price,
    'chainId': 10143
})
signed_approve = w3.eth.account.sign_transaction(approve_txn, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_approve.raw_transaction)
print(f"Approve TX sent: {w3.to_hex(tx_hash)}")
w3.eth.wait_for_transaction_receipt(tx_hash)

amountOutMin = 0
path = [gmon_address, octo_contract_address]
deadline = w3.eth.get_block('latest')['timestamp'] + 600

swap_txn = octoswap_contract.functions.swapExactTokensForTokens(
    gmon_amount,
    amountOutMin,
    path,
    my_address,
    deadline
).build_transaction({
    'from': my_address,
    'nonce': w3.eth.get_transaction_count(my_address),
    'gas': 200000,
    'gasPrice': w3.eth.gas_price,
    'chainId': 10143
})


sign = w3.eth.account.sign_transaction(swap_txn, private_key)
tx = w3.eth.send_raw_transaction(sign.raw_transaction)

tx_data = w3.eth.wait_for_transaction_receipt(tx, timeout = 200)

if 'status' in tx_data and tx_data['status'] == 1:
    print(f'transaction was successful: {tx.hex()}')
else:
    print(f'transaction failed {tx_data["transactionHash"].hex()}')


Add Line
