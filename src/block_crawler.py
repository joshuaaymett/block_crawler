import click
from blockchain_requests import QuickNodeEtheriumRequest
import requests


@click.command()
@click.option(
    "--endpoint",
    help="A JSON-RPC endpoint to call an Ethereum client (e.g. https://rpc.quicknode.pro/key)",
)
@click.option(
    "--db-path",
    help="The path of the SQLite file to write to or a connection URI (e.g. db.sqlite3 or postgresql://user:password@localhost:5432/database)",
)
@click.option(
    "--block-range",
    help="A block range (inclusive), formatted as '{start}-{end}', (e.g. 200-300)",
)
def block_crawler(endpoint: str, db_path: str, block_range: str):
    split_br: str = str(block_range).split("-")
    br_start: int = int(split_br[0])
    br_end: int = int(split_br[1])

    for block_num in range(br_start, br_end + 1):
        req = QuickNodeEtheriumRequest(
            call_name="eth_getBlockByNumber",
            url=endpoint,
            parameters=[hex(block_num), True],
        )
        print(requests.post(**req.get_request_params()).text)

    # TODO save to DB


if __name__ == "__main__":
    block_crawler()


# TODO save method should be a class that allows for easy expansion for other db types
# TODO comment and document code thoroughly
# TODO update requirements.txt
# TODO blockchain type should be designed in a way where adding new ones are flexible
# TODO add a couple unit tests? or at least document
# TODO document that input validation could be added, multithreading could be added
# TODO document inclusive range
