import hashlib
import json
import sqlite3
import time

class BlockchainDB:
    def __init__(self, db_file='blockchain.db'):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()
        if self.get_latest_block() is None:
            self.create_genesis_block()

    def create_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS blocks (
                        id INTEGER PRIMARY KEY,
                        timestamp REAL,
                        previous_hash TEXT,
                        nonce INTEGER,
                        hash TEXT
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        block_id INTEGER,
                        sender TEXT,
                        recipient TEXT,
                        amount REAL,
                        FOREIGN KEY(block_id) REFERENCES blocks(id)
                    )''')
        self.conn.commit()

    def create_genesis_block(self):
        genesis_block = {
            'index': 0,
            'timestamp': time.time(),
            'transactions': [],
            'previous_hash': "0",
            'nonce': 0
        }
        genesis_hash = self.calculate_hash(genesis_block)
        self.insert_block(0, genesis_block['timestamp'], genesis_block['previous_hash'], genesis_block['nonce'], genesis_hash)
        print("Genesis block created")

    def calculate_hash(self, block):
        block_string = json.dumps({
            'index': block.get('index', None),
            'timestamp': block['timestamp'],
            'transactions': block.get('transactions', []),
            'previous_hash': block['previous_hash'],
            'nonce': block['nonce']
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def insert_block(self, index, timestamp, previous_hash, nonce, block_hash):
        c = self.conn.cursor()
        c.execute('INSERT INTO blocks (id, timestamp, previous_hash, nonce, hash) VALUES (?, ?, ?, ?, ?)',
                  (index, timestamp, previous_hash, nonce, block_hash))
        self.conn.commit()

    def insert_transaction(self, block_id, sender, recipient, amount):
        c = self.conn.cursor()
        c.execute('INSERT INTO transactions (block_id, sender, recipient, amount) VALUES (?, ?, ?, ?)',
                  (block_id, sender, recipient, amount))
        self.conn.commit()

    def get_latest_block(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM blocks ORDER BY id DESC LIMIT 1')
        return c.fetchone()

    def get_transactions_by_sender(self, sender):
        c = self.conn.cursor()
        c.execute('SELECT * FROM transactions WHERE sender = ?', (sender,))
        return c.fetchall()

    def add_block(self, transactions, previous_hash, difficulty=2):
        index = self.get_latest_block()[0] + 1
        nonce = 0
        timestamp = time.time()

        block = {
            'index': index,
            'timestamp': timestamp,
            'transactions': transactions,
            'previous_hash': previous_hash,
            'nonce': nonce
        }

        block_hash = self.calculate_hash(block)
        target = '0' * difficulty

        print(f"Mining block {index}...")
        while not block_hash.startswith(target):
            nonce += 1
            block['nonce'] = nonce
            block_hash = self.calculate_hash(block)

        self.insert_block(index, timestamp, previous_hash, nonce, block_hash)
        for tx in transactions:
            self.insert_transaction(index, tx['sender'], tx['recipient'], tx['amount'])

        print(f"Block {index} mined with hash {block_hash}")

    def print_chain(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM blocks ORDER BY id')
        blocks = c.fetchall()
        for block in blocks:
            print(f"\nBlock ID: {block[0]}, Hash: {block[4]}")
            print(f"Previous Hash: {block[2]}, Nonce: {block[3]}, Timestamp: {time.ctime(block[1])}")
            c.execute('SELECT sender, recipient, amount FROM transactions WHERE block_id=?', (block[0],))
            transactions = c.fetchall()
            if transactions:
                print(" Transactions:")
                for tx in transactions:
                    print(f"  - Sender: {tx[0]}, Recipient: {tx[1]}, Amount: {tx[2]}")
            else:
                print(" No transactions")

def main():
    blockchain = BlockchainDB()

    while True:
        print("\nMenu:")
        print("1. Add new transactions and mine a block")
        print("2. Query transactions by sender")
        print("3. Print the entire blockchain")
        print("4. Exit")
        choice = input("Enter choice (1-4): ")

        if choice == '1':
            transactions = []
            while True:
                sender = input("Enter sender name (or 'done' to finish): ")
                if sender.lower() == 'done':
                    break
                recipient = input("Enter recipient name: ")
                try:
                    amount = float(input("Enter amount: "))
                except ValueError:
                    print("Invalid amount. Try again.")
                    continue

                transactions.append({'sender': sender, 'recipient': recipient, 'amount': amount})
                print("Transaction added.")

            if transactions:
                latest_block = blockchain.get_latest_block()
                previous_hash = latest_block[4] if latest_block else "0"
                blockchain.add_block(transactions, previous_hash)
            else:
                print("No transactions to add.")

        elif choice == '2':
            sender = input("Enter sender name to query transactions: ")
            txs = blockchain.get_transactions_by_sender(sender)
            if txs:
                print(f"Transactions by {sender}:")
                for tx in txs:
                    print(f"  ID: {tx[0]}, Block ID: {tx[1]}, Recipient: {tx[3]}, Amount: {tx[4]}")
            else:
                print("No transactions found for this sender.")

        elif choice == '3':
            blockchain.print_chain()

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
