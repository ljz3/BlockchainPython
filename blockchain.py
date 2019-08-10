from functools import reduce
import hashlib as hl
import json

from hash_util import hash_string_256, hash_block
from block import Block
from transaction import Transaction

MINING_REWARD = 10

blockchain = []
open_transactions =[]
owner = "Kevin"

def load_data():
	global blockchain
	global open_transactions
	try:
		with open("blockchain.txt", mode="r") as file:
			file_content = file.readlines()

			blockchain = json.loads(file_content[0][:-1])
			updated_blockchain = []
			for block in blockchain:
				converted_tx = [Transaction(tx["sender"], tx["recipient"], tx["amount"]) for tx in block["transactions"]]
				
				updated_block = Block(block["index"],block["previous_hash"], converted_tx, block["proof"], block["timestamp"])
				updated_blockchain.append(updated_block)

			blockchain = updated_blockchain
			open_transactions= json.loads(file_content[1])
			updated_transactions = []
			for tx in open_transactions:
				updated_transaction = [Transaction(tx["sender"], tx["recipient"], tx["amount"]) for tx in block["transactions"]]
				updated_transactions.append(updated_transaction)
			open_transactions = updated_transactions
	except (IOError, IndexError):
		genesis_block = Block(0, "", [], 100, 0)

		blockchain = [genesis_block]
		open_transactions =[]

	finally:
		print("Cleanup")



load_data()

def get_last_blockchain_value():
	if len(blockchain) < 1:
		return None
	return blockchain[-1]

def verify_transaction(transaction):
	sender_balance = get_balance(transaction.sender)
	return sender_balance >= transaction.amount
		

def add_transaction(recipient,sender = owner, amount = 1.0):

	"""
	Arguments:
		:sender: The sender of the coins
		:recipient: The recipient of the coins
		:amount: The amount of coins sent with the transaction (default = 1.0)
	"""
	# transaction = {
	# 	"sender":sender,
	# 	"recipient":recipient, 
	# 	"amount": amount
	# }

	transaction = Transaction(sender, recipient, amount)

	if verify_transaction(transaction):
		open_transactions.append(transaction)
		save_data()
		return True
	return False


def get_balance(participant):
	
	tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
	open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
	tx_sender.append(open_tx_sender)
	amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
	
	tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]
	amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
	
	return amount_received - amount_sent


def mine_block():
	last_block = blockchain[-1]
	hashed_block = hash_block(last_block)
	proof = proof_of_work()
	# reward_transaction = {
	# 	"sender": "MINING",
	# 	"recipient": owner,
	# 	"amount": MINING_REWARD
	# }

	reward_transaction = Transaction("MINING", owner, MINING_REWARD)

	copied_transactions = open_transactions[:]
	copied_transactions.append(reward_transaction)
	block = Block(len(blockchain), hashed_block, copied_transactions, proof)

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


def save_data():
	try:
		with open("blockchain.txt", mode="w") as file:
			saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in blockchain]]
			file.write(json.dumps(saveable_chain))
			file.write("\n")
			saveable_tx = [tx.__dict__ for tx in open_transactions]
			file.write(json.dumps(saveable_tx))
	except IOError:
		print("Saving Failed")



def valid_proof(transactions, last_hash, proof):
	guess = (str(tx.to_ordered_dict() for tx in transactions) + str(last_hash) + str(proof)).encode()
	guess_hash = hash_string_256(guess)
	#print(guess_hash)
	return guess_hash[0:2] == "00"


def proof_of_work():
	last_block = blockchain[-1]
	last_hash = hash_block(last_block)
	proof = 0
	while not valid_proof(open_transactions, last_hash, proof):
		proof += 1
	return proof


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            print('Proof of work is invalid')
            return False
    return True


def verify_transactions():
	return all([verify_transaction(tx) for tx in open_transactions])

waiting_for_input = True

while waiting_for_input:

	if not verify_chain():
		print("Invalid!")
		break

	print("Please choose")
	print("1: Add a new transaction value")
	print("2: Output the transaction blocks")
	print("3: Mine new block")
	print("4: Output Participants")
	print("5: Check transaction validity")
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
			save_data()

	elif user_choice == "4":
		print("Not available")

	elif user_choice == "5":
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