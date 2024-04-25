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
This project is intended as a POC. Duplicate blocks/transactions are allowed in tables as each table uses a surrogate key, "id", as the primary key.

### Input Validation
Input validation is performed to ensure valid block ranges. Database path and endpoint inputs are not validated as requests and sqlite libraries will throw errors with invalid inputs.

### Database
Most fields are stored in hexadecimal in order to prevent integer overflow caused by SQLite's limited (8 byte) integer. For a production database, Postgres may be better suited due to its numeric type; however, for this project, SQLite was used for simplicity.

### Easy Expansion
The current structure src/blockchain_requests allows for easy addition of new APIs/blockchains. The structure may require additional folders (e.g. src/blockchain_requests/quicknode/etherium.py, etc.) should many additional APIs/blockchains be added. Schemas are structured similarly.

### Exception handling
Current exception handling is limited to a single retry after a sleep to account for exceptions caused by endpoint limits. This could be further enhanced to dynamically adjust according to rate limits.

SQLite commit is intentionally placed at the end of the script to ensure ACID compliance

## Potential Improvements
- Batch database insertions
- Add multithreading for endpoint requests (account for endpoint request limits, add "smart" functionality for dynamically adjusting)
- Unit testing
