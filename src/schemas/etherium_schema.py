"""
File to store etherium-related schemas

NOTE: Certain fields can be nullable if in pending state
"""

TRANSACTION_SCHEMA = """
id INTEGER PRIMARY KEY AUTOINCREMENT,
hash TEXT NOT NULL,
blockHash TEXT,
blockNumber TEXT,
`from` TEXT NOT NULL,
`to` TEXT,
value TEXT NOT NULL
"""

BLOCK_SCHEMA = """
id INTEGER PRIMARY KEY AUTOINCREMENT,
hash TEXT,
number TEXT,
timestamp TEXT NOT NULL
"""
