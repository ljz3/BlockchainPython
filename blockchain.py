MINING_REWARD = 10


GENESIS_BLOCK = {
	"previous_hash": "", 
	"index": 0, 
	"transactions": []
	}
blockchain = [GENESIS_BLOCK]
open_transactions =[]
owner = "Kevin"
participants = {"Kevin"}


def get_last_blockchain_value():
	if len(blockchain) < 1:
		return None
	return blockchain[-1]

def verify_transaction(transaction):
	sender_balance = get_balance(transaction["sender"])
	return sender_balance >= transaction["amount"]
		

def add_transaction(recipient,sender = owner, amount = 1.0):

	"""
	Arguments:
		:sender: The sender of the coins
		:recipient: The recipient of the coins
		:amount: The amount of coins sent with the transaction (default = 1.0)
	"""
	transaction = {
		"sender":sender,
		"recipient":recipient, 
		"amount": amount
	}

	if verify_transaction(transaction):
		open_transactions.append(transaction)
		participants.add(sender)
		participants.add(recipient)
		return True
	return False


def get_balance(participant):
	tx_sender = [[tx["amount"] for tx in block["transactions"] if tx["sender"] == participant] for block in blockchain]
	open_tx_sender = [tx["amount"] for tx in open_transactions if tx["sender"] == participant]
	tx_sender.append(open_tx_sender)
	amount_sent = 0
	for tx in tx_sender:
		if len(tx) > 0:
			amount_sent += tx[0]
	tx_recipient = [[tx["amount"] for tx in block["transactions"] if tx["recipient"] == participant] for block in blockchain]
	amount_received = 0
	for tx in tx_recipient:
		if len(tx) > 0:
			amount_received += tx[0]

	return amount_received - amount_sent


def mine_block():
	last_block = blockchain[-1]
	hashed_block = hash_block(last_block)
	reward_transaction = {
		"sender": "MINING",
		"recipient": owner,
		"amount": MINING_REWARD
	}
	copied_transactions = open_transactions[:]
	copied_transactions.append(reward_transaction)
	block = {
		"previous_hash": hashed_block, 
		"index": len(blockchain), 
		"transactions": copied_transactions
	}
	blockchain.append(block)
	return True


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


def hash_block(block):
	return "-".join([str(block[key]) for key in block])


def verify_chain():
	for (index,block) in enumerate(blockchain):
		if index == 0:
			continue

		if block["previous_hash"] != hash_block(blockchain[index-1]):
			return False
	return True


def verify_transactions():
	return all([verify_transaction(tx) for tx in open_transactions])

waiting_for_input = True

while waiting_for_input:
	print("Please choose")
	print("1: Add a new transaction value")
	print("2: Output the transaction blocks")
	print("3: Mine new block")
	print("4: Manipulate the chain")
	print("5: Output Participants")
	print("6: Check transaction validity")
	print("q: Quit")
	
	user_choice = get_user_choice()
	
	if user_choice == "1":
		tx_data = get_tx_value()
		recipient, amount = tx_data
		if add_transaction(recipient,amount=amount):
			print("Added Transaction!")
		else:
			print("Transaction Failed")
		print(open_transactions)


	elif user_choice =="2":
		print_blockchain_elements()

	elif user_choice =="3":
		if mine_block():
			open_transactions = []

	elif user_choice =="4":
		if len(blockchain)>=1:
			blockchain[0] = {
				"previous_hash": "", 
				"index": 0, 
				"transactions": [{"sender": "Kevin", "recipient": "Seth", "amount": 100}]
			}

	elif user_choice == "5":
		print(participants)

	elif user_choice == "6":
		if verify_transactions():
			print("All transactions are valid")
		else:
			print("There are invalid transactions")

	elif user_choice == "q":
		waiting_for_input=False

	else:
		print("Input invalid, please pick from the list")

	if verify_chain():
		print("Valid!")
	else:
		print("Invalid!")
		break
	
	print(get_balance("Kevin"))

else:
	print("User left!")



print("Done!")