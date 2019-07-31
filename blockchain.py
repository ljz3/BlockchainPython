from functools import reduce
import hashlib as hl
import json

MINING_REWARD = 10


GENESIS_BLOCK = {
	"previous_hash": "", 
	"index": 0, 
	"transactions": [],
	"proof": 100
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

	amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

	tx_recipient = [[tx["amount"] for tx in block["transactions"] if tx["recipient"] == participant] for block in blockchain]
	amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

	return amount_received - amount_sent


def mine_block():
	last_block = blockchain[-1]
	hashed_block = hash_block(last_block)
	proof = proof_of_work()
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
		"transactions": copied_transactions,
		"proof": proof
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
	return hl.sha256(json.dumps(block).encode()).hexdigest()



def valid_proof(transactions, last_hash, proof):
	guess = (str(transactions) + str(last_hash) + str(proof)).encode()
	guess_hash = hl.sha256(guess).hexdigest()
	print(guess_hash)
	return guess_hash[0:2] == "00"


def proof_of_work():
	last_block = blockchain[-1]
	last_hash = hash_block(last_block)
	proof = 0
	while not valid_proof(open_transactions, last_hash, proof):
		proof += 1
	return proof


def verify_chain():
	for (index,block) in enumerate(blockchain):
		if index == 0:
			continue
		if block["previous_hash"] != hash_block(blockchain[index-1]):
			return False
		if not valid_proof(block["transactions"][:-1], block["previous_hash"], block["proof"]):
			print("POW is invalid")
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

	if not verify_chain():
		print("Invalid!")
		break
	
	print("Balance of {}: {:6.2f}".format("Kevin", get_balance("Kevin")))

else:
	print("User left!")



print("Done!")