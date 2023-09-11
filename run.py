from utils import main
from setting import ERC20_TOKENS, ETH_TOKENS
from config import WALLETS, RECIPIENTS
from data.title import TITLE, TITLE_COLOR
import asyncio
from loguru import logger
from termcolor import cprint

if __name__ == "__main__":

    cprint(TITLE, TITLE_COLOR)
    cprint(f'\nsubscribe to us : https://t.me/hodlmodeth\n', TITLE_COLOR)

    if len(WALLETS) == len(RECIPIENTS):

        print(f'Работаем с {len(WALLETS)} кошельками')
        print(input('\nENTER PRESS'))

        '''сначала запускаем трансфер erc20, затем eth токенов'''
        if len(ERC20_TOKENS) > 0:
            asyncio.run(main(ERC20_TOKENS))
        if len(ETH_TOKENS) > 0:
            ETH_TOKENS = {chain: [''] for chain in ETH_TOKENS}
            asyncio.run(main(ETH_TOKENS))

    else:
        logger.error(f'кол-во кошельков = {len(WALLETS)};  кол-во получателей = {len(RECIPIENTS)}')

