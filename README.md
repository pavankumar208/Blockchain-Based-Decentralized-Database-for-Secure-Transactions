
# Advanced DBMS Project - Blockchain Implementation in Python

This project is a simplified blockchain implementation that uses SQLite as a backend database. It demonstrates core blockchain concepts like blocks, transactions, proof-of-work, and hash chaining.

## Features

- Create and store blocks with transactions in SQLite
- Proof-of-Work mining mechanism with adjustable difficulty
- Insert and retrieve transactions by sender
- Genesis block creation on first run
- View full blockchain history

## Technologies Used

- Python 3.x
- SQLite3
- JSON for transaction formatting
- SHA-256 hashing via hashlib

## File

- `ADVANCED DBMS PROJECT.py`: The main application script

## How to Run

1. Ensure you have Python 3 installed.
2. Run the script:
   ```bash
   python "ADVANCED DBMS PROJECT.py"
   ```

3. Use the interactive menu to:
   - Add transactions and mine new blocks
   - Query transactions by sender
   - View the entire blockchain

## Requirements

No external packages are needed; all dependencies are part of the Python standard library.

## Example Menu Options

- **1**: Add transactions and mine a new block
- **2**: Query transactions by sender name
- **3**: Print the full blockchain
- **4**: Exit the program

## License

This project is provided under the MIT License.
