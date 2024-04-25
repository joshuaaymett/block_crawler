"""
Script for getting blocks in a range and persisting to a sqlite database
"""

from time import sleep
import sqlite3
import re
import click
import requests
from blockchain_requests import QuickNodeEtheriumRequest
from schemas.etherium_schema import TRANSACTION_SCHEMA, BLOCK_SCHEMA


def get_nullable_val_from_dict(dictionary: dict, key: str) -> str:
    """
    .get returns None as a string if the value is None. QuickNode documentation was unclear
    about type of return value, therefore "None" and None are used as a precaution
    """
    val = dictionary.get(key)
    if val in [None, "None"]:
        return "NULL"
    return val


def get_block_range(block_range: str) -> tuple:
    """
    Returns tuple (start, end) for block range string and performs input validation
    """
    if not re.match(r"^\d+-\d+$", block_range):
        raise ValueError(
            f"Invalid block range {block_range}. Input must be of format start-end (e.g. 10-14)"
        )
    split_br: str = str(block_range).split("-")
    start, end = int(split_br[0]), int(split_br[1])
    if not end >= start:
        raise ValueError(
            f"Invalid block range {start}-{end}, start of block range must be less than or equal to end"
        )
    return (start, end)


@click.command()
@click.option(
    "--endpoint",
    help="A JSON-RPC endpoint to call an Ethereum client (e.g. https://rpc.quicknode.pro/key)",
)
@click.option(
    "--db-path",
    help="The path of the SQLite file to write to \
        (e.g. db.sqlite3)",
)
@click.option(
    "--block-range",
    help="A block range (inclusive), formatted as '{start}-{end}', (e.g. 200-300)",
)
def block_crawler(endpoint: str, db_path: str, block_range: str):
    """
    Main script
    """
    br_start, br_end = get_block_range(block_range)

    responses: list = []
    for block_num in range(br_start, br_end + 1):
        req = QuickNodeEtheriumRequest(
            call_name="eth_getBlockByNumber",
            url=endpoint,
            parameters=[hex(block_num), True],
        )
        # Retry once if an error occurs after sleep (e.g. hit quota)
        try:
            responses.append(requests.post(**req.get_request_params()))
        except:
            sleep(1)
            responses.append(requests.post(**req.get_request_params()))

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Create transaction table and then create block table with transaction as a foreign key
    cur.execute(f"CREATE TABLE IF NOT EXISTS `transaction` ({TRANSACTION_SCHEMA})")
    cur.execute(f"CREATE TABLE IF NOT EXISTS block ({BLOCK_SCHEMA})")

    # Save responses in database
    for response in responses:
        # Save blocks to block table
        results_json = response.json()["result"]
        block_hash = get_nullable_val_from_dict(results_json, "hash")
        number = get_nullable_val_from_dict(results_json, "number")
        timestamp = int(results_json["timestamp"], 16)
        transactions = results_json["transactions"]
        cur.execute(
            f"INSERT INTO block (hash, number, timestamp) VALUES ('{block_hash}', '{number}', datetime({timestamp}, 'unixepoch'))"
        )
        # Save transactions to transaction table
        for transaction in transactions:
            t_hash = transaction["hash"]
            t_block_hash = get_nullable_val_from_dict(transaction, "blockHash")
            t_block_number = get_nullable_val_from_dict(transaction, "blockNumber")
            t_from = transaction["from"]
            t_to = get_nullable_val_from_dict(transaction, "to")
            t_value = transaction["value"]
            cur.execute(
                f"INSERT INTO `transaction` (hash, blockHash, blockNumber, `from`, `to`, value) \
                VALUES ('{t_hash}', '{t_block_hash}', '{t_block_number}', '{t_from}', '{t_to}', '{t_value}')"
            )

    con.commit()
    con.close()


if __name__ == "__main__":
    block_crawler()
