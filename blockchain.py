blockchain = []

def get_last_blockchain_value():
    return blockchain[-1]


def add_value(transaction_amount, last_transaction = [1]):
    blockchain.append([last_transaction,transaction_amount])
    

tx_amount = input("Your transaction amount please: ")

add_value(tx_amount)
add_value(last_transaction=get_last_blockchain_value(),transaction_amount=0.9)
add_value(10, get_last_blockchain_value())

print(blockchain)