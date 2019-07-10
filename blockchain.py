blockchain = []
open_transactions =[]
owner = "Kevin"

def get_last_blockchain_value():
	if len(blockchain) < 1:
		return None
	return blockchain[-1]


def add_transaction(recipient,sender = owner, amount = 1.0):

	"""
	Arguments:
		:sender: The sender of the coins
		:recipient: The recipient of the coins
		:amount: The amount of coins sent with the transaction (default = 1.0)
	"""
	transaction = {"sender":sender, "recipient":recipient, "amount": amount}
	open_transactions.append(transaction)
    
def mine_block():
	pass

def get_tx_value():
	tx_recipient = input("Enter the recipient of the transaction: ")
	tx_amount = float(input("Enter the amount please: "))
	return (tx_recipient,tx_amount)


def get_user_choice():
	return input("Your choice: ")
	

def print_blockchain_elements():
	for block in blockchain:
		print("Outputting block")
		print(block)
	else:
		print("-" *20)


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

waiting_for_input = True

while waiting_for_input:
	print("Please choose")
	print("1: Add a new transaction value")
	print("2: Output the transaction blocks")
	print("3: Manipulat the chain")
	print("4: Quit")
	
	user_choice = get_user_choice()
	
	if user_choice == "1":
		tx_data = get_tx_value()
		recipient, amount = tx_data
		add_transaction(recipient,amount=amount)
		print(open_transactions)

	elif user_choice =="2":
		print_blockchain_elements()

	elif user_choice =="3":
		if len(blockchain)>=1:
			blockchain[0] = [2]

	elif user_choice == "4":
		waiting_for_input=False

	else:
		print("Input invalid, please pick from the list")

	if verify_chain():
		print("Valid!")
	else:
		print("Invalid!")
		break
else:
	print("User left!")




print("Done!")