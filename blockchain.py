blockchain = []

def get_last_blockchain_value():
    return blockchain[-1]


def add_value(transaction_amount, last_transaction = [1]):
    blockchain.append([last_transaction,transaction_amount])
    

def get_tx_value():
    return float(input("Your transaction amount please: "))

def get_user_choice():
	return input("Your choice: ")
	

def print_blockchain_elements():
	for block in blockchain:
		print("Outputting block")
		print(block)


tx_amount = get_tx_value()
add_value(tx_amount)


while True:
	print("Please choose")
	print("1: Add a new transaction value")
	print("2: Output the transaction blocks")
	print("3: Quit")
	
	user_choice = get_user_choice()
	
	if user_choice == "1":
		tx_amount = get_tx_value()
		add_value(tx_amount, get_last_blockchain_value())
	elif user_choice =="2":
		print_blockchain_elements()
	elif user_choice == "3":
		break
	else:
		print("Input invalid, please pick from the list")
	
	

print("Done!")