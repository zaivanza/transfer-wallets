import json
from pathlib import Path

STR_DONE    = '✅ '
STR_CANCEL  = '❌ '

max_time_check_tx_status = 100 # в секундах. если транза не выдаст статус за это время, она будет считаться исполненной

def load_json(filepath: Path | str):
    with open(filepath, "r") as file:
        return json.load(file)
    
def read_txt(filepath: Path | str):
    with open(filepath, "r") as file:
        return [row.strip() for row in file]
    
def call_json(result: list | dict, filepath: Path | str):
    with open(f"{filepath}.json", "w") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

ERC20_ABI = load_json("data/erc20.json")
WALLETS = read_txt("data/wallets.txt")
RECIPIENTS = read_txt("data/recipients.txt")
RECIPIENTS_WALLETS = dict(zip(WALLETS, RECIPIENTS))
