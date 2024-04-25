# block_crawler

## Description
This project is a sample of how to query the Etherium blockchain and save results in a SQLite3 database. It is based on Relayer's technical challenge (PDF of assignment included)

## Usage
The script takes three arguments:
--endpoint: A QuickNode endpoint (see technical challenge PDF for instructions on how to set up)
--db-path: Path to SQLite database
--block-range: Inclusive block range to query and save to DB (e.g. 10-13 includes blocks 10, 11, 12, and 13)

e.g. 
python block_crawler.py --endpoint <quicknode_endpoint> --db-path foo.db --block-range 19727985-19727990

## Design
This project is intended as a sample and lacks input validation. It also has minimal exception handling which would need to be addded before using in a production environment. Duplicate blocks/transactions are allowed in tables as each table uses a surrogate key, "id", as the primary key.

### Easy Expansion
The current structure src/blockchain_requests allows for easy addition of new APIs/blockchains. The structure may require additional folders (e.g. src/blockchain_requests/quicknode/etherium.py, etc.) should many additional APIs/blockchains be added. Schemas are structured similarly.

### Exception handling
Current exception handling is limited to a single retry after a sleep to account for exceptions caused by endpoint limits.

SQLite commit is intentionally placed at the end of the script to ensure ACID compliance

## Potential Improvements
- Batch database insertions
- Add multithreading for endpoint requests (account for endpoint request limits, add "smart" functionality for dynamically adjusting)
- Add input validation
- Enhance exception handling
- Unit testing
