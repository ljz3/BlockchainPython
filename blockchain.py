blockchain = []

def get_last_blockchain_value():
	if len(blockchain) < 1:
		return None
	return blockchain[-1]


def add_transaction(transaction_amount, last_transaction = [1]):
	if last_transaction == None:
		last_transaction = [1]
	blockchain.append([last_transaction,transaction_amount])
    

def get_tx_value():
    return float(input("Your transaction amount please: "))

def get_user_choice():
	return input("Your choice: ")
	

def print_blockchain_elements():
	for block in blockchain:
		print("Outputting block")
		print(block)


def verify_chain():
	block_index = 0
	is_valid = True
	for block in blockchain:
		if block_index==0:
			block_index+=1
			continue
		elif block[0] == blockchain[block_index-1]:
			is_valid = True
		else:
			is_valid = False
			break
		block_index+=1
	return is_valid


while True:
	print("Please choose")
	print("1: Add a new transaction value")
	print("2: Output the transaction blocks")
	print("3: Manipulat the chain")
	print("4: Quit")
	
	user_choice = get_user_choice()
	
	if user_choice == "1":
		tx_amount = get_tx_value()
		add_transaction(tx_amount, get_last_blockchain_value())
	elif user_choice =="2":
		print_blockchain_elements()
	elif user_choice =="3":
		if len(blockchain)>=1:
			blockchain[0] = [2]
	elif user_choice == "4":
		break
	else:
		print("Input invalid, please pick from the list")

	if verify_chain():
		print("Valid!")
	else:
		print("Invalid!")
		break
	

print("Done!")