genesis_block = {
	"previous_hash": "", 
	"index": 0, 
	"transactions": []
	}
blockchain = [genesis_block]
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
	last_block = blockchain[-1]
	hashed_block = "-".join([str(last_block[key]) for key in last_block])
	print(hashed_block)
	block = {
	"previous_hash": hashed_block, 
	"index": len(blockchain), 
	"transactions": open_transactions
	}
	blockchain.append(block)


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
	print("3: Mine new block")
	print("4: Manipulat the chain")
	print("5: Quit")
	
	user_choice = get_user_choice()
	
	if user_choice == "1":
		tx_data = get_tx_value()
		recipient, amount = tx_data
		add_transaction(recipient,amount=amount)
		print(open_transactions)

	elif user_choice =="2":
		print_blockchain_elements()

	elif user_choice =="3":
		mine_block()

	elif user_choice =="4":
		if len(blockchain)>=1:
			blockchain[0] = [2]

	elif user_choice == "5":
		waiting_for_input=False

	else:
		print("Input invalid, please pick from the list")

#	if verify_chain():
#		print("Valid!")
#	else:
#		print("Invalid!")
#		break

else:
	print("User left!")



print("Done!")