from config import RECIPIENTS_WALLETS, WALLETS, STR_DONE, STR_CANCEL, ERC20_ABI, max_time_check_tx_status
from data.data import TG_TOKEN, TG_ID, DATA
from setting import RETRY, RANDOM_WALLETS, TG_BOT_SEND, WALLETS_IN_BATCH, MIN_TRANSFER_USD, MIN_TRANSFER_AMOUNT, SLEEPING_TIME

from loguru import logger
import time
from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
import random
import asyncio, aiohttp
import telebot
import math

MULTIPLIER = 1.5 # на сколько будет умножаться (gas * gasPrice), если монета нативная и выводим весь баланс
    
list_send = []
def send_msg():

    try:
        str_send = '\n'.join(list_send)
        bot = telebot.TeleBot(TG_TOKEN)
        bot.send_message(TG_ID, str_send, parse_mode='html')  

    except Exception as error: 
        logger.error(error)

def intToDecimal(qty, decimal):
    return int(qty * int("".join(["1"] + ["0"]*decimal)))

def decimalToInt(qty, decimal):
    return qty/ int("".join((["1"]+ ["0"]*decimal)))

def round_to(num, digits=3):
    try:
        if num == 0: return 0
        scale = int(-math.floor(math.log10(abs(num - int(num))))) + digits - 1
        if scale < digits: scale = digits
        return round(num, scale)
    except: return num

async def get_price(session, symbol):
    try:
        if symbol == 'CORE':
            url = 'https://min-api.cryptocompare.com/data/price?fsym=COREDAO&tsyms=USDT'
        else:
            url = f'https://min-api.cryptocompare.com/data/price?fsym={symbol}&tsyms=USDT'

        async with session.get(url, timeout=10) as resp:
            if resp.status == 200:
                resp_json = await resp.json(content_type=None)
                return float(resp_json.get('USDT', 0))
            else:
                logger.error(f'Failed to fetch price for {symbol}. Status code: {resp.status}')
                return 0
    except Exception as error:
        logger.error(f'Error while fetching price for {symbol}: {error}')
        return 0

async def get_prices(datas):
    prices = {}

    for chain, coins in datas.items():
        web3 = Web3(Web3.HTTPProvider(DATA[chain]['rpc']))

        for address_contract in coins:
            if address_contract == '':  # eth
                symbol = DATA[chain]['token']
            else:
                token_contract = web3.eth.contract(address=Web3.to_checksum_address(address_contract), abi=ERC20_ABI)
                symbol = token_contract.functions.symbol().call()

            prices[symbol] = 0

    async with aiohttp.ClientSession() as session:
        tasks = [get_price(session, symbol) for symbol in prices]

        results = await asyncio.gather(*tasks)

    for symbol, price in zip(prices.keys(), results):
        prices[symbol] = price

    return prices

class Web3ManagerAsync:
    
    def __init__(self, key, chain):
        self.key = key
        self.chain = chain
        self.web3 = self.get_web3()
        self.address = self.web3.eth.account.from_key(self.key).address
        self.chain_id = DATA[self.chain]['chain_id']

    def get_web3(self):
        rpc = DATA[self.chain]['rpc']
        web3 = Web3(AsyncHTTPProvider(rpc), modules={"eth": (AsyncEth)}, middlewares=[])
        return web3

    async def add_gas_limit(self, contract_txn):

        value = contract_txn['value']
        contract_txn['value'] = 0
        pluser = [1.02, 1.05]
        gasLimit = await self.web3.eth.estimate_gas(contract_txn)
        contract_txn['gas'] = int(gasLimit * random.uniform(pluser[0], pluser[1]))

        contract_txn['value'] = value
        return contract_txn

    async def add_gas_price(self, contract_txn):

        if self.chain == 'bsc':
            contract_txn['gasPrice'] = 1000000000 # специально ставим 1 гвей, так транза будет дешевле
        else:
            gas_price = await self.web3.eth.gas_price
            contract_txn['gasPrice'] = int(gas_price * random.uniform(1.01, 1.02))
        return contract_txn

    async def get_data_token(self, token_address):

        try:

            token_contract  = self.web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
            decimals        = await token_contract.functions.decimals().call()
            symbol          = await token_contract.functions.symbol().call()
            return token_contract, decimals, symbol
        
        except Exception as error:
            logger.error(error)

    async def sign_tx(self, contract_txn):

        signed_tx = self.web3.eth.account.sign_transaction(contract_txn, self.key)
        raw_tx_hash = await self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash = self.web3.to_hex(raw_tx_hash)
        
        return tx_hash
    
    async def get_status_tx(self, tx_hash):

        logger.info(f'{self.chain} : checking tx_status : {tx_hash}')
        start_time_stamp = int(time.time())

        while True:
            try:

                receipt = await self.web3.eth.get_transaction_receipt(tx_hash)
                status = receipt["status"]
                if status in [0, 1]:
                    return status

            except Exception as error:
                # logger.info(f'error, try again : {error}')
                time_stamp = int(time.time())
                if time_stamp-start_time_stamp > max_time_check_tx_status:
                    logger.info(f'не получили tx_status за {max_time_check_tx_status} sec, думаем что tx is success')
                    return 1
                # time.sleep(1)
                await asyncio.sleep(1)

    async def send_tx(self, contract_txn):

        try:

            tx_hash = await self.sign_tx(contract_txn)
            status  = await self.get_status_tx(tx_hash)
            tx_link = f'{DATA[self.chain]["scan"]}/{tx_hash}'

            return status, tx_link
        
        except Exception as error:
            logger.error(error)
            return False, False

    async def get_token_info(self, token_address):

        if token_address == '': 
            address = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
            decimal = 18
            symbol = DATA[self.chain]['token']
            token_contract = ''
        else:
            address = token_address
            token_contract, decimal, symbol = await self.get_data_token(token_address)

        return {'address': address, 'symbol': symbol, 'decimal': decimal, 'contract': token_contract}
    
    async def get_balance(self, token_address):

        while True:
            try:
                    
                token_data = await self.get_token_info(token_address)

                if token_address == '': # eth
                    balance = await self.web3.eth.get_balance(self.web3.to_checksum_address(self.address))
                else:
                    balance = await token_data['contract'].functions.balanceOf(self.web3.to_checksum_address(self.address)).call()

                balance_human = decimalToInt(balance, token_data['decimal']) 
                return balance_human

            except Exception as error:
                logger.error(error)
                time.sleep(1)

class Transfer:
    
    def __init__(self, number, key, chain, token):
        self.key = key
        self.number = number
        self.chain = chain
        self.token = token
        self.to_address = RECIPIENTS_WALLETS[self.key]
        self.manager = Web3ManagerAsync(self.key, self.chain)

    async def setup(self):
        self.amount = await self.manager.get_balance(self.token)
        self.token_data = await self.manager.get_token_info(self.token)
        self.symbol = self.token_data['symbol']
        self.value = intToDecimal(self.amount, self.token_data['decimal']) 
        self.module_str = f'{self.number} {self.manager.address} | {round_to(self.amount)} {self.symbol} transfer => {self.to_address}'

    async def get_txn(self):

        try:

            if self.token == '':
                contract_txn = {
                    'from': self.manager.address,
                    'chainId': self.manager.chain_id,
                    'gasPrice': 0,
                    'nonce': await self.manager.web3.eth.get_transaction_count(self.manager.address),
                    'gas': 0,
                    'to': Web3.to_checksum_address(self.to_address),
                    'value': self.value
                }

                gas_gas = int(contract_txn['gas'] * contract_txn['gasPrice'] * MULTIPLIER) 
                contract_txn['value'] = contract_txn['value'] - gas_gas

            else:
                contract_txn = await self.token_data['contract'].functions.transfer(
                    Web3.to_checksum_address(self.to_address),
                    int(self.value)
                    ).build_transaction(
                        {
                            'from': self.manager.address,
                            'chainId': self.manager.chain_id,
                            'gasPrice': 0,
                            'gas': 0,
                            'nonce': await self.manager.web3.eth.get_transaction_count(self.manager.address),
                            'value': 0
                        }
                    )
                
            contract_txn = await self.manager.add_gas_price(contract_txn)
            contract_txn = await self.manager.add_gas_limit(contract_txn)

            if self.token == '':
                gas_gas = int(contract_txn['gas'] * contract_txn['gasPrice'] * MULTIPLIER) 
                contract_txn['value'] = contract_txn['value'] - gas_gas
            
            return contract_txn
            
        except Exception as error:
            logger.error(error)
            list_send.append(f'{STR_CANCEL}{self.module_str} | {error}')
            return False

    def compare(self, prices):

        value = round_to(self.amount * prices[self.symbol])
        if value < MIN_TRANSFER_USD:
            logger.info(f'{self.module_str} | {value} {self.symbol} < {MIN_TRANSFER_USD} (usd $)')
            list_send.append(f'{STR_CANCEL}{self.module_str} | {value} {self.symbol} (value) less {MIN_TRANSFER_USD}')
            return False
        elif self.amount < MIN_TRANSFER_AMOUNT:
            logger.info(f'{self.module_str} | {self.amount} {self.symbol} < {MIN_TRANSFER_AMOUNT}')
            list_send.append(f'{STR_CANCEL}{self.module_str} | {self.amount} {self.symbol} (amount) less {MIN_TRANSFER_AMOUNT}')
            return False
        else:
            return True


async def worker(number, key, chain, token, prices, retry=0):

    transfer = Transfer(number, key, chain, token)
    await transfer.setup()

    if transfer.compare(prices) == False:
        return False

    contract_txn = await transfer.get_txn()
    if contract_txn is False: 
        return False

    status, tx_link = await transfer.manager.send_tx(contract_txn)

    if status == False:
        logger.error(f'{transfer.module_str}')
        list_send.append(f'{STR_CANCEL}{transfer.module_str}')
        return False
    elif status == 1:
        logger.success(f'{transfer.module_str} | {tx_link}')
        list_send.append(f'{STR_DONE}{transfer.module_str}')
        return True
    elif status == 0:
        logger.error(f'tx is failed | {tx_link}')
        if retry < RETRY:
            logger.info(f'try again in 3 sec.')
            await asyncio.sleep(3)
            return await worker(number, key, chain, token, prices, retry+1)
        else:
            list_send.append(f'{STR_CANCEL}{transfer.module_str}')
            return False
        
async def process(number, key, chain, tokens, prices):
    for token in tokens:
        await worker(number, key, chain, token, prices)
        await asyncio.sleep(SLEEPING_TIME)

async def main(datas):

    logger.info(f'getting prices...')
    prices = await get_prices(datas)
    logger.info(f'prices : {prices}')

    if RANDOM_WALLETS == True: 
        random.shuffle(WALLETS)

    batches = [WALLETS[i:i + WALLETS_IN_BATCH] for i in range(0, len(WALLETS), WALLETS_IN_BATCH)]

    number = 0
    for batch in batches:

        tasks = []
        for key in batch:
            number += 1

            for chain, tokens in datas.items():
                tasks.append(asyncio.create_task(process(f'[{number}/{len(WALLETS)}]', key, chain, tokens, prices)))

        await asyncio.gather(*tasks)

        if TG_BOT_SEND == True:
            send_msg() # отправляем результат в телеграм
        list_send.clear()

